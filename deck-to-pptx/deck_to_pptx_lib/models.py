from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class InputBundle:
    mode: str
    raw_input: str
    topic: str
    outline: str = ""
    source_path: Optional[Path] = None
    local_files: list[Path] = field(default_factory=list)
    audience: str = ""
    tone: str = ""
    language: str = "auto"


@dataclass
class SourceSection:
    title: str
    body: str
    bullets: list[str] = field(default_factory=list)
    images: list[Path] = field(default_factory=list)
    source_ref: str = ""


@dataclass
class NormalizedSource:
    source_type: str
    title: str
    subtitle: str
    sections: list[SourceSection]
    images: list[Path] = field(default_factory=list)
    language: str = "zh"
    provenance: list[str] = field(default_factory=list)


@dataclass
class Scene:
    role: str
    title: str
    thesis: str
    bullets: list[str] = field(default_factory=list)
    body: str = ""
    image_path: Optional[Path] = None
    source_refs: list[str] = field(default_factory=list)
    importance: int = 1


@dataclass
class SlideSpec:
    slide_id: str
    role: str
    layout_hint: str
    title: str
    thesis: str
    bullets: list[str] = field(default_factory=list)
    body: str = ""
    image_path: Optional[Path] = None
    notes: str = ""


@dataclass
class DeckSpec:
    title: str
    subtitle: str
    audience: str
    tone: str
    style_direction: str
    language: str
    slides: list[SlideSpec] = field(default_factory=list)
    provenance: list[str] = field(default_factory=list)
    qa_notes: list[str] = field(default_factory=list)
