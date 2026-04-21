from __future__ import annotations

from pptx.dml.color import RGBColor


THEMES = {
    "tech-dark": {
        "name": "Tech Dark",
        "background": RGBColor(13, 16, 24),
        "surface": RGBColor(24, 29, 40),
        "primary": RGBColor(236, 241, 248),
        "secondary": RGBColor(170, 182, 201),
        "accent": RGBColor(78, 145, 208),
        "muted": RGBColor(123, 134, 152),
        "font": "Aptos",
        "display_font": "Aptos Display",
    },
    "business-light": {
        "name": "Business Light",
        "background": RGBColor(245, 248, 252),
        "surface": RGBColor(230, 236, 244),
        "primary": RGBColor(29, 40, 58),
        "secondary": RGBColor(78, 94, 118),
        "accent": RGBColor(44, 112, 172),
        "muted": RGBColor(126, 136, 152),
        "font": "Aptos",
        "display_font": "Aptos Display",
    },
    "editorial": {
        "name": "Editorial",
        "background": RGBColor(243, 239, 233),
        "surface": RGBColor(232, 225, 214),
        "primary": RGBColor(43, 37, 32),
        "secondary": RGBColor(106, 92, 81),
        "accent": RGBColor(128, 92, 66),
        "muted": RGBColor(141, 130, 118),
        "font": "Georgia",
        "display_font": "Georgia",
    },
    "bold-gradient": {
        "name": "Bold Gradient",
        "background": RGBColor(18, 23, 44),
        "surface": RGBColor(33, 44, 78),
        "primary": RGBColor(238, 244, 252),
        "secondary": RGBColor(187, 200, 223),
        "accent": RGBColor(234, 133, 92),
        "muted": RGBColor(132, 145, 174),
        "font": "Aptos",
        "display_font": "Aptos Display",
    },
}


def pick_style_direction(style: str, topic: str, audience: str, tone: str) -> str:
    if style in THEMES:
        return style

    topic_lower = f"{topic} {audience} {tone}".lower()
    if any(token in topic_lower for token in ["ai", "agent", "workflow", "automation", "product", "tech"]):
        return "tech-dark"
    if any(token in topic_lower for token in ["board", "finance", "business", "management", "汇报", "复盘"]):
        return "business-light"
    if any(token in topic_lower for token in ["brand", "editorial", "content", "观点", "方法论"]):
        return "editorial"
    return "bold-gradient"
