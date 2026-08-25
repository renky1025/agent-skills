# Agent Skills Collection

通用 AI Agent 技能集合 —— 内容创作、代码工程、知识学习、媒体处理与智能体配置的生产力工具箱。

## 治理约定（阅读前必读）

- **仓库即唯一真源**：本仓库的目录树是技能清单的权威来源。新增 / 删除技能必须同步本文件与目录结构。
- **运行时依赖（未含于快照）**：`viral-hook`、`translate-polisher` 在 WorkBuddy 运行环境中已安装，但不在本仓库快照内。引用它们的技能（如 `infocard` 双语模式、`wechat-article-writer`）在缺失时自动降级，不会断链。
- **质量治理（2026-08-25 一轮治理）**：`skill-security-check`、`infocard`、`github-analyzer`、`pdf2md`、`video-minutes`、`wechat-article-writer`、`edulab`、`hermes-setup` 八个原待修技能已完成修复，统一为标杆级（详见文末「最近更新」）。

## 技能总览

当前共 **27** 个顶层技能，按领域分组如下。质量标注：⭐ = 标杆（5/5），✅ = 良好（4/5），🔧 = 本轮治理达标。

### ✍️ 写作与内容创作

| 技能 | 一句话说明 | 质量 |
|------|-----------|------|
| [de-ai-writing](de-ai-writing/SKILL.md) | 文本去 AI 味五步法，11 类 AI 味检测，唯一真源 | ⭐ |
| [snowflake-novel-writer](snowflake-novel-writer/SKILL.md) | 雪花写作法 10 步小说创作，中文优先，内置反俗套 | ⭐ |
| [curriculum-design](curriculum-design/SKILL.md) | OBE + 布鲁姆六层次，课程大纲与教案双模板 | ⭐ |
| [novel-writing](novel-writing/SKILL.md) | LOCK 系统 + 三幕结构小说创作框架（快速骨架） | ✅ |
| [wechat-article-writer](wechat-article-writer/SKILL.md) | 专业自媒体长文写作（选题/标题/框架/情绪/低创作度） | 🔧 |
| [weitoutiao-creator](weitoutiao-creator/SKILL.md) | 微头条短文案爆款生成器，6 步 + 5 风格 + 10 框架 | ✅ |
| [black-humor-writing](black-humor-writing/SKILL.md) | 黑色幽默五步 SOP，区分度清晰 | ✅ |
| [article-deconstructor](article-deconstructor/SKILL.md) | 文章 10 维拆解，结构/说服/情绪/金句分析 | ✅ |

### 🛠 代码与工程

| 技能 | 一句话说明 | 质量 |
|------|-----------|------|
| [claude-simplify](claude-simplify/SKILL.md) | 三 Agent 并行代码审查（复用 / 质量 / 效率） | ⭐ |
| [clean-code](clean-code/SKILL.md) | 17 章代码质量知识库 + 索引 + 跨语言映射 | ⭐ |
| [skill-security-check](skill-security-check/SKILL.md) | Skill 安装前多语言安全检查（11 项 + CLI） | 🔧 |
| [design-md-extractor](design-md-extractor/SKILL.md) | URL 设计系统提取，生成 DESIGN.md 规范 | ✅ |
| [github-analyzer](github-analyzer/SKILL.md) | GitHub 项目一键分析（README 驱动五章节报告） | 🔧 |

### 🧠 知识与学习

| 技能 | 一句话说明 | 质量 |
|------|-----------|------|
| [grasp](grasp/SKILL.md) | 十维认知框架 × 加速学习协议，7 阶段交互式学习 | ⭐ |
| [teach-eli5](teach-eli5/SKILL.md) | 给小白讲明白：MISSION 锚定 + 自包含教学 HTML（图多字少） | ✅ |
| [obsidian-kb-builder](obsidian-kb-builder/SKILL.md) | Karpathy Wiki 模式知识库，双链图谱 + 图数据导出 | 🔧 |
| [claude-remember](claude-remember/SKILL.md) | 跨记忆层级整理与管理 | ✅ |
| [llm-aiops](llm-aiops/SKILL.md) | LLM + AIOps 研究参考（78+ 论文） | ✅ |
| [edulab](edulab/SKILL.md) | 中高考数学可视化：3D 解题演示 + 函数图形联动 | 🔧 |

