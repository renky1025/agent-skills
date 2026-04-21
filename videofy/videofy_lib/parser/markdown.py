"""
Markdown 解析器
"""

import re
from typing import List, Optional, Tuple
from ..models import ContentBlock, ContentType, Section, ParsedDocument
from ..utils.text import clean_text, detect_language, extract_title_from_path
from .image_matcher import ImageMatcher


class MarkdownParser:
    """Markdown 文档解析器"""

    def __init__(self, md_path: str, images_dir: Optional[str] = None):
        self.md_path = md_path
        self.images_dir = images_dir
        self.image_matcher = ImageMatcher(images_dir)
        self.raw_content = self._read_file()
        self.language = detect_language(self.raw_content)

    def _read_file(self) -> str:
        """读取 Markdown 文件"""
        with open(self.md_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _extract_title(self) -> Tuple[str, str]:
        """提取主标题和副标题"""
        # 从文件名获取基础标题
        title = extract_title_from_path(self.md_path)

        # 尝试从内容提取副标题
        subtitle = ""
        lines = self.raw_content.split('\n')

        for line in lines:
            line = line.strip()
            if not line or line.startswith('![') or line.startswith('#'):
                continue

            clean = clean_text(line)
            if 20 < len(clean) < 150:
                subtitle = clean
                break

        return title, subtitle

    def _parse_content_blocks(self, text: str) -> List[ContentBlock]:
        """解析内容块"""
        blocks = []

        # 按双换行分割段落
        chunks = re.split(r'\n\n+', text)

        for chunk in chunks:
            chunk = chunk.strip()
            if not chunk:
                continue

            block = self._classify_block(chunk)
            if block:
                blocks.append(block)

        return blocks

    def _classify_block(self, text: str) -> Optional[ContentBlock]:
        """分类内容块"""
        text = text.strip()
        if not text:
            return None

        # 代码块
        if text.startswith('```'):
            return self._parse_code_block(text)

        # 标题
        if text.startswith('#'):
            level = len(text) - len(text.lstrip('#'))
            title = clean_text(text.lstrip('#'))
            return ContentBlock(
                type=ContentType.HEADING,
                content=title,
                level=level,
                weight=10 - level  # 级别越高，权重越高
            )

        # 图片
        if text.startswith('!['):
            img_match = re.match(r'!\[([^\]]*)\]\s*\(([^)]+)\)', text)
            if img_match:
                alt_text = img_match.group(1)
                img_ref = img_match.group(2)
                img_path = self.image_matcher.find_image(img_ref)

                # 图片说明处理：如果是"图像"等占位符，使用空字符串
                # 后续会从上下文提取描述
                caption = alt_text.strip()
                if caption in ['图像', 'image', '图片', 'figure', 'img']:
                    caption = ""

                return ContentBlock(
                    type=ContentType.IMAGE,
                    content=alt_text,
                    image_path=img_path,
                    image_caption=caption,
                    weight=8
                )

        # 列表
        if re.match(r'^[-*+]\s', text, re.MULTILINE):
            items = []
            for line in text.split('\n'):
                if re.match(r'^[-*+]\s', line):
                    item = clean_text(re.sub(r'^[-*+]\s', '', line))
                    if item:
                        items.append(item)
            if items:
                return ContentBlock(
                    type=ContentType.BULLET_LIST,
                    content='\n'.join(items),
                    weight=7
                )

        # 引用
        if text.startswith('>'):
            quote = clean_text(re.sub(r'^>\s?', '', text, flags=re.MULTILINE))
            return ContentBlock(
                type=ContentType.QUOTE,
                content=quote,
                weight=6
            )

        # 表格
        if '|' in text and '\n' in text:
            lines = text.split('\n')
            if all('|' in line for line in lines[:2]):
                return ContentBlock(
                    type=ContentType.TABLE,
                    content=text,
                    weight=4
                )

        # 普通段落
        clean = clean_text(text)
        if len(clean) > 10:
            return ContentBlock(
                type=ContentType.PARAGRAPH,
                content=clean,
                weight=5
            )

        return None

    def _parse_code_block(self, text: str) -> ContentBlock:
        """解析代码块"""
        lines = text.split('\n')

        # 提取语言
        lang = ""
        if lines[0].startswith('```'):
            lang = lines[0][3:].strip()

        # 提取代码内容
        code_lines = []
        for line in lines[1:]:
            if line.strip() == '```':
                break
            code_lines.append(line)

        code = '\n'.join(code_lines)

        return ContentBlock(
            type=ContentType.CODE_BLOCK,
            content=code[:500],  # 限制长度
            code_lang=lang,
            weight=6
        )

    def parse_sections(self) -> List[Section]:
        """解析为章节结构
        支持标准 Markdown 标题 (## 标题) 和纯文本标题
        """
        sections = []
        current_section: Optional[Section] = None
        current_content = []

        lines = self.raw_content.split('\n')
        i = 0

        # 首先收集所有可能的标题行
        potential_titles = []
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                continue

            # Markdown 标题
            if re.match(r'^#{2,3}\s+', stripped):
                title = re.sub(r'^#{2,3}\s*', '', stripped)
                potential_titles.append((idx, title, 'markdown'))
                continue

            # 一级标题作为文档标题
            if re.match(r'^#\s+', stripped):
                continue

            # 排除明显的非标题
            if stripped in ['图像', 'Image', '图片'] or stripped.startswith('!['):
                continue

            # 纯文本标题特征：
            # 1. 长度适中 (5-40个字符)
            # 2. 不包含常见标点
            # 3. 后面是空行或图片
            # 4. 不是列表项
            if (5 < len(stripped) < 40 and
                not stripped.startswith(('- ', '* ', '1.', '2.', '3.')) and
                not re.search(r'[。！？.,;:!?]', stripped[-3:]) and
                idx + 1 < len(lines)):

                next_line = lines[idx + 1].strip()
                # 检查是否是标题模式
                if (next_line == '' or
                    next_line.startswith('![') or
                    next_line.startswith('[') or
                    next_line.startswith('http')):
                    potential_titles.append((idx, stripped, 'text'))

        # 使用检测到的标题分割文档
        if len(potential_titles) >= 2:
            for i, (idx, title, title_type) in enumerate(potential_titles):
                # 确定这个章节的结束位置
                end_idx = potential_titles[i + 1][0] if i + 1 < len(potential_titles) else len(lines)

                # 提取内容
                content_lines = lines[idx + 1:end_idx]
                content = '\n'.join(content_lines)

                section = Section(
                    title=clean_text(title),
                    level=2,
                    content_blocks=self._parse_content_blocks(content),
                    subsections=[]
                )
                sections.append(section)
        else:
            # 如果没有检测到足够的标题，将整个文档作为一个章节
            blocks = self._parse_content_blocks(self.raw_content)
            if blocks:
                sections.append(Section(
                    title=extract_title_from_path(self.md_path),
                    level=2,
                    content_blocks=blocks,
                    subsections=[]
                ))

        return sections

    def parse(self) -> ParsedDocument:
        """完整解析文档"""
        title, subtitle = self._extract_title()
        sections = self.parse_sections()

        return ParsedDocument(
            title=title,
            subtitle=subtitle,
            sections=sections,
            agenda=[],  # 将在 PagePlanner 中生成
            slides=[],
            language=self.language
        )
