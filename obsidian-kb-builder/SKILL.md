---
name: obsidian-kb-builder
description: 快速构建本地知识库（Obsidian 双链图谱）。当用户输入目录 / 文档 / URL 并希望搭建或填充个人知识库、Obsidian vault、互链 markdown 笔记，或导出知识图谱数据时，使用此 skill。This skill should be used when the user wants to scaffold or populate a local personal knowledge base / Obsidian vault from files, folders, or web URLs — preserving text and images and producing interlinked ([[wikilink]]) markdown pages plus exportable graph data.
agent_created: true
---

# Obsidian KB Builder

## Overview

按 Karpathy「LLM Wiki」模式，把目录 / 文档 / URL 转化为一个**持久、互链、可复利**的本地知识库（Obsidian vault）。图谱即 Obsidian 双链图谱：节点是笔记，边是页面间的 `[[链接]]`。脚本负责机械的 I/O（建结构、抓取法、图片本地化、导出图数据），AI 负责语义抽取与互链。

## When To Use

- 用户说「建一个知识库 / 个人 wiki / Obsidian vault」「把这批文章/这个文件夹/这个网页纳入知识库」。
- 用户要从 URL、PDF、笔记批量生成互链 markdown 并保留图片。
- 用户要「导出知识图谱 / 图数据」用于可视化或导入 Neo4j / Gephi。

## Prerequisites

- 确定目标 vault 路径（用户指定；不存在则新建）。
- 访问外网时确保 `http_proxy` / `https_proxy` 环境变量已设置（fetch_source 走代理）。
- PDF / DOCX 摄入需要本机 `pandoc`（未装则脚本会提示安装）。

## Workflow

> **路径约定**：下文命令中的 `<skill>` 指本技能安装目录（如 `~/.claude/skills/obsidian-kb-builder`）。运行脚本时请将 `<skill>` 替换为实际路径，或在技能目录下执行。

### 1. 初始化（仅首次）

若 vault 不存在或缺少 `raw/`、`wiki/`、`.wiki-schema.md`，运行：

```bash
python3 <skill>/scripts/scaffold.py --vault <vault路径> [--topic "知识库主题"]
```

该脚本创建 `raw/{articles,tweets,wechat,xiaohongshu,zhihu,pdfs,notes,assets}`、`wiki/{entities,topics,sources,comparisons,synthesis}`、`.wiki-schema.md`、`index.md`、`log.md`、`purpose.md`。已存在的文件不覆盖。

### 2. 摄入每个输入（fetch_source.py）

对每个 URL 或本地文件运行：

```bash
python3 <skill>/scripts/fetch_source.py --input <URL或文件路径> --vault <vault路径> [--subdir articles]
```

- URL：经 Jina Reader 取干净 markdown；文中图片下载到 `raw/assets/`，改写为本地相对路径 `../assets/xxx`。
- 本地 .md/.txt/.html 直接处理；.pdf/.docx 用 pandoc 转换。
- 目录：遍历受支持文件，按类型选 `--subdir`（文章→articles，推文→tweets，小红书→xiaohongshu，知乎→zhihu，PDF→pdfs，笔记→notes）。
- 脚本打印写出的 `raw/.../*.md` 路径与图片统计，AI 据此继续抽取。

### 3. 语义抽取与互链（AI 执行，详见 references/workflow.md）

读取 `raw/<subdir>/<file>.md` 后：

1. 写 source 摘要页 `wiki/sources/<date>-<slug>.md`；
2. 更新 / 新建 `wiki/entities/` 与 `wiki/topics/` 页面，带 YAML frontmatter（`tags/created/updated/sources`）；
3. 在相关页面间加 `[[链接]]`，每页底部维护「相关页面」列表（**这是图数据的边，务必互链**）；
4. 更新 `index.md`（加一行 `[[页面名]] — 摘要`）；
5. 向 `log.md` 追加 `## [YYYY-MM-DD] ingest | <源标题>`。

新数据反驳旧主张时显式标注矛盾，不静默覆盖。`raw/` 只读不改，所有产物在 `wiki/`。

### 4. 查询与复利

对 wiki 提问，答案用 `[[链接]]` 引用；有价值的对比 / 分析 / 新关联存回 `wiki/comparisons/` 或 `wiki/synthesis/`，让探索也复利累积。

### 5. 导出图数据（export_graph.py）

```bash
python3 <skill>/scripts/export_graph.py --vault <vault路径> [--json]
```

输出 `graph/graph-nodes.csv`、`graph/graph-edges.csv`、`graph/graph.json`，并报告**孤儿页**（无入链）与**枢纽页**（最多入链）。CSV/JSON 可导入 Neo4j / Gephi。Obsidian 打开 vault → Graph View 即可直接可视化双链图谱。

## Graph Data

本知识库的「图数据」有两层含义，按需取用：

- **Obsidian 原生**：`[[链接]]` 即图，Graph View 直接看，无需额外导出。
- **结构化导出**：`export_graph.py` 产出节点 / 边 CSV+JSON，用于程序化图分析或导入图数据库。

## Resources

- `scripts/scaffold.py` — 初始化 vault 结构与配置文件。
- `scripts/fetch_source.py` — URL / 文档 → 规范化 markdown，图片本地化。
- `scripts/export_graph.py` — 解析全库 `[[链接]]` 导出图数据。
- `references/workflow.md` — Ingest / Query / Lint 详细流程、页面格式与命名规范。

## Notes

- 私人文件安全：仅在用户明确指定的 vault 路径下读写；不递归删除、不改动 `raw/` 原始内容。
- 图谱质量取决于 `[[链接]]` 的密度与正确性，而非页面数量——摄入时务必互链。
- `.wiki-schema.md` 是运行时配置，可随使用与用户共同演进。
