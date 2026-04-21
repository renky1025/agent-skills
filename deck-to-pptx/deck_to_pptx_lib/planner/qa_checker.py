from __future__ import annotations

from ..models import DeckSpec
from ..utils.text import bullets_from_text, clamp_text, first_sentence


def _normalized(text: str) -> str:
    return " ".join((text or "").lower().split())


ROLE_TITLE_LIMITS = {
    "cover": 64,
    "agenda": 64,
    "closing": 64,
}

ROLE_THESIS_LIMITS = {
    "point": 105,
    "data": 95,
    "image": 110,
    "compare": 100,
    "process": 100,
}

ROLE_BULLET_LIMITS = {
    "agenda": (6, 64),
    "point": (4, 68),
    "data": (4, 72),
    "image": (3, 76),
    "compare": (4, 66),
    "process": (4, 82),
    "quote": (3, 80),
}


def run_qa(deck: DeckSpec) -> DeckSpec:
    notes: list[str] = []

    for slide in deck.slides:
        title_limit = ROLE_TITLE_LIMITS.get(slide.role, 56)
        thesis_limit = ROLE_THESIS_LIMITS.get(slide.role, 140)
        bullet_count_limit, bullet_len_limit = ROLE_BULLET_LIMITS.get(slide.role, (5, 90))

        slide.title = clamp_text(slide.title or deck.title, title_limit)
        slide.thesis = clamp_text(slide.thesis or "", thesis_limit)

        if slide.role not in {"cover", "closing", "agenda"} and not slide.thesis:
            slide.thesis = first_sentence(slide.body, max_len=120)
            notes.append(f"{slide.slide_id}: filled missing thesis")

        if slide.role == "agenda":
            slide.bullets = [clamp_text(item, bullet_len_limit) for item in slide.bullets[:bullet_count_limit]]
        else:
            if not slide.bullets and slide.body:
                slide.bullets = bullets_from_text(slide.body, limit=4)
                if slide.bullets:
                    notes.append(f"{slide.slide_id}: derived bullets from body")
            slide.bullets = [clamp_text(item, bullet_len_limit) for item in slide.bullets[:bullet_count_limit]]

            thesis_norm = _normalized(slide.thesis)
            deduped: list[str] = []
            for bullet in slide.bullets:
                bullet_norm = _normalized(bullet)
                if thesis_norm and bullet_norm == thesis_norm:
                    notes.append(f"{slide.slide_id}: removed thesis-duplicate bullet")
                    continue
                if deduped and bullet_norm == _normalized(deduped[-1]):
                    notes.append(f"{slide.slide_id}: removed repeated bullet")
                    continue
                deduped.append(bullet)
            slide.bullets = deduped

        if slide.role in {"data", "compare", "process"} and not slide.bullets and slide.thesis:
            slide.bullets = [slide.thesis]

    deck.qa_notes = notes
    return deck
