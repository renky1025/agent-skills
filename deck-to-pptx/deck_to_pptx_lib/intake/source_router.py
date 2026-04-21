from __future__ import annotations

from pathlib import Path

from ..models import InputBundle
from ..utils.files import collect_local_files
from ..utils.text import clean_text, detect_language, first_sentence


def route_source(
    source: str,
    outline: str = "",
    audience: str = "",
    tone: str = "",
    language: str = "auto",
) -> InputBundle:
    candidate_path = Path(source).expanduser()
    chosen_language = detect_language(source) if language == "auto" else language

    if candidate_path.exists():
        files = collect_local_files(candidate_path)
        mode = "materials_dir" if candidate_path.is_dir() else "local_file"
        topic = candidate_path.name if candidate_path.is_dir() else candidate_path.stem
        return InputBundle(
            mode=mode,
            raw_input=source,
            topic=topic,
            outline=outline,
            source_path=candidate_path,
            local_files=files,
            audience=audience,
            tone=tone,
            language=chosen_language,
        )

    source_clean = clean_text(source)
    if outline:
        mode = "brief"
        topic = first_sentence(source_clean, max_len=80) or source_clean
    elif "\n" in source_clean or len(source_clean) > 120:
        mode = "brief"
        lines = [line.strip() for line in source_clean.splitlines() if line.strip()]
        topic = lines[0] if lines else source_clean[:80]
        outline = "\n".join(lines[1:])
    else:
        mode = "topic"
        topic = source_clean

    return InputBundle(
        mode=mode,
        raw_input=source,
        topic=topic,
        outline=outline,
        audience=audience,
        tone=tone,
        language=chosen_language,
    )
