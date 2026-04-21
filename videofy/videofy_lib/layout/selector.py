"""
布局选择器
"""

from ..models import Slide
from .base import BaseLayout
from .registry import get_layout


class LayoutSelector:
    """布局选择器 - 根据内容选择合适的布局"""

    def __init__(self, theme: str = "linear"):
        self.theme = theme

    def select_layout(self, slide: Slide) -> BaseLayout:
        """为幻灯片选择布局"""
        layout_type = slide.layout_type
        return get_layout(layout_type, self.theme)