### 🎬 媒体处理

| 技能 | 一句话说明 | 质量 |
|------|-----------|------|
| [video-minutes](video-minutes/SKILL.md) | 智能视频纪要，行动项 @tags 分发（可选降级） | 🔧 |
| [video-dubbing](video-dubbing/SKILL.md) | AI 视频配音翻译：人声分离 → 转录 → 精翻 → TTS | ✅ |
| [pdf2md](pdf2md/SKILL.md) | 高精度 PDF 转 Markdown（OpenDataLoader PDF） | 🔧 |
| [mlx-tts](mlx-tts/SKILL.md) | Apple Silicon 本地 TTS（Qwen3-TTS / MLX） | ✅ |
| [image-design](image-design/SKILL.md) | 摄影逻辑驱动的 AI 图片提示词设计 | ✅ |
| [mckinsey-cover](mckinsey-cover/SKILL.md) | 麦肯锡风格封面 / 信息图生成 | ✅ |
| [infocard](infocard/SKILL.md) | 内容驱动的信息卡片图片生成（10 主题） | 🔧 |

### 🤖 智能体

| 技能 | 一句话说明 | 质量 |
|------|-----------|------|
| [hermes-setup](hermes-setup/SKILL.md) | Hermes Agent 全自动安装与配置（7 天路线） | 🔧 |

---

## 项目结构

```
agent-skills/
+-- README.md
+-- LICENSE
+-- SKILLS-UPGRADE-AUDIT.md        # 升级优化审计报告（2026-08-25）
|
+-- article-deconstructor/         # 文章 10 维拆解
+-- black-humor-writing/           # 黑色幽默五步 SOP
+-- clean-code/                    # 代码质量知识库（17 章）
+-- claude-remember/               # 跨层级记忆管理
+-- claude-simplify/               # 三 Agent 并行代码审查
+-- curriculum-design/             # 专业课程设计
+-- de-ai-writing/                 # 文本去 AI 味（唯一真源）
+-- design-md-extractor/           # URL 设计系统提取
+-- edulab/                        # 中高考数学可视化
+-- github-analyzer/               # GitHub 项目分析
+-- grasp/                         # 十维认知 × 加速学习
+-- hermes-setup/                  # Hermes Agent 安装配置
+-- image-design/                  # AI 图片提示词设计
+-- infocard/                      # 信息卡片生成器
+-- llm-aiops/                     # LLM + AIOps 研究参考
+-- mckinsey-cover/                # 麦肯锡风格封面生成
+-- mlx-tts/                       # Apple Silicon 本地 TTS
+-- novel-writing/                 # LOCK 系统小说创作
+-- obsidian-kb-builder/           # Karpathy Wiki 知识库
+-- pdf2md/                        # PDF 转 Markdown
+-- skill-security-check/          # Skill 安全检查
+-- snowflake-novel-writer/        # 雪花写作法小说创作
+-- teach-eli5/                    # 给小白讲明白（教学 HTML 引擎）
+-- video-dubbing/                 # AI 视频配音
+-- video-minutes/                 # 视频纪要生成器
+-- weitoutiao-creator/            # 微头条短文案生成器
+-- wechat-article-writer/         # 自媒体长文写作
```

---

## Skill 文档规范

