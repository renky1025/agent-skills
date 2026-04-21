from __future__ import annotations

from ..models import DeckSpec, NormalizedSource, Scene, SlideSpec
from ..renderer.layout_registry import layout_for_role
from ..renderer.theme_registry import pick_style_direction


def build_deck(
    source: NormalizedSource,
    scenes: list[Scene],
    style: str = "auto",
    audience: str = "",
    tone: str = "",
) -> DeckSpec:
    style_direction = pick_style_direction(style, source.title, audience, tone)
    slides: list[SlideSpec] = []

    for index, scene in enumerate(scenes, start=1):
        slides.append(
            SlideSpec(
                slide_id=f"slide-{index}",
                role=scene.role,
                layout_hint=layout_for_role(scene.role),
                title=scene.title,
                thesis=scene.thesis,
                bullets=scene.bullets,
                body=scene.body,
                image_path=scene.image_path,
            )
        )

    return DeckSpec(
        title=source.title,
        subtitle=source.subtitle,
        audience=audience,
        tone=tone,
        style_direction=style_direction,
        language=source.language,
        slides=slides,
        provenance=source.provenance,
    )
