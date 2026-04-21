from __future__ import annotations

import re
from pathlib import Path


def clean_text(text: str) -> str:
    if not text:
        return ""

    cleaned = text.replace("\r\n", "\n")
    cleaned = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", cleaned)
    cleaned = re.sub(r"\[\s*\]\([^)]+\)", "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    cleaned = re.sub(r"`{1,3}", "", cleaned)
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    lines = []
    for raw_line in cleaned.splitlines():
        stripped = raw_line.strip()
        if stripped in {"[", "]"}:
            continue
        if stripped.startswith("](") and stripped.endswith(")"):
            continue
        lines.append(raw_line)
    return "\n".join(lines).strip()


def detect_language(text: str) -> str:
    if not text:
        return "en"

    chinese = len(re.findall(r"[\u4e00-\u9fff]", text))
    compact = len(re.sub(r"\s", "", text))
    if compact and chinese / compact > 0.1:
        return "zh"
    return "en"


def slugify(text: str) -> str:
    compact = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    compact = re.sub(r"[-\s]+", "-", compact)
    return compact or "deck"


def split_sentences(text: str) -> list[str]:
    cleaned = clean_text(text)
    if not cleaned:
        return []

    parts = re.split(r"(?<=[。！？.!?])\s+|\n+", cleaned)
    return [part.strip(" -•") for part in parts if part.strip(" -•")]


def first_sentence(text: str, max_len: int = 110) -> str:
    sentences = split_sentences(text)
    if not sentences:
        return ""
    sentence = sentences[0]
    if len(sentence) <= max_len:
        return sentence
    return sentence[: max_len - 3].rstrip() + "..."


def bullets_from_text(text: str, limit: int = 4) -> list[str]:
    cleaned = clean_text(text)
    if not cleaned:
        return []

    explicit = []
    for line in cleaned.splitlines():
        stripped = line.strip()
        if re.match(r"^[-*+]\s+", stripped):
            explicit.append(re.sub(r"^[-*+]\s+", "", stripped))

    if explicit:
        return [item[:90] for item in explicit[:limit]]

    sentences = split_sentences(cleaned)
    bullets = []
    for sentence in sentences:
        if len(sentence) < 12:
            continue
        bullets.append(sentence[:90])
        if len(bullets) >= limit:
            break
    return bullets


def derive_title_from_path(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ").strip() or path.name


def clamp_text(text: str, max_len: int) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 3].rstrip() + "..."
