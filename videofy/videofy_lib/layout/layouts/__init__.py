"""
videofy 布局实现
"""

# 这些导入会自动触发布局注册
from .title import TitleLayout
from .agenda import AgendaLayout
from .topic_cover import TopicCoverLayout
from .topic_overview import TopicOverviewLayout
from .topic_detail import TopicDetailLayout
from .split_left import SplitLeftLayout
from .split_right import SplitRightLayout
from .code import CodeLayout
from .end import EndLayout

__all__ = [
    'TitleLayout', 'AgendaLayout', 'TopicCoverLayout',
    'TopicOverviewLayout', 'TopicDetailLayout',
    'SplitLeftLayout', 'SplitRightLayout',
    'CodeLayout', 'EndLayout'
]
