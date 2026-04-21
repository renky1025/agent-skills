"""
文本处理工具
"""

import re
from typing import List, Tuple


def clean_text(text: str) -> str:
    """清理文本但保留结构"""
    if not text:
        return ""

    # 移除 Markdown 图片链接
    text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', text)
    # 移除普通链接，保留文字
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # 移除裸链接
    text = re.sub(r'\]?\(https?://[^\s)]+\)?', '', text)
    text = re.sub(r'https?://\S+', '', text)
    # 移除 Markdown 标记
    text = re.sub(r'\*\*', '', text)
    text = re.sub(r'(?<!\*)\*(?!\*)', '', text)
    text = re.sub(r'`', '', text)
    text = re.sub(r'#+\s*', '', text)
    # 移除空括号
    text = re.sub(r'\[\s*\]', '', text)
    text = re.sub(r'\(\s*\)', '', text)
    text = re.sub(r'\]\(', '', text)
    # 清理多余空格
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def extract_title_from_path(path: str) -> str:
    """从文件路径提取标题"""
    import os
    basename = os.path.basename(path)
    name = os.path.splitext(basename)[0]
    return name.replace('_', ' ').replace('-', ' ').strip()


def detect_language(text: str) -> str:
    """检测文本语言"""
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    total_chars = len(re.sub(r'\s', '', text))
    if total_chars > 0 and chinese_chars / total_chars > 0.1:
        return 'zh'
    return 'en'


def split_into_sentences(text: str) -> List[str]:
    """将文本分割成句子"""
    # 中文句子分隔
    sentences = re.split(r'(?<=[。！？])\s*', text)
    # 过滤空句子
    return [s.strip() for s in sentences if s.strip()]


def summarize_text(text: str, max_length: int = 100) -> str:
    """摘要文本"""
    sentences = split_into_sentences(text)
    if not sentences:
        return text[:max_length]

    # 取第一句作为摘要
    summary = sentences[0]
    if len(summary) > max_length:
        summary = summary[:max_length] + "..."

    return summary


def generate_agenda_summary(section_title: str, content: str) -> str:
    """
    为目录项生成一句话摘要
    确保提取完整的一句话，不截断
    """
    clean = clean_text(content)

    # 尝试提取核心主题（通常在第一段）
    paragraphs = [p for p in clean.split('\n\n') if len(p.strip()) > 20]

    if not paragraphs:
        return f"关于{section_title}的介绍"

    # 取第一句完整的句子
    first_para = paragraphs[0]
    sentences = split_into_sentences(first_para)

    if sentences:
        # 取第一句，确保完整
        summary = sentences[0].strip()
        # 如果第一句太短（少于15字），尝试拼接第二句
        if len(summary) < 15 and len(sentences) > 1:
            summary = summary + sentences[1].strip()
    else:
        # 如果连一个完整句子都找不到，取前50字并确保在标点处截断
        summary = first_para[:50]
        # 找最后一个标点，确保不截断
        last_punct = max(summary.rfind('。'), summary.rfind('，'),
                         summary.rfind('；'), summary.rfind('：'))
        if last_punct > 20:
            summary = summary[:last_punct + 1]

    return summary.strip()


def clean_title(text: str) -> str:
    """
    清理标题，移除数字序号
    例如：
    - "1. 标题" → "标题"
    - "一、标题" → "标题"
    - "第1章 标题" → "标题"
    - "32. 5. 标题" → "标题"
    """
    if not text:
        return ""

    # 先进行基础清理
    text = clean_text(text)

    # 移除开头的数字序号模式
    # 匹配：数字. 或 数字、 或 第数字章 或 第数字节 或 中文数字
    patterns = [
        r'^\d+\.\s*',           # "1. " 或 "12. "
        r'^[一二三四五六七八九十]+[、\.\s]+',  # "一、" 或 "二."
        r'^第[\d一二三四五六七八九十]+[章节]\s*[、\.\-]?\s*',  # "第一章 " 或 "第1章、"
        r'^\d+\s*[、\.\-]\s*',   # "1、" 或 "1."
    ]

    for pattern in patterns:
        text = re.sub(pattern, '', text)

    # 清理可能残留的多余空格
    text = text.strip()

    return text


def truncate_to_length(text: str, max_length: int, suffix: str = "...") -> str:
    """截断文本到指定长度"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_keywords(text: str, top_n: int = 5) -> List[str]:
    """提取关键词（简单实现）"""
    # 移除标点
    clean = re.sub(r'[^\w\s]', '', text.lower())
    words = clean.split()

    # 过滤常见词
    stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                  '的', '是', '在', '和', '了', '有', '与', '及'}

    word_counts = {}
    for word in words:
        if word not in stop_words and len(word) > 2:
            word_counts[word] = word_counts.get(word, 0) + 1

    # 排序返回
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_words[:top_n]]


def escape_html(text: str) -> str:
    """转义 HTML 特殊字符"""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))


def nl2br(text: str) -> str:
    """换行转 <br>"""
    return text.replace('\n', '<br>')
