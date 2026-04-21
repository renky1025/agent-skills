ROLE_TO_LAYOUT = {
    "cover": "cover-hero",
    "agenda": "agenda-grid",
    "section": "section-divider",
    "point": "point-spotlight",
    "image": "image-split",
    "compare": "compare-columns",
    "process": "process-track",
    "quote": "quote-poster",
    "data": "data-dashboard",
    "closing": "closing-clean",
}


def layout_for_role(role: str) -> str:
    return ROLE_TO_LAYOUT.get(role, "point-spotlight")