每个 Skill 应包含：
- **SKILL.md** — 完整使用文档（必需）
- **scripts/** — 执行脚本（如有代码）
- **references/** — 参考资料（可选）

## 安装基路径约定

- 全库统一基路径：`~/.workbuddy/skills/<skill>/`
- 脚本内一律用相对路径或运行时参数，禁止写死 `/Users/<user>/...`
- 外部依赖（pandoc / ffmpeg / mlx-audio / Java 等）在 Prerequisites 段统一声明
- 代理：统一读取 `https_proxy` / `http_proxy` 环境变量，不写死具体地址

## 快速开始

### 环境要求

- 通用 AI 编程助手（WorkBuddy / Claude Code 等）
- 部分 Skill 需要 Python 3.10+ / Node.js / FFmpeg / Java 11+

### 常用依赖

```bash
# 视频 / 媒体类
brew install ffmpeg          # macOS
sudo apt install ffmpeg      # Ubuntu

# mlx-tts（Apple Silicon only）
brew install ffmpeg uv && uv tool install --force "mlx-audio" --prerelease=allow

# pdf2md
pip install "opendataloader-pdf[hybrid]"
```

---

## 最近更新

### 2026-08-25 — 全量治理与标杆化

- **统一基路径**：`infocard` 的 `~/.claude/skills` → `~/.workbuddy/skills`；`video-minutes` 的 `~/.ai-agent/skills` → `~/.workbuddy/skills`；`edulab` / `obsidian-kb-builder` 去除 `/Users/kyren` 绝对路径，统一为 `~`。
- **可移植性**：`github-analyzer` 写死代理 `127.0.0.1:7890` → 读取 `https_proxy`/`http_proxy` 环境变量（缺失直连）。
- **启用与降级**：`wechat-article-writer` 移除 `disable: true` 重新启用，缺失的 `viral-hook` 标注为运行时依赖；`infocard` 双语模式标注 `translate-polisher` 运行时依赖（缺失降级为内部直译）。
- **文档与实现对齐**：`skill-security-check` 补全 `scripts/security-check.js` / `src/` 入口；`pdf2md` 删除与 `pdf2md.py` 重复的 380 行伪代码，改为调用脚本。
- **去重（单一真源）**：`de-ai-writing` 定为去 AI 味唯一真源，`snowflake-novel-writer`、`wechat-article-writer` 的内嵌副本加溯源声明并保持同步。
- **分发降级**：`video-minutes` 任务分发系统的 7 个缺失兄弟技能改为可选，不可用时降级为本地 TODO 清单。
- **文件规范**：`hermes-setup/skill.md` 重命名为 `SKILL.md`（大小写敏感 FS 可识别）；删除 `infocard/capture_dsh.js` 死文件。
- **导航**：`novel-writing` ↔ `snowflake-novel-writer`、`obsidian-kb-builder` 的 `<skill>` 占位符加使用说明。
- **README 重写**：与 26 个实际目录严格对齐，补齐 `black-humor-writing` / `clean-code` / `edulab` / `obsidian-kb-builder`，移除仓库不存在的 `frontend-design` / `life-quotes` / `material-to-slides` / `viral-hook` 条目。

### 2026-08-25 — teach-eli5 重构

- **融合 mattpocock `teach` 方法论**：从 1 行 stub 升级为多文件技能（SKILL.md + references/{MISSION,LESSON,LEARNING-RECORD}-FORMAT.md + assets/base.css）。MISSION 锚定目标、ZPD 最近发展区选材、每课一个自包含精美 HTML、复用组件库、术语表与学习记录沉淀；叠加 eli5 小白约束（图多字少、先类比后精确、禁行话、可离线）。
- 计入顶层技能总数，目录对齐更新为 27 个。

### 2026-07-27 — grasp v2 重构

- grasp 更名重构：以十维认知框架为核心骨架，7 阶段交互式学习；调用 `/grasp <topic> [--phase=N]`。

### 2026-07-25 — 全量巡视与批量优化

- 缺陷修复、路径通用化、记忆体系通用化、交叉引用、能力增强、README 重写。

---

> 每个 Skill 都是独立模块，可单独使用。建议先阅读各 Skill 的 SKILL.md 了解详细功能。
