"""
AI文本概括器 - 用于提炼段落中心思想和生成主题标题
"""

import re
from typing import List, Optional


def extract_main_idea(paragraph: str) -> str:
    """
    提取段落中心思想
    策略：
    1. 识别主题句（通常在段首或段尾）
    2. 提取关键词组合
    3. 生成简洁的概括句
    """
    if not paragraph or len(paragraph.strip()) < 20:
        return paragraph.strip() if paragraph else ""

    # 清理文本
    text = paragraph.strip()

    # 分割成句子
    sentences = re.split(r'(?<=[。！？.!?])\s*', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return text[:50]

    # 策略1：如果第一句包含核心关键词，使用它
    first_sentence = sentences[0]

    # 识别核心关键词（名词、动词短语）
    keywords = extract_keywords_from_text(text)

    # 如果第一句较短且包含关键词，使用它
    if len(first_sentence) < 80 and any(kw in first_sentence for kw in keywords[:3]):
        return clean_sentence(first_sentence)

    # 策略2：组合关键信息生成概括
    # 提取谁/什么 + 做了什么/怎么样
    summary = generate_summary_from_keywords(text, keywords)

    if summary and len(summary) > 10:
        return summary

    # 策略3：回退到第一句
    return clean_sentence(first_sentence[:80])


def extract_keywords_from_text(text: str) -> List[str]:
    """提取关键词"""
    # 清理文本
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', ' ', text)

    # 中文关键词模式（2-6字词组）
    words = []

    # 提取潜在的技术术语、名词短语
    patterns = [
        r'[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*',  # 英文术语
        r'[a-z]+_[a-z_]+',  # snake_case 变量
        r'[\u4e00-\u9fa5]{2,6}(?:工具|系统|方法|模式|机制|策略|原理|概念)',  # 中文术语
        r'(?:如何|为什么|什么|怎么)[\u4e00-\u9fa5]{2,8}',  # 问题型
        r'[\u4e00-\u9fa5]{2,4}(?:问题|错误|异常|风险|挑战)',  # 问题型
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        words.extend(matches)

    # 统计词频
    word_freq = {}
    for word in words:
        if len(word) > 1:
            word_freq[word] = word_freq.get(word, 0) + 1

    # 按频率排序
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    return [w for w, _ in sorted_words[:10]]


def generate_summary_from_keywords(text: str, keywords: List[str]) -> str:
    """基于关键词生成概括句"""
    if not keywords:
        return ""

    # 查找包含最多关键词的句子
    sentences = re.split(r'(?<=[。！？.!?])\s*', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    best_sentence = ""
    best_score = 0

    for sentence in sentences:
        if len(sentence) < 20 or len(sentence) > 150:
            continue

        score = sum(1 for kw in keywords if kw in sentence)
        if score > best_score:
            best_score = score
            best_sentence = sentence

    return clean_sentence(best_sentence) if best_sentence else ""


def clean_sentence(sentence: str) -> str:
    """清理句子，移除不必要的修饰"""
    # 移除开头的连接词
    prefixes = ['首先，', '其次，', '然后，', '最后，', '同时，', '此外，', '例如，', '比如，']
    for prefix in prefixes:
        if sentence.startswith(prefix):
            sentence = sentence[len(prefix):]

    # 移除例句（包含"例如"、"比如"的句子）
    if '例如' in sentence or '比如' in sentence or '如' in sentence[:10]:
        # 尝试提取主要部分
        parts = re.split(r'[，。]?(?:例如|比如|如)', sentence)
        if parts and len(parts[0]) > 15:
            sentence = parts[0]

    return sentence.strip()


def generate_title_from_content(content: str, max_length: int = 25) -> str:
    """
    从内容生成标题
    不是简单提取，而是提炼中心思想
    """
    main_idea = extract_main_idea(content)

    if not main_idea:
        return "内容概述"

    # 如果已经很短，直接返回
    if len(main_idea) <= max_length:
        return main_idea

    # 否则需要压缩
    # 策略：提取主谓宾结构
    compressed = compress_to_title(main_idea, max_length)

    return compressed if compressed else main_idea[:max_length]


def compress_to_title(sentence: str, max_length: int) -> str:
    """将句子压缩成标题长度"""
    # 移除修饰成分
    # 移除"的"字短语
    compressed = re.sub(r'[\u4e00-\u9fa5]+的', '', sentence)

    # 如果压缩后太短，回退
    if len(compressed) < 10:
        compressed = sentence

    # 截取到合适长度，确保在语义边界
    if len(compressed) > max_length:
        # 找最后一个动词或名词
        truncated = compressed[:max_length]
        # 尝试在标点处截断
        last_punct = max(truncated.rfind('，'), truncated.rfind('、'))
        if last_punct > max_length * 0.6:
            compressed = truncated[:last_punct]
        else:
            compressed = truncated

    return compressed.strip('，、。 ')


def summarize_paragraphs(paragraphs: List[str], max_points: int = 3) -> List[str]:
    """
    概括多个段落，生成要点
    """
    summaries = []

    for para in paragraphs:
        if not para.strip():
            continue

        summary = extract_main_idea(para)
        if summary and len(summary) > 10:
            summaries.append(summary)

        if len(summaries) >= max_points:
            break

    return summaries


# 使用示例
if __name__ == "__main__":
    test_text = """
    在 Hermes 的 delegate_task 模式下，父 agent 像项目经理一样，将任务拆解后分发给子 agent，
    然后阻塞等待所有结果返回。这种模式的优势在于简单直观，
    但缺点是父 agent 必须等待所有子任务完成才能继续，导致整体执行时间较长。
    """

    title = generate_title_from_content(test_text)
    print(f"Generated title: {title}")

    main_idea = extract_main_idea(test_text)
    print(f"Main idea: {main_idea}")
