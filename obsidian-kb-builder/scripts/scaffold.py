#!/usr/bin/env python3
"""scaffold.py — 初始化一个 LLM Wiki 风格的本地知识库（Obsidian vault）。

用法:
  python3 scaffold.py --vault /path/to/vault [--topic "我的知识库"]

在 vault 下创建:
  raw/{articles,tweets,wechat,xiaohongshu,zhihu,pdfs,notes,assets}/
  wiki/{entities,topics,sources,comparisons,synthesis}/
  .wiki-schema.md  index.md  log.md  purpose.md

幂等：已存在的目录/文件跳过，不覆盖用户数据。
"""
import argparse
import os
import datetime

SCHEMA_MD = """# Wiki Schema（知识库配置规范）

> 本文件告诉 AI 如何维护这个本地知识库（LLM Wiki 模式）。你与 AI 可共同调整它。

## 知识库信息

- 主题：（由创建者填写）
- 创建日期：{date}
- 语言：中文
- 版本：1.0

## 目录结构

```
<vault>/
├── raw/                    # 原始素材（AI 只读，不会修改）
│   ├── articles/           # 网页文章
│   ├── tweets/             # X / Twitter 内容
│   ├── wechat/             # 微信公众号文章
│   ├── xiaohongshu/        # 小红书内容
│   ├── zhihu/              # 知乎内容
│   ├── pdfs/               # PDF 文件
│   ├── notes/              # 手写笔记
│   └── assets/             # 图片等附件（fetch_source.py 自动下载到这里）
├── wiki/                   # 知识库主体（AI 写，你看）
│   ├── entities/           # 实体页（人物、组织、概念、技术）
│   ├── topics/             # 主题页（研究主题、知识领域）
│   ├── sources/            # 素材摘要页（每个素材一篇摘要）
│   ├── comparisons/        # 对比分析页
│   └── synthesis/          # 综合分析页
├── index.md                # 内容索引（目录）
├── log.md                  # 操作日志（时间线）
└── .wiki-schema.md         # 本文件（配置规范）
```

## 页面命名规范

- 实体页：`wiki/entities/{{名称}}.md`（例：`Transformer.md`、`知识构建.md`）
- 主题页：`wiki/topics/{{主题名}}.md`（例：`AI编程工具.md`）
- 素材摘要：`wiki/sources/{{日期}}-{{短标题}}.md`（例：`2026-04-05-karpathy-llm-wiki.md`）
- 对比分析：`wiki/comparisons/{{对比主题}}.md`
- 综合分析：`wiki/synthesis/{{分析主题}}.md`

## 交叉引用规范（图数据来源）

- 页面间使用 `[[页面名]]` 语法（Obsidian 兼容双向链接）。**这些链接即图数据的边。**
- 素材引用格式：`[来源: 标题](../sources/xxx.md)`
- 每个页面底部维护「相关页面」列表，确保页面互联而非孤立。

## 页面格式规范

每个 wiki 页面建议包含：

```markdown
---
tags: [标签1, 标签2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [关联素材列表]
---

# 页面标题

> 一句话摘要

## 正文内容

## 相关页面

- [[另一个页面]]
- [[又一个页面]]
```

## 操作流程

- **Ingest（摄入）**：把素材放入 `raw/` → AI 读取 → 写 source 摘要页 → 更新相关 entity/topic 页 → 在页面间加 `[[链接]]` → 更新 `index.md` 与 `log.md`。
- **Query（查询）**：对 wiki 提问，答案附 `[[链接]]` 引用；有价值的答案存回 wiki 成为新页。
- **Lint（体检）**：检查矛盾、陈旧主张、孤儿页（无入链）、缺失交叉引用。可用 `export_graph.py` 输出节点/边并定位孤儿与枢纽。

## 图数据

本知识库的图 = Obsidian 双链图谱：节点是笔记，边是 `[[页面名]]`。直接用 Obsidian 打开 vault 点 Graph View 即可可视化。运行 `export_graph.py` 可导出结构化节点/边（CSV/JSON）供 Neo4j / Gephi 等使用。
"""

INDEX_MD = """# 知识库索引

> 内容总目录。每次 Ingest 后由 AI 更新。查询时先读本文件定位相关页，再下钻。
> 按类别组织，每页一行摘要 + 链接。

## 实体（Entities）
<!-- 人物 / 组织 / 概念 / 技术 -->

## 主题（Topics）
<!-- 研究主题 / 知识领域 -->

## 素材来源（Sources）
<!-- 每个原始素材一篇摘要 -->
"""

LOG_MD = """# 知识库日志

> 时序操作日志（append-only）。每条统一前缀 `## [YYYY-MM-DD] <动作> | <标题>`。
> 解析最近 5 条：`grep "^## \\[" log.md | tail -5`

## [{date}] init | 知识库初始化
- 建立 raw/ 与 wiki/ 目录，写入 .wiki-schema.md、index.md、log.md。
"""

PURPOSE_MD = """# 知识库目的

> 用一两句话写清这个知识库服务什么目标、覆盖哪些领域、给谁用。
> 例：收集并结构化我在 AI 编程工具链、后端架构、流体力学方面的学习与素材，便于长期检索与综合。
"""


def makedirs(path, created):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
        created.append(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True, help="知识库（vault）根目录路径")
    ap.add_argument("--topic", default="", help="知识库主题（写入 purpose.md，可选）")
    args = ap.parse_args()

    vault = os.path.abspath(args.vault)
    today = datetime.date.today().isoformat()
    created = []

    # raw 子目录
    raw_dirs = ["articles", "tweets", "wechat", "xiaohongshu", "zhihu", "pdfs", "notes", "assets"]
    for d in raw_dirs:
        makedirs(os.path.join(vault, "raw", d), created)
    # wiki 子目录
    wiki_dirs = ["entities", "topics", "sources", "comparisons", "synthesis"]
    for d in wiki_dirs:
        makedirs(os.path.join(vault, "wiki", d), created)

    # 配置文件（仅在不存在时写入，避免覆盖用户已演进的 schema）
    schema_path = os.path.join(vault, ".wiki-schema.md")
    if not os.path.exists(schema_path):
        with open(schema_path, "w", encoding="utf-8") as f:
            f.write(SCHEMA_MD.format(date=today))
        created.append(schema_path)

    index_path = os.path.join(vault, "index.md")
    if not os.path.exists(index_path):
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(INDEX_MD)
        created.append(index_path)

    log_path = os.path.join(vault, "log.md")
    if not os.path.exists(log_path):
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(LOG_MD.format(date=today))
        created.append(log_path)

    purpose_path = os.path.join(vault, "purpose.md")
    if not os.path.exists(purpose_path):
        content = PURPOSE_MD
        if args.topic:
            content = f"# 知识库目的\n\n主题：{args.topic}\n\n> 用一两句话写清这个知识库服务什么目标、覆盖哪些领域、给谁用。\n"
        with open(purpose_path, "w", encoding="utf-8") as f:
            f.write(content)
        created.append(purpose_path)

    print(f"vault: {vault}")
    print(f"created_items: {len(created)}")
    for c in created:
        print(f"  + {os.path.relpath(c, vault)}")
    print("done: scaffold ready. 用 Obsidian 打开 vault 即可看到空结构；运行 fetch_source.py 摄入素材。")


if __name__ == "__main__":
    main()
