# Agent Skills Collection

通用 AI Agent 技能集合 — 自动化内容创作、社交媒体管理、安全检查与生产力工具箱。

## 项目简介

本项目是一系列面向 AI 助手的 Skill（技能）模块，每个 Skill 针对特定场景提供自动化解决方案。覆盖视频处理、社交媒体运营、文章分析与创作、安全检查、翻译优化等领域。

## Skill 目录

### 📊 内容策展与分析

| Skill | 描述 | 版本 |
|-------|------|------|
| [article-deconstructor](#article-deconstructor) | 文章拆解分析器 — 10 维爆款分析 | — |
| [infocard](#infocard) | 智能信息卡片生成器 — 内容驱动布局 | v6.6 |
| [pdf2md](#pdf2md) | PDF 转 Markdown 工具 | — |
| [design-md-extractor](#design-md-extractor) | URL 设计系统提取器 | — |
| [github-analyzer](#github-analyzer) | GitHub 项目一键分析 | — |

### ✍️ 内容创作与生成

| Skill | 描述 | 版本 |
|-------|------|------|
| [wechat-article-writer](#wechat-article-writer) | 专业自媒体长文写作 | — |
| [weitoutiao-creator](#weitoutiao-creator) | 微头条短文案爆款生成器 | — |
| [snowflake-novel-writer](#snowflake-novel-writer) | 雪花写作法小说创作（10 步） | — |
| [novel-writing](#novel-writing) | LOCK 系统小说创作框架 | — |
| [image-design](#image-design) | 高级质感 AI 图片提示词设计 | — |
| [mckinsey-cover](#mckinsey-cover) | 麦肯锡风格封面/信息图生成 | — |
| [frontend-design](#frontend-design) | 高保真前端界面设计 | — |
| [curriculum-design](#curriculum-design) | 专业课程设计与教学设计 | — |
| [de-ai-writing](#de-ai-writing) | 文本去AI味五步法 | — |
| [life-quotes](#life-quotes) | 人生感悟与金句生成 | — |
| [material-to-slides](#material-to-slides) | 资料转 HTML 幻灯片 | — |
| [viral-hook](#viral-hook) | 社交媒体评论文案生成器 | v3.3 |

### 🎬 音视频处理

| Skill | 描述 | 版本 |
|-------|------|------|
| [video-minutes](#video-minutes) | 智能视频纪要生成器 | v2.0 |
| [video-dubbing](#video-dubbing) | AI 视频配音与翻译 | — |
| [mlx-tts](#mlx-tts) | Apple Silicon 本地 TTS | — |

### 🛡️ 工具与安全

| Skill | 描述 | 版本 |
|-------|------|------|
| [skill-security-check](#skill-security-check) | Skill 安装前安全检查 | — |
| [claude-simplify](#claude-simplify) | 三 Agent 并行代码审查（复用/质量/效率） | — |
| [claude-remember](#claude-remember) | 跨层级记忆管理与整理 | — |

### 🧠 学习与效率

| Skill | 描述 | 版本 |
|-------|------|------|
| [grasp](#grasp) | 十维认知框架 × 加速学习协议 — 7 阶段交互式学习 | v2 |
| [llm-aiops](#llm-aiops) | LLM + AIOps 研究参考（78+ 论文） | — |
| [hermes-setup](#hermes-setup) | Hermes Agent 全自动安装与配置 | — |

---

## Skill 详情

### grasp

**十维认知框架 × 加速学习协议** — 以10维认知框架为内容骨架，嵌入 Feynman 讲解、第一性原理拆解、主动回忆和间隔重复四种学习技术。7阶段从身份识别到进阶路径，全覆盖掌握任何知识领域。

| 阶段 | 名称 | 维度覆盖 | 核心方法 |
|------|------|---------|---------|
| 1 | Identity | 名称/类别/定义/特征 | Feynman + Teach-back |
| 2 | Anatomy | 结构/功能 | 第一性原理拆解 |
| 3 | Ecosystem | 条件/历史 | 时间线 + 条件分析 |
| 4 | Horizon | 趋势/风险 | 情景推演 + 风险审计 |
| 5 | Recall | 全10维 | 主动回忆 + 维度诊断 |
| 6 | Map | 全10维 | 一页速查 + 间隔重复 |
| 7 | Path | 全10维 | 路线图 + 行动清单 |

```bash
/grasp <topic>              # 全流程顺序
/grasp <topic> --phase=N    # 跳到指定阶段
```

[查看完整文档](grasp/SKILL.md)

---

### design-md-extractor

**URL 设计系统提取器** — 输入任意网站 URL，提取其视觉设计系统，生成符合 `@google/design.md` 规范的 DESIGN.md 文档。

- 🔗 URL 视觉分析 — 提取颜色、字体、间距、圆角、阴影等设计 Token
- 📝 符合 Spec 的输出 — YAML front matter + 8 段 Markdown
- 🧩 组件状态覆盖 — hover / focus / active 等完整状态
- ✅ 内置校验 — `npx @google/design.md lint`

参考项目：[google-labs-code/design.md](https://github.com/google-labs-code/design.md)

[查看完整文档](design-md-extractor/SKILL.md)

---

### github-analyzer

**GitHub 项目一键分析** — 分析任意 GitHub 仓库，回答项目是什么、有什么用、怎么用。

- 📖 README + 代码结构自动分析
- 📊 五章节报告：项目概述、核心亮点、技术栈、使用指南、社区活跃度

[查看完整文档](github-analyzer/SKILL.md)

---

### article-deconstructor

**文章拆解器** — 分析高流量文章的核心要素，提取结构、说服策略、情绪触发点和金句。10 个拆解维度，适用于内容分析、文案学习、对标研究。

[查看完整文档](article-deconstructor/SKILL.md)

---

### video-minutes

**智能视频纪要生成器** — 自动提取视频语音、生成字幕、智能分类总结。

- 🤖 自动分类 7 种视频类型（会议/课程/访谈/演讲/播客/教程/录屏）
- 📝 核心要点 + 行动项 + 关键决策
- 🏷️ @tags 任务分发
- 🔗 本地文件、Zoom/腾讯会议、YouTube/B站
- 🌐 99+ 语言支持

```bash
python video-minutes/scripts/generate_minutes.py meeting.mp4
python video-minutes/scripts/generate_minutes.py ~/Recordings --batch
```

[查看完整文档](video-minutes/README.md)

---

### infocard

**智能信息卡片生成器** — 从 URL 或文本提取内容，自动生成精美信息卡片图片。

核心设计理念：内容驱动布局。三个维度（密度/结构/情绪）自动选择最佳视觉形式，以"知识分享"而非"摘要"方式呈现。

配色主题（10 种）：slate / ocean / sunset / coral / indigo / forest / dark / purple / dashboard / guofeng

```bash
/infocard <URL>                       # 默认 slate 主题
/infocard <URL> --theme=ocean --lang=both
```

[查看完整文档](infocard/SKILL.md)

---

### life-quotes

**人生感悟与金句生成器** — 根据话题生成哲思/治愈/诗意/反讽/行动五种风格的哲理警句。适用视频号文案、朋友圈金句、情感共鸣内容创作。

[查看完整文档](life-quotes/SKILL.md)

---

### material-to-slides

**资料转 HTML 幻灯片** — 将任意资料阅读理解后，生成可直接播放的 HTML 幻灯片。默认纸墨印刷风格，支持 5 种配色，←/→ 键翻页。

```bash
/把这个做成PPT <URL>
```

[查看完整文档](material-to-slides/SKILL.md)

---

### viral-hook

**社交媒体评论文案生成器** — 阅读图片或文本内容，生成爆款标题 + 评论文案 + 标签。支持小红书/微博/Twitter/朋友圈，内置去AI味六步检查。

```bash
/viral-hook <文本> --platform=小红书 --style=共鸣 --count=3
```

[查看完整文档](viral-hook/SKILL.md)

---

### novel-writing

基于 **LOCK 系统 + 三幕结构 + 人物弧光** 的小说创作框架。适合快速搭建叙事骨架、塑造角色、构建跨幕情节。

[查看完整文档](novel-writing/SKILL.md)

---

### snowflake-novel-writer

使用 **雪花写作法** 的 10 步小说创作流程，从一句话概括到初稿写作。中文优先，内置反俗套检查和去AI味三遍法。

[查看完整文档](snowflake-novel-writer/SKILL.md)

---

### wechat-article-writer

**专业自媒体长文写作** — 创作公众号/小红书/知乎/头条等平台具有传播力的内容。涵盖选题分析（痛点驱动法）、12 种标题模板、4 大文章框架、情绪传播方法、低创作度合规指南。

[查看完整文档](wechat-article-writer/SKILL.md)

---

### weitoutiao-creator

**微头条短文案生成器** — 6 步工作流程：选题分析 → 素材获取 → 风格选择（5 种）→ 框架构建（10 种）→ 文案生成 → 优化迭代。300 字以内短文。

[查看完整文档](weitoutiao-creator/SKILL.md)

---

### image-design

**高级质感 AI 图片设计** — 基于摄影逻辑的 AI 图片提示词生成。五大核心维度：主体描述 + 构图位置 + 光线逻辑 + 相机视角 + 风格与质感。适用于 Midjourney、Stable Diffusion 等 AI 绘图工具。

[查看完整文档](image-design/SKILL.md)

---

### mckinsey-cover

**麦肯锡风格封面/信息图生成** — 输入主题词和用途，自动生成顶级咨询公司视觉风格的高级封面或信息图。提示词模版来自 Adrian Punk 原创。

[查看完整文档](mckinsey-cover/SKILL.md)

---

### frontend-design

**高保真前端界面设计** — 创建独特、生产级的前端界面，避免"AI 生成"的千篇一律感。大胆美学、独特字体、非对称布局、精心设计的动画。

输出：生产级 HTML/CSS/JS 或 React/Vue 代码。

[查看完整文档](.staged-skills/frontend-design/SKILL.md)

---

### de-ai-writing

**文本去AI味** — "检测→删除→声纹校准→改写→反查"五步法去除文字中的AI痕迹。11 类 AI 味检测框架，7 维度评分标准。适用于自媒体文章、职场周报、产品文案等。

[查看完整文档](de-ai-writing/SKILL.md)

---

### curriculum-design

**专业课程设计与教学设计** — 基于 OBE 成果导向 + 布鲁姆认知六层次 + 两性一度标准。双层面输出：课程级教学大纲 + 课堂级教案。适用高校教学发展、企业培训开发。

[查看完整文档](curriculum-design/SKILL.md)

---

### video-dubbing

**AI 视频配音与翻译** — 完整流水线：Demucs 分离人声 → Whisper 转录 → 精翻 → 本地 TTS 合成 → FFmpeg 合并。保持音画同步。

```bash
python video_dubbing.py input.mp4 --target-lang zh
```

[查看完整文档](video-dubbing/SKILL.md)

---

### mlx-tts

**Apple Silicon 本地 TTS** — 使用 Qwen3-TTS (MLX 框架) 在 Mac 上进行高质量本地语音合成。Prompt-based 声音设计，完全私密，无需云端。

```bash
brew install ffmpeg uv && uv tool install --force "mlx-audio" --prerelease=allow
```

[查看完整文档](mlx-tts/SKILL.md)

---

### hermes-setup

**Hermes Agent 全自动安装与配置** — 从零搭建自我进化的 AI 个人 Operator。

7 天路线：安装部署 → 身份/SOUL → 模型选择 → 记忆系统 → 消息网关 → Skills 系统 → Cron 定时 → Dashboard。

[查看完整文档](hermes-setup/skill.md)

---

### llm-aiops

**LLM + AIOps 研究参考指南** — 基于 78+ 篇论文提炼的 LLM 应用于智能运维的综合参考。覆盖故障管理、日志分析、基础设施管理三大领域，含 RCAgent、mABC 等关键系统介绍。

[查看完整文档](llm-aiops/SKILL.md)

---

## 快速开始

### 环境要求

- 通用 AI 编程助手
- 部分 Skill 需要 Python 3.8+ / Node.js 14+ / FFmpeg

### 常用依赖

```bash
# video-minutes / video-dubbing
brew install ffmpeg          # macOS
sudo apt install ffmpeg      # Ubuntu

# mlx-tts (Apple Silicon only)
brew install ffmpeg uv && uv tool install --force "mlx-audio" --prerelease=allow
```

---

## 项目结构

```
agent-skills/
├── README.md
├── LICENSE
│
├── article-deconstructor/        # 文章拆解分析
├── grasp/                        # 十维认知 × 加速学习协议 v2
├── claude-remember/              # 记忆管理与整理
├── claude-simplify/              # 代码简化与质量检查
├── curriculum-design/            # 专业课程设计
├── de-ai-writing/                # 文本去AI味
├── design-md-extractor/          # URL 设计系统提取器
├── github-analyzer/              # GitHub 项目分析
├── hermes-setup/                 # Hermes Agent 安装配置
├── image-design/                 # AI 图片提示词设计
├── infocard/                     # 信息卡片生成器 v6.6
├── life-quotes/                  # 人生感悟与金句
├── llm-aiops/                    # LLM + AIOps 研究参考
├── material-to-slides/           # 资料转 HTML 幻灯片
├── mckinsey-cover/               # 麦肯锡风格封面生成
├── mlx-tts/                      # Apple Silicon 本地 TTS
├── novel-writing/                # LOCK 系统小说创作
├── pdf2md/                       # PDF 转 Markdown
├── skill-security-check/         # Skill 安全检查
├── snowflake-novel-writer/       # 雪花写作法小说创作
├── video-dubbing/                # AI 视频配音
├── video-minutes/                # 视频纪要生成器
├── viral-hook/                   # 社交媒体文案生成器
├── wechat-article-writer/        # 自媒体长文写作
├── weitoutiao-creator/           # 微头条短文案生成器
│
└── .staged-skills/               # 待发布技能
    └── frontend-design/          # 高保真前端界面设计
```

---

### Skill 文档规范

每个 Skill 应包含：
- **SKILL.md** — 完整使用文档（必需）
- **scripts/** — 执行脚本（如有代码）
- **references/** — 参考资料（可选）

---

## 贡献指南

1. 每个 Skill 包含完整的 SKILL.md 文档
2. 遵循现有目录结构和命名规范
3. 在 README 目录和项目结构中添加新 Skill
4. 脚本型 Skill 提供安装和配置说明

---

## 许可证

MIT — 详见 [LICENSE](LICENSE)

---

## 最近更新

### 2026-07-27 — grasp v2 重构

- **grasp 重构**: 原 blitz 更名为 grasp，以十维认知框架为核心骨架重构 7 个学习阶段
  - Phase 1-4 依次覆盖 10 个认知维度（名称/类别/定义/特征 → 结构/功能 → 条件/历史 → 趋势/风险）
  - Phase 5-7 产出：维度诊断矩阵 → 知识地图 + 间隔重复 → 进阶路线 + 行动清单
  - 保留全部学习科学技术（Feynman、第一性原理、主动回忆、间隔重复），嵌入维度而非作为独立阶段
  - 调用方式：`/grasp <topic> [--phase=N]`

### 2026-07-25 — 全量巡视与批量优化

- **缺陷修复**: pdf2md 残留代码片段、video-minutes 重复"依赖安装"章节
- **路径通用化**: 所有 Skill 中硬编码的平台路径（`~/.claude/skills/`、`.opencode/skills/`）统一为工作区��对路径
- **记忆体系通用化**: claude-remember 改为通用记忆层级描述，不绑定特定平台的记忆文件路径
- **交叉引用**: 为重叠技能对添加互引（de-ai-writing↔viral-hook, novel-writing↔snowflake-novel-writer, wechat-article-writer↔weitoutiao-creator）
- **能力增强**: image-design 添加原生图片生成工具说明；pdf2md 添加原生 PDF 读取备选方案；video-minutes 添加多模态视频理解备选方案
- **README 重写**: 清理已删除技能，补齐缺失条目，统一格式，去除所有平台特定引用

---

> 每个 Skill 都是独立的模块，可单独使用。建议先阅读各 Skill 的 SKILL.md 了解详细功能。
