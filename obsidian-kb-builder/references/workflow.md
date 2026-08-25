# LLM Wiki 工作流详解（obsidian-kb-builder 参考）

本文件是 skill 的详细流程与规范，供执行时按需读取。核心理念见 Karpathy「LLM Wiki」：
让 LLM 作为「维基维护者」，增量构建并维护一个**持久、互链、可复利**的本地知识库，
其图谱 = Obsidian 双链图谱（节点是笔记，边是 `[[页面名]]`）。

## 一、整体流程

```
输入(目录/文档/URL)
   │
   ├─ 首次：scaffold.py 建 vault 结构 + .wiki-schema.md + index.md + log.md
   │
   ├─ 每个输入：fetch_source.py → raw/<subdir>/<date>-<slug>.md（文本+图片本地化）
   │
   ├─ Ingest（AI 执行）：读 raw 源 → 写 wiki/ 各类页面 → 页面间加 [[链接]] → 更新 index/log
   │
   ├─ Query：对 wiki 提问，答案附 [[引用]]，好答案存回 wiki
   │
   └─ Lint / 导出：export_graph.py 输出图数据；定期体检矛盾/孤儿页
```

## 二、输入处理

- **URL**：`fetch_source.py --input <url> --vault <vault>`。经 Jina Reader 取 markdown，图片下载到 `raw/assets/`。
- **本地文档**（.md/.txt/.html/.pdf/.docx）：同上，传入文件路径。pdf/docx 需要本机 `pandoc`。
- **目录**：遍历目录内所有受支持文件，逐个调用 `fetch_source.py`（按扩展名选 `--subdir`：文章→articles，推文→tweets，小红书→xiaohongshu，知乎→zhihu，PDF→pdfs，笔记→notes）。
- **图片保留**：fetch_source 会自动把文中图片落到 `raw/assets/`，并改写为本地相对路径 `../assets/xxx`，避免 URL 失效。AI 后续在 wiki 页引用图片时直接用相对路径。

## 三、Ingest（AI 抽取职责）

读取 `raw/<subdir>/<file>.md` 后，AI 应：

1. 与用户简短确认关键要点（或在批量模式直接处理）。
2. 写 **source 摘要页** `wiki/sources/<date>-<slug>.md`：一句话摘要 + 关键信息 + 链接到相关实体/主题。
3. 更新/新建 **entity 页**（`wiki/entities/`）与 **topic 页**（`wiki/topics/`）：
   - 一个源可能触动 10–15 个页面；新数据**反驳**旧主张时显式标注矛盾，不要静默覆盖。
   - 每页带 YAML frontmatter：`tags / created / updated / sources`。
4. **加 `[[链接]]`**：在相关页面间建立双向链接（这是图数据的边）。每个页面底部维护「相关页面」列表。
5. 更新 **`index.md`**：在对应类别下加一行 `[[页面名]] — 一句话摘要`。
6. 向 **`log.md`** 追加：`## [YYYY-MM-DD] ingest | <源标题>`。

页面格式示例：

```markdown
---
tags: [实体, 身份认证]
created: 2026-06-05
updated: 2026-06-05
sources: [2026-06-05-passkey入门与Go实现]
---

# Passkey

> FIDO 联盟提出的基于非对称加密的无密码身份认证凭据方案

## 关键信息
- 相关标准：[[FIDO2]]、[[WebAuthn]]、[[CTAP]]
- 提出者：[[FIDO 联盟]]

## 相关页面
- [[FIDO2]]
- [[WebAuthn]]
- [[无密码认证]]
```

## 四、Query

- 先读 `index.md` 定位相关页，再下钻具体页面。
- 答案用 `[[页面名]]` 引用来源。
- 有价值的对比/分析/新关联，存回 wiki 成为新页（如 `wiki/comparisons/` 或 `wiki/synthesis/`），让探索也复利累积。

## 五、Lint 与图数据

- **体检**：检查页间矛盾、被新源推翻的陈旧主张、孤儿页（无入链）、缺失交叉引用。
- **导出图数据**：`export_graph.py --vault <vault> [--json]` 输出 `graph/graph-nodes.csv`、`graph/graph-edges.csv`、`graph/graph.json`，并报告孤儿页与枢纽页。CSV/JSON 可导入 Neo4j / Gephi 做进一步图分析。
- **可视化**：用 Obsidian 打开 vault → Graph View（全局/局部图）即见双链图谱；开启「Tags」「Properties」作为节点更丰富。

## 六、命名与目录约定

- `raw/{articles,tweets,wechat,xiaohongshu,zhihu,pdfs,notes,assets}`
- `wiki/{entities,topics,sources,comparisons,synthesis}`
- 素材摘要：`wiki/sources/<日期>-<短标题>.md`
- 完整规范见 vault 内的 `.wiki-schema.md`（由 scaffold.py 生成，可随使用共同演进）。

## 七、常见注意点

- `raw/` 是**不可变**源，AI 只读不改；所有产物在 `wiki/`。
- 图谱质量取决于 `[[链接]]` 的密度与正确性，而非页面数量。摄入时务必互链。
- 代理：fetch_source 走 `http_proxy`/`https_proxy` 环境变量；在需要代理的网络环境（如访问外网）确保变量已设置。
- 私人文件安全：仅在用户明确指定的 vault 路径下读写；不递归删除、不改动 `raw/` 原始内容。
