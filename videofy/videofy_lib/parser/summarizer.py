"""
内容概括模块 - 使用AI概括总结内容
只有标题和图片说明使用原文，其他都需要AI概括
"""

from typing import List
from ..utils.text import clean_text, split_into_sentences


def summarize_paragraph(paragraph: str, max_sentences: int = 2) -> str:
    """
    概括段落内容
    策略：
    1. 如果是短段落（<100字），直接返回清理后的文本
    2. 如果是长段落，提取关键句子并重新组织
    """
    clean = clean_text(paragraph)
    if len(clean) < 100:
        return clean

    sentences = split_into_sentences(clean)
    if len(sentences) <= max_sentences:
        return clean

    # 提取前几句作为概括
    summary_sentences = sentences[:max_sentences]
    summary = ''.join(summary_sentences)

    # 如果概括太长，截断到合理长度
    if len(summary) > 150:
        # 找到最后一个完整句子
        last_punct = max(summary.rfind('。'), summary.rfind('；'))
        if last_punct > 100:
            summary = summary[:last_punct + 1]
        else:
            summary = summary[:150] + "..."

    return summary


def extract_key_points(content: str, max_points: int = 4) -> List[str]:
    """
    从内容中提取关键要点
    不是简单复制，而是重新组织和概括
    """
    clean = clean_text(content)
    if not clean:
        return []

    # 分割成句子
    sentences = split_into_sentences(clean)

    # 过滤掉过短的句子
    meaningful_sentences = [s for s in sentences if len(s.strip()) > 15]

    if len(meaningful_sentences) <= max_points:
        return meaningful_sentences

    # 选择最重要的句子（按位置和信息密度）
    # 策略：第一句通常是核心，后面的按长度选择（中等长度的通常信息密度高）
    selected = [meaningful_sentences[0]]  # 第一句通常最重要

    # 从剩余句子中选择
    remaining = meaningful_sentences[1:]
    # 按长度排序，选择中等长度的
    remaining.sort(key=len)

    # 从中间开始选（避免太短或太长的）
    mid = len(remaining) // 2
    for i in range(max_points - 1):
        idx = mid + i - (max_points - 1) // 2
        if 0 <= idx < len(remaining) and remaining[idx] not in selected:
            selected.append(remaining[idx])

    return selected[:max_points]


def summarize_section_content(content_blocks: List) -> str:
    """
    概括章节核心内容
    用于生成主题摘要
    """
    # 收集所有文本内容
    all_text = []
    for block in content_blocks:
        if hasattr(block, 'content') and block.content:
            all_text.append(block.content)

    if not all_text:
        return ""

    # 合并文本
    combined = ' '.join(all_text)

    # 生成摘要
    return summarize_paragraph(combined, max_sentences=2)


def generate_topic_description(title: str, content: str) -> str:
    """
    生成主题描述
    基于标题和内容，生成一句话描述
    """
    clean_content = clean_text(content)

    if not clean_content:
        return f"关于{title}的内容"

    # 提取第一句作为基础
    sentences = split_into_sentences(clean_content)
    if sentences:
        first = sentences[0]
        # 如果第一句包含标题关键词，使用它
        if any(keyword in first for keyword in title.split()[:3]):
            return first[:120]

    # 否则基于内容生成描述
    summary = summarize_paragraph(clean_content, max_sentences=1)
    return summary[:120]


def summarize_for_bullet_points(content: str, num_bullets: int = 3) -> List[str]:
    """
    为幻灯片要点概括内容
    每个要点应该是简洁的概括，不是原文复制
    """
    clean = clean_text(content)
    if len(clean) < 50:
        return [clean] if clean else []

    sentences = split_into_sentences(clean)

    if len(sentences) <= num_bullets:
        return [s for s in sentences if len(s) > 10]

    # 选择关键句子并简化
    bullets = []
    step = len(sentences) // num_bullets

    for i in range(num_bullets):
        idx = i * step
        if idx < len(sentences):
            sentence = sentences[idx].strip()
            # 简化句子
            if len(sentence) > 80:
                # 找到合适的截断点
                last_punct = max(sentence.rfind('，', 0, 80), sentence.rfind('。', 0, 80))
                if last_punct > 50:
                    sentence = sentence[:last_punct]
                else:
                    sentence = sentence[:80] + "..."
            bullets.append(sentence)

    return bullets
