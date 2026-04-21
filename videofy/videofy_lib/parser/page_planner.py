"""
页面规划器 - 目录驱动的页面分配
"""

import math
from typing import List, Dict, Tuple
from ..models import AgendaItem, Slide, SlideContent, Section, ParsedDocument, ContentType
from ..config import DEFAULT_MAX_SLIDES
from ..utils.text import clean_text, clean_title
from .summarizer import (
    summarize_section_content,
    summarize_for_bullet_points
)
from .ai_summarizer import (
    extract_main_idea,
    generate_title_from_content
)


class PagePlanner:
    """
    页面规划器
    核心原则：
    1. 按重要性排序章节（图文优先）
    2. 超限内容直接丢弃
    3. 每个页面必须服务于目录中的主题
    """

    def __init__(self, max_slides: int = DEFAULT_MAX_SLIDES):
        self.max_slides = max_slides

    def _calculate_section_importance(self, section: Section) -> Tuple[int, int, int]:
        """
        计算章节重要性
        返回: (图片数量, 内容权重, 字符数) - 按优先级排序
        """
        image_count = 0
        total_weight = 0
        char_count = section.char_count

        for block in section.content_blocks:
            if block.type == ContentType.IMAGE:
                image_count += 1
            total_weight += block.weight

        return (image_count, total_weight, char_count)

    def generate_agenda(self, doc: ParsedDocument) -> List[AgendaItem]:
        """
        生成目录项 - 按重要性排序
        使用AI概括提炼中心思想，不是原文复制
        """
        agenda = []

        for i, section in enumerate(doc.sections, 1):
            # 收集章节所有文本内容
            section_texts = [b.content for b in section.content_blocks if b.content]
            full_content = ' '.join(section_texts)

            # 使用AI概括生成摘要
            summary = extract_main_idea(full_content)
            if not summary:
                summary = summarize_section_content(section.content_blocks)

            # 生成更好的标题（提炼中心思想）
            # 如果原标题太短或太泛（如"text"），生成新标题
            raw_title = section.title.strip()
            if len(raw_title) < 10 or raw_title.lower() in ['text', '文本', '内容']:
                # 从内容生成标题
                generated_title = generate_title_from_content(full_content, max_length=30)
                final_title = generated_title if generated_title else clean_title(raw_title)
            else:
                # 清理原标题中的数字
                final_title = clean_title(raw_title)

            item = AgendaItem(
                index=i,
                title=final_title,
                summary=summary,
                source_section=section
            )
            agenda.append(item)

        # 按重要性排序：图片数量 > 内容权重 > 字符数
        agenda.sort(key=lambda item: self._calculate_section_importance(item.source_section)
                    if item.source_section else (0, 0, 0), reverse=True)

        # 重新编号（1, 2, 3...）
        for i, item in enumerate(agenda, 1):
            item.index = i

        return agenda

    def distribute_pages(self, agenda: List[AgendaItem]) -> List[AgendaItem]:
        """
        分配页面数给每个目录项
        策略：
        1. 按重要性排序后选择前N个主题
        2. 超限内容直接丢弃
        """
        available = self.max_slides - 3  # 留给内容页的页面

        # 如果主题数超过可用页面，按重要性截断
        if len(agenda) > available:
            # 直接丢弃后面的主题
            agenda = agenda[:available]

        # 计算每个主题的内容权重
        weights = []
        for item in agenda:
            section = item.source_section
            if section:
                weight = section.total_weight
            else:
                weight = 1
            weights.append(weight)

        total_weight = sum(weights) or 1

        # 分配页面（每个主题至少1页）
        allocations = []
        for weight in weights:
            ratio = weight / total_weight
            pages = max(1, math.floor(available * ratio))
            allocations.append(pages)

        # 调整分配确保总和等于可用页面
        allocations = self._balance_allocations(allocations, available)

        # 应用分配
        for item, pages in zip(agenda, allocations):
            item.content_pages = pages

        return agenda

    def _balance_allocations(self, allocations: List[int], target: int) -> List[int]:
        """平衡分配确保总和等于目标"""
        if not allocations:
            return allocations

        current = sum(allocations)

        if current == target:
            return allocations

        if current < target:
            # 欠分：给分配最多的项增加
            diff = target - current
            max_idx = allocations.index(max(allocations))
            allocations[max_idx] += diff
        else:
            # 超分：从分配最多的项减少
            diff = current - target
            while diff > 0 and allocations:
                max_idx = allocations.index(max(allocations))
                if allocations[max_idx] > 1:
                    allocations[max_idx] -= 1
                    diff -= 1
                else:
                    break

        return allocations

    def plan_slides(self, doc: ParsedDocument) -> List[Slide]:
        """
        规划所有幻灯片
        """
        # 1. 生成目录
        agenda = self.generate_agenda(doc)
        agenda = self.distribute_pages(agenda)
        doc.agenda = agenda

        # 2. 生成幻灯片
        slides = []
        slide_num = 0

        # 标题页
        slide_num += 1
        slides.append(self._create_title_slide(doc, slide_num))

        # 目录页
        slide_num += 1
        slides.append(self._create_agenda_slide(agenda, slide_num))

        # 内容页 - 按目录项生成
        for item in agenda:
            item_slides = self._create_topic_slides(item, slide_num)
            slides.extend(item_slides)
            slide_num += len(item_slides)

        # 结束页
        slide_num += 1
        slides.append(self._create_end_slide(doc, slide_num))

        # 更新总数和编号
        total = len(slides)
        for i, slide in enumerate(slides, 1):
            slide.slide_number = i
            slide.total_slides = total

        doc.slides = slides
        return slides

    def _create_title_slide(self, doc: ParsedDocument, num: int) -> Slide:
        """创建标题页"""
        return Slide(
            slide_number=num,
            total_slides=0,  # 稍后更新
            layout_type="title",
            agenda_item=None,
            content=SlideContent(
                layout_type="title",
                title=doc.title,
                subtitle=doc.subtitle
            ),
            duration=6
        )

    def _create_agenda_slide(self, agenda: List[AgendaItem], num: int) -> Slide:
        """创建目录页"""
        # 只显示标题，不显示序号
        bullets = [item.title for item in agenda]

        return Slide(
            slide_number=num,
            total_slides=0,
            layout_type="agenda",
            agenda_item=None,
            content=SlideContent(
                layout_type="agenda",
                title="目录",
                bullets=bullets
            ),
            duration=5
        )

    def _create_topic_slides(self, item: AgendaItem, start_num: int) -> List[Slide]:
        """为主题创建内容页"""
        slides = []
        section = item.source_section

        if not section or not section.content_blocks:
            # 空章节，创建一个占位页
            slides.append(Slide(
                slide_number=start_num + len(slides),
                total_slides=0,
                layout_type="topic_cover",
                agenda_item=item,
                content=SlideContent(
                    layout_type="topic_cover",
                    title=item.title,
                    subtitle=item.summary
                ),
                duration=4
            ))
            return slides

        # 检查是否有图片
        images = [b for b in section.content_blocks if b.type.value == "image"]
        has_images = len(images) > 0

        # 第一页：主题封面
        # 如果有图片，第一页使用图文布局
        if has_images:
            img = images[0]
            # 图片说明：优先使用alt文本，否则使用章节摘要
            caption = img.image_caption if img.image_caption else item.summary
            slides.append(Slide(
                slide_number=start_num + len(slides),
                total_slides=0,
                layout_type="split_left",  # 左图右文
                agenda_item=item,
                content=SlideContent(
                    layout_type="image_text",
                    title=item.title,  # 标题使用原文
                    subtitle="",  # 副标题留空，使用body_text显示说明
                    image_path=img.image_path,
                    body_text=[caption] if caption else []  # 图片说明
                ),
                duration=5
            ))
        else:
            # 无图片，使用普通封面
            slides.append(Slide(
                slide_number=start_num + len(slides),
                total_slides=0,
                layout_type="topic_cover",
                agenda_item=item,
                content=SlideContent(
                    layout_type="topic_cover",
                    title=item.title,
                    subtitle=item.summary
                ),
                duration=5
            ))

        # 剩余页面分配具体内容
        remaining_pages = item.content_pages - 1

        if remaining_pages > 0:
            content_slides = self._distribute_content_to_slides(
                section.content_blocks, item, remaining_pages, start_num + len(slides)
            )
            slides.extend(content_slides)

        return slides

    def _distribute_content_to_slides(self, blocks: List, item: AgendaItem,
                                       page_count: int, start_num: int) -> List[Slide]:
        """将内容块分配到多个幻灯片
        要点使用AI概括，图片说明使用原文
        """
        slides = []

        # 按优先级排序内容块
        sorted_blocks = sorted(blocks, key=lambda b: b.weight, reverse=True)

        # 收集内容 - 分类处理
        key_points = []
        code_blocks = []
        images = []
        paragraphs = []

        for block in sorted_blocks:
            if block.type.value == "bullet_list":
                # 列表项使用AI概括
                points = summarize_for_bullet_points(block.content, num_bullets=3)
                key_points.extend(points)
            elif block.type.value == "paragraph":
                paragraphs.append(block.content)
            elif block.type.value == "code_block":
                code_blocks.append(block)
            elif block.type.value == "image":
                images.append(block)

        # 如果有段落，提取更多要点
        if paragraphs:
            combined = ' '.join(paragraphs)
            para_points = summarize_for_bullet_points(combined, num_bullets=4)
            key_points.extend(para_points)

        # 去重并限制数量
        seen = set()
        unique_points = []
        for p in key_points:
            p_clean = p.strip()
            if p_clean and p_clean not in seen:
                seen.add(p_clean)
                unique_points.append(p_clean)
        key_points = unique_points[:6]  # 最多6个要点

        # 根据页面数决定展示策略
        page_idx = 0

        # 概览页（如果有多页）
        if page_count >= 2 and key_points:
            overview_points = key_points[:4]
            slides.append(Slide(
                slide_number=start_num + page_idx,
                total_slides=0,
                layout_type="topic_overview",
                agenda_item=item,
                content=SlideContent(
                    layout_type="topic_overview",
                    title=item.title,  # 标题使用原文
                    bullets=overview_points  # 要点使用AI概括
                ),
                duration=5
            ))
            page_idx += 1

        # 图片页 - 图片说明使用原文
        while page_idx < page_count and images:
            img = images.pop(0)
            # 图片说明使用原文（caption）
            caption = img.image_caption if img.image_caption else ""
            slides.append(Slide(
                slide_number=start_num + page_idx,
                total_slides=0,
                layout_type="split_left" if page_idx % 2 == 0 else "split_right",
                agenda_item=item,
                content=SlideContent(
                    layout_type="image_text",
                    title=item.title,  # 标题使用原文
                    image_path=img.image_path,
                    body_text=[caption] if caption else []  # 图片说明使用原文
                ),
                duration=5
            ))
            page_idx += 1

        # 代码页 - 代码使用原文
        while page_idx < page_count and code_blocks:
            code = code_blocks.pop(0)
            slides.append(Slide(
                slide_number=start_num + page_idx,
                total_slides=0,
                layout_type="code",
                agenda_item=item,
                content=SlideContent(
                    layout_type="code",
                    title=item.title,  # 标题使用原文
                    code=code.content,  # 代码使用原文
                    code_lang=code.code_lang
                ),
                duration=6
            ))
            page_idx += 1

        # 剩余页面填充要点 - 使用AI概括
        while page_idx < page_count and key_points:
            points = key_points[:4]
            key_points = key_points[4:]

            slides.append(Slide(
                slide_number=start_num + page_idx,
                total_slides=0,
                layout_type="topic_detail",
                agenda_item=item,
                content=SlideContent(
                    layout_type="detail",
                    title=item.title,  # 标题使用原文
                    bullets=points  # 要点使用AI概括
                ),
                duration=5
            ))
            page_idx += 1

        return slides

    def _create_end_slide(self, doc: ParsedDocument, num: int) -> Slide:
        """创建结束页"""
        end_text = "感谢观看"

        return Slide(
            slide_number=num,
            total_slides=0,
            layout_type="end",
            agenda_item=None,
            content=SlideContent(
                layout_type="end",
                title=end_text
            ),
            duration=4
        )
