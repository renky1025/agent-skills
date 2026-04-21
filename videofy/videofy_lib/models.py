"""
数据模型定义
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum


class ContentType(Enum):
    """内容块类型"""
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    BULLET_LIST = "bullet_list"
    CODE_BLOCK = "code_block"
    IMAGE = "image"
    TABLE = "table"
    QUOTE = "quote"


@dataclass
class ContentBlock:
    """内容块 - 原始Markdown内容"""
    type: ContentType
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    # 图片相关
    image_path: Optional[str] = None
    image_caption: str = ""
    # 代码相关
    code_lang: str = ""
    # 层级
    level: int = 1
    # 权重（用于页面分配）
    weight: int = 1


@dataclass
class Section:
    """文档章节"""
    title: str
    level: int
    content_blocks: List[ContentBlock] = field(default_factory=list)
    subsections: List['Section'] = field(default_factory=list)

    @property
    def char_count(self) -> int:
        """内容字符数"""
        count = len(self.title)
        for block in self.content_blocks:
            count += len(block.content)
        return count

    @property
    def total_weight(self) -> int:
        """总权重"""
        return sum(block.weight for block in self.content_blocks)


@dataclass
class AgendaItem:
    """目录项 - 页面规划的驱动"""
    index: int
    title: str
    summary: str
    content_pages: int = 1
    source_section: Optional[Section] = None

    def __repr__(self):
        return f"AgendaItem({self.index}: {self.title} - {self.content_pages} pages)"


@dataclass
class SlideContent:
    """单页幻灯片内容"""
    layout_type: str
    title: str
    subtitle: str = ""
    body_text: List[str] = field(default_factory=list)
    bullets: List[str] = field(default_factory=list)
    code: str = ""
    code_lang: str = ""
    image_path: Optional[str] = None
    image_caption: str = ""
    cards: List[Dict[str, str]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Slide:
    """幻灯片 - 带页面编号和归属"""
    slide_number: int
    total_slides: int
    layout_type: str
    agenda_item: Optional[AgendaItem]
    content: SlideContent
    duration: int = 5

    @property
    def is_first(self) -> bool:
        return self.slide_number == 1

    @property
    def is_last(self) -> bool:
        return self.slide_number == self.total_slides

    @property
    def progress(self) -> float:
        return (self.slide_number / self.total_slides) * 100


@dataclass
class ParsedDocument:
    """解析后的完整文档"""
    title: str
    subtitle: str
    sections: List[Section]
    agenda: List[AgendaItem]
    slides: List[Slide] = field(default_factory=list)
    language: str = "zh"
