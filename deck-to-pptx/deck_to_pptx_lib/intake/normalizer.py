from __future__ import annotations

import re
import subprocess
from pathlib import Path

try:
    from docx import Document
except Exception:  # pragma: no cover - optional dependency
    Document = None

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover - optional dependency
    PdfReader = None

from ..models import InputBundle, NormalizedSource, SourceSection
from ..utils.files import split_local_files
from ..utils.text import (
    bullets_from_text,
    clean_text,
    derive_title_from_path,
    detect_language,
    first_sentence,
)
from .web_research import research_topic_markdown


def _read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_docx_file(path: Path) -> str:
    if Document is None:
        return ""
    document = Document(path)
    paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
    return "\n\n".join(paragraphs)


def _read_pdf_file(path: Path) -> str:
    if PdfReader is not None:
        try:
            reader = PdfReader(str(path))
            pages = [page.extract_text() or "" for page in reader.pages]
            text = "\n\n".join(page.strip() for page in pages if page.strip())
            if text:
                return text
        except Exception:
            pass

    try:
        result = subprocess.run(
            ["/usr/bin/strings", str(path)],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception:
        return ""

    if result.returncode != 0:
        return ""

    cleaned_lines: list[str] = []
    for raw_line in result.stdout.splitlines():
        line = raw_line.strip()
        if len(line) <= 4:
            continue
        if any(token in line for token in ["obj", "endobj", "stream", "endstream", "trailer", "%PDF", "xref", "<<", ">>"]):
            continue

        if "(" in line and ")" in line:
            extracted_parts = []
            current = []
            depth = 0
            for char in line:
                if char == "(":
                    depth += 1
                    if depth == 1:
                        current = []
                        continue
                if char == ")" and depth:
                    depth -= 1
                    if depth == 0:
                        extracted_parts.append("".join(current))
                        current = []
                        continue
                if depth >= 1:
                    current.append(char)
            line = " ".join(part.strip() for part in extracted_parts if part.strip())

        line = line.strip()
        if len(line) > 4:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def _read_supported_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        return _read_text_file(path)
    if suffix == ".docx":
        return _read_docx_file(path)
    if suffix == ".pdf":
        return _read_pdf_file(path)
    return ""


def _extract_markdown_images(markdown_text: str, source_dirs: list[Path] | None) -> list[Path]:
    if not source_dirs:
        return []

    images: list[Path] = []
    for match in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", markdown_text):
        raw_target = match.group(1).strip()
        if not raw_target or "://" in raw_target:
            continue
        for source_dir in source_dirs:
            image_path = (source_dir / raw_target).resolve()
            if image_path.exists():
                if image_path not in images:
                    images.append(image_path)
                break
    return images


def _parse_markdown(
    markdown_text: str,
    fallback_title: str,
    source_dirs: list[Path] | None = None,
) -> tuple[str, str, list[SourceSection]]:
    lines = markdown_text.splitlines()
    title = fallback_title
    subtitle = ""
    sections: list[SourceSection] = []

    current_title: str | None = None
    current_lines: list[str] = []

    def flush_section() -> None:
        nonlocal current_title, current_lines
        if not current_title:
            return
        raw_body = "\n".join(current_lines)
        body = clean_text(raw_body)
        if not body:
            current_title = None
            current_lines = []
            return
        sections.append(
            SourceSection(
                title=current_title,
                body=body,
                bullets=bullets_from_text(body),
                images=_extract_markdown_images(raw_body, source_dirs),
            )
        )
        current_title = None
        current_lines = []

    def next_nonempty_line(start: int) -> tuple[int | None, str]:
        for index in range(start, len(lines)):
            candidate = lines[index].strip()
            if candidate:
                return index, candidate
        return None, ""

    def consume_heading(start: int) -> tuple[int, int | None, str]:
        stripped = lines[start].strip()
        if not stripped.startswith("#"):
            return 0, None, ""

        marker = stripped.lstrip("#")
        level = len(stripped) - len(marker)
        inline_title = clean_text(marker)
        if inline_title:
            return level, start, inline_title

        next_index, next_line = next_nonempty_line(start + 1)
        if next_index is None or next_line.startswith("#"):
            return level, start, ""
        return level, next_index, clean_text(next_line)

    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if stripped.startswith("#"):
            level, consumed_index, heading_title = consume_heading(index)
            if heading_title:
                if level == 1:
                    title = heading_title or fallback_title
                    index = (consumed_index or index) + 1
                    continue
                if level == 2:
                    flush_section()
                    current_title = heading_title
                    index = (consumed_index or index) + 1
                    continue

        if stripped and not subtitle and not stripped.startswith("#"):
            subtitle = first_sentence(stripped, max_len=120)
        if current_title:
            current_lines.append(line)
        index += 1

    flush_section()

    if not sections:
        body = clean_text(markdown_text)
        paragraphs = [segment.strip() for segment in body.split("\n\n") if segment.strip()]
        for index, paragraph in enumerate(paragraphs[:4], start=1):
            sections.append(
                SourceSection(
                    title=f"Section {index}" if detect_language(body) == "en" else f"第 {index} 部分",
                    body=paragraph,
                    bullets=bullets_from_text(paragraph),
                )
            )

    return title, subtitle, sections


def _normalize_from_materials(bundle: InputBundle) -> NormalizedSource:
    assert bundle.local_files
    text_files, image_files = split_local_files(bundle.local_files)

    combined_parts: list[str] = []
    provenance: list[str] = []
    markdown_files = [file_path for file_path in text_files if file_path.suffix.lower() == ".md"]

    for file_path in text_files:
        try:
            text = _read_supported_file(file_path)
        except Exception:
            text = ""
        if not text:
            continue
        provenance.append(str(file_path))
        if file_path.suffix.lower() == ".md":
            combined_parts.append(text)
        else:
            combined_parts.append(f"## {derive_title_from_path(file_path)}\n\n{text}")

    if not combined_parts:
        combined_parts.append(f"# {bundle.topic}\n\n## Summary\n\nNo supported text material was found.")

    source_dirs: list[Path] = []
    if len(markdown_files) == 1:
        source_dirs.append(markdown_files[0].parent)
    if bundle.source_path:
        source_dirs.append(bundle.source_path)
    title, subtitle, sections = _parse_markdown(
        "\n\n".join(combined_parts),
        fallback_title=bundle.topic,
        source_dirs=source_dirs,
    )

    return NormalizedSource(
        source_type=bundle.mode,
        title=title,
        subtitle=subtitle,
        sections=sections,
        images=image_files,
        language=bundle.language if bundle.language != "auto" else detect_language(title),
        provenance=provenance,
    )


def _normalize_from_text(bundle: InputBundle) -> NormalizedSource:
    if bundle.mode == "topic":
        markdown_text = research_topic_markdown(bundle.topic, bundle.language)
    else:
        outline_lines = [line.strip(" -•\t") for line in bundle.outline.splitlines() if line.strip()]
        if outline_lines:
            body = "\n\n".join(f"## {line}\n\n{line}" for line in outline_lines)
            markdown_text = f"# {bundle.topic}\n\n{body}"
        else:
            markdown_text = f"# {bundle.topic}\n\n{bundle.outline or bundle.raw_input}"

    title, subtitle, sections = _parse_markdown(markdown_text, fallback_title=bundle.topic)

    return NormalizedSource(
        source_type=bundle.mode,
        title=title,
        subtitle=subtitle,
        sections=sections,
        images=[],
        language=detect_language(markdown_text),
        provenance=[bundle.raw_input],
    )


def normalize_bundle(bundle: InputBundle) -> NormalizedSource:
    if bundle.mode in {"materials_dir", "local_file"}:
        return _normalize_from_materials(bundle)
    return _normalize_from_text(bundle)
