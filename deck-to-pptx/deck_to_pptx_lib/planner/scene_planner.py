from __future__ import annotations

from ..models import NormalizedSource, Scene, SourceSection
from ..utils.text import bullets_from_text, first_sentence


def _infer_content_role(section: SourceSection) -> str:
    title_text = section.title.lower()
    title_and_body = f"{section.title} {section.body}".lower()

    if section.images:
        return "image"
    if any(token in title_text for token in [" vs ", "对比", "比较", "trade-off"]):
        return "compare"
    if any(token in title_text for token in ["步骤", "流程", "工作流", "step", "process", "workflow"]):
        return "process"
    if any(token in title_and_body for token in ["quote", "引用", "观点", "原话"]):
        return "quote"
    if any(char.isdigit() for char in section.body) and len(section.bullets) >= 2:
        return "data"
    return "point"


def plan_scenes(source: NormalizedSource, max_slides: int) -> list[Scene]:
    max_slides = max(max_slides, 4)
    scenes: list[Scene] = [
        Scene(role="cover", title=source.title, thesis=source.subtitle or source.title),
        Scene(
            role="agenda",
            title="目录" if source.language == "zh" else "Agenda",
            thesis="",
            bullets=[section.title for section in source.sections[:6]],
        ),
    ]

    available = max_slides - 3
    ordered_sections = source.sections[:available]
    use_dividers = available > len(ordered_sections)

    if use_dividers:
        for section in ordered_sections:
            scenes.append(
                Scene(
                    role="section",
                    title=section.title,
                    thesis=first_sentence(section.body, max_len=120),
                    bullets=section.bullets[:4],
                    body=section.body,
                    source_refs=[section.source_ref] if section.source_ref else [],
                )
            )

    remaining = max_slides - len(scenes) - 1
    for section in ordered_sections:
        if remaining <= 0:
            break
        scenes.append(
            Scene(
                role=_infer_content_role(section),
                title=section.title,
                thesis=first_sentence(section.body, max_len=120),
                bullets=section.bullets[:4] or bullets_from_text(section.body, limit=4),
                body=section.body,
                image_path=section.images[0] if section.images else None,
                source_refs=[section.source_ref] if section.source_ref else [],
                importance=2,
            )
        )
        remaining -= 1

    scenes.append(
        Scene(
            role="closing",
            title="谢谢" if source.language == "zh" else "Thank You",
            thesis=source.title,
        )
    )
    return scenes[:max_slides]
