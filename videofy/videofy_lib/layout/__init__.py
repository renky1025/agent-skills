"""
videofy 布局模块
"""

from .base import BaseLayout
from .registry import register_layout, get_layout, get_available_layouts
from .selector import LayoutSelector

# 自动导入所有布局以触发注册
from .layouts import (
    title, agenda, topic_cover, topic_overview,
    topic_detail, split_left, split_right, code, end
)

__all__ = [
    'BaseLayout', 'register_layout', 'get_layout',
    'get_available_layouts', 'LayoutSelector'
]
