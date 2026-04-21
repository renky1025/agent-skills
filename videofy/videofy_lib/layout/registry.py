"""
布局注册表
"""

from typing import Dict, Type
from .base import BaseLayout

# 布局注册表
_layout_registry: Dict[str, Type[BaseLayout]] = {}


def register_layout(layout_class: Type[BaseLayout]):
    """注册布局类"""
    instance = layout_class()
    _layout_registry[instance.layout_type] = layout_class
    return layout_class


def get_layout(layout_type: str, theme: str = "linear") -> BaseLayout:
    """获取布局实例"""
    layout_class = _layout_registry.get(layout_type)
    if not layout_class:
        # 默认使用第一个可用布局
        layout_class = list(_layout_registry.values())[0]
    return layout_class(theme)


def get_available_layouts() -> list:
    """获取可用布局列表"""
    return list(_layout_registry.keys())
