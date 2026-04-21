from __future__ import annotations

import json
import urllib.parse
import urllib.request

from ..utils.text import clamp_text, detect_language


def _fetch_json(url: str) -> object:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "deck-to-pptx/0.1"},
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def _fetch_wikipedia_summary(topic: str, language: str) -> str:
    base = "zh" if language == "zh" else "en"
    query = urllib.parse.quote(topic)

    search_url = (
        f"https://{base}.wikipedia.org/w/api.php"
        f"?action=opensearch&search={query}&limit=1&namespace=0&format=json"
    )
    search_result = _fetch_json(search_url)

    if not isinstance(search_result, list) or len(search_result) < 2 or not search_result[1]:
        return ""

    page_title = urllib.parse.quote(search_result[1][0])
    summary_url = f"https://{base}.wikipedia.org/api/rest_v1/page/summary/{page_title}"
    summary_result = _fetch_json(summary_url)

    if isinstance(summary_result, dict):
        return summary_result.get("extract", "") or ""
    return ""


def _fallback_markdown(topic: str, language: str) -> str:
    if language == "zh":
        return (
            f"# {topic}\n\n"
            f"围绕“{topic}”整理一份结构清晰、适合演示的说明。\n\n"
            "## 为什么现在要关注\n"
            f"{topic} 正在从零散尝试走向系统化落地，组织需要更稳定的表达和交付方式。\n\n"
            "## 当前最常见的阻塞\n"
            "- 信息散落在多种资料中\n"
            "- 内容能总结，但很难直接变成可演示页面\n"
            "- 演示稿经常在结构、节奏和视觉上失真\n\n"
            "## 推荐的工作流\n"
            "- 先统一资料来源\n"
            "- 再抽取演示主张和页面顺序\n"
            "- 最后选择匹配页面角色的版式输出\n\n"
            "## 落地建议\n"
            "- 先做一版高信号样稿\n"
            "- 评审后再追加细节和视觉资产\n"
            "- 用统一模板保持后续输出稳定\n"
        )

    return (
        f"# {topic}\n\n"
        f"A concise presentation-ready explanation of {topic}.\n\n"
        "## Why it matters\n"
        f"{topic} is easier to understand when the material is compressed into a clear presentation sequence.\n\n"
        "## Common friction\n"
        "- Source material is fragmented\n"
        "- Notes rarely map cleanly to slide structure\n"
        "- Visual quality drops during last-mile conversion\n\n"
        "## Recommended workflow\n"
        "- Normalize the material first\n"
        "- Build a page-level narrative next\n"
        "- Render with a limited but strong layout system\n\n"
        "## Next actions\n"
        "- Ship one strong sample deck first\n"
        "- Review structure before polishing details\n"
        "- Keep the output pipeline repeatable\n"
    )


def research_topic_markdown(topic: str, language: str = "auto") -> str:
    chosen_language = detect_language(topic) if language == "auto" else language

    try:
        summary = _fetch_wikipedia_summary(topic, chosen_language)
    except Exception:
        summary = ""

    if not summary:
        return _fallback_markdown(topic, chosen_language)

    trimmed = clamp_text(summary, 800)
    if chosen_language == "zh":
        return (
            f"# {topic}\n\n"
            f"{trimmed}\n\n"
            "## 核心背景\n"
            f"{trimmed[:180]}\n\n"
            "## 主要问题\n"
            "- 资料难以直接组织成演示逻辑\n"
            "- 单页经常堆满信息，缺少主张\n"
            "- 输出格式与表达节奏不一致\n\n"
            "## 可执行做法\n"
            "- 先抽取主题和关键章节\n"
            "- 再把章节压成页面主张\n"
            "- 最后映射到有限版式系统\n"
        )

    return (
        f"# {topic}\n\n"
        f"{trimmed}\n\n"
        "## Core context\n"
        f"{trimmed[:180]}\n\n"
        "## Main issues\n"
        "- Raw material does not map cleanly to slides\n"
        "- Pages lose their single point\n"
        "- Delivery quality drifts across formats\n\n"
        "## Practical route\n"
        "- extract the narrative first\n"
        "- compress each section into a slide thesis\n"
        "- render through a limited layout system\n"
    )
