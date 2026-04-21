from __future__ import annotations

from pathlib import Path

from ..config import IMAGE_EXTENSIONS, TEXT_EXTENSIONS


def collect_local_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]

    files = [item for item in path.rglob("*") if item.is_file()]
    return sorted(files, key=lambda item: str(item).lower())


def split_local_files(files: list[Path]) -> tuple[list[Path], list[Path]]:
    text_files: list[Path] = []
    image_files: list[Path] = []

    for file_path in files:
        suffix = file_path.suffix.lower()
        if suffix in TEXT_EXTENSIONS:
            text_files.append(file_path)
        elif suffix in IMAGE_EXTENSIONS:
            image_files.append(file_path)

    return text_files, image_files


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
