# Agent Skills: 工业级 AI Agent 技能生态库

面向下一代自主 Agent 与开发者协作系统（Claude Code、Codex、Cursor 等）的生产级开源技能集（Agent Skills）。全量模块采用标准化 `SKILL.md` 契约体系与结构化上下文传递设计，提供从内容创作、多媒体音视频工程、代码研发与安全审计，到认知学习与智能知识库管理的一站式可复用能力。

---

## 核心设计与工程原则

1. **契约化上下文传递 (Contract-Based Context Passing)**：每个 Skill 均定义明确的输入边界、产出契约（Outcome Contract）与完成标准（Done When），拒绝模糊盲注，确保多 Agent 协作时状态确定。
2. **纯净规范与跨平台安全 (Zero-Garble & Pure ASCII Guarantee)**：文档与生成管道严守纯 ASCII 字符结构规范，杜绝特殊制表符引发的字符编码异常（`U+FFFD` / 乱码）。
3. **单一真源与分层复用 (Single Source of Truth)**：通用能力（如 `de-ai-writing` 反 AI 腔调算法）沉淀为唯一真源，上层业务 Skill 引用而非重复硬编码。
4. **渐进式降级 (Graceful Degradation)**：依赖外部可选插件或环境服务的技能，均提供完善的本地替代路径与确定性回退方案。

---

## 仓库结构全景

```
agent-skills/
+-- README.md                         # 权威架构与使用指南
+-- LICENSE                           # 开源许可证
+-- SKILLS-UPGRADE-AUDIT.md           # 架构审计与治理报告
|
+-- [内容创作与自媒体]
|   +-- article-deconstructor/        # 爆款文章 10 维结构解构器
|   +-- black-humor-writing/          # 单立人黑色幽默五步创作法
|   +-- de-ai-writing/                # 通用文本去 AI 味与活人声纹校准 (唯一真源)
|   +-- novel-writing/                # 基于 LOCK 系统的叙事小说骨架
|   +-- snowflake-novel-writer/       # 雪花写作法 10 步逐层精细长篇创作
|   +-- wechat-article-writer/        # 微信公众号与自媒体长文爆款创作流
|   +-- weitoutiao-creator/           # 微头条短文案 6 步爆款生成器
|
+-- [多媒体与音视频工程]
|   +-- image-design/                 # 摄影学五维 AI 绘图提示词生成器
|   +-- infocard/                     # 高清自适应现代信息卡片渲染引擎
|   +-- mckinsey-cover/               # 麦肯锡与顶级咨询风研报封面生成器
|   +-- mlx-tts/                      # Apple Silicon (MLX) 本地极速语音合成
|   +-- video-dubbing/                # 视频翻译、AI 语音克隆配音与字幕压制
|   +-- video-minutes/                # 智能视频纪要生成与 @tags 任务分发
|
+-- [代码工程与研发安全]
|   +-- agent-coding-style/           # Coding Agent 确定性回答与操作规范
|   +-- claude-simplify/              # 三 Agent 并行代码审查与精简流水线
|   +-- clean-code/                   # 《Clean Code》17 章全书知识体系与重构指南
|   +-- design-md-extractor/          # Web 视觉设计系统逆向提取器 (DESIGN.md)
|   +-- github-analyzer/              # GitHub 仓库极速 5 维解构报告生成器
|   +-- jira-server-pat-cli/          # Jira Server/Data Center 通用管理 CLI
|   +-- llm-aiops/                    # 大模型 AIOps 运维与根因定位研究参考库
|   +-- skill-security-check/         # Agent Skill 11 项静态漏洞与安全审计器
|
+-- [认知学习与教育实验室]
|   +-- curriculum-design/            # OBE 成果导向与布鲁姆认知模型课程设计
|   +-- edulab/                       # 中高考数学可视化解题 (3D 几何 + 2D 函数联动)
|   +-- grasp/                        # 十维认知框架 x 费曼加速学习协议
|   +-- teach-eli5/                   # Matt Pocock 教学法小白友好自包含课件生成器
|
+-- [知识库与记忆管理]
    +-- claude-remember/              # 多层级 AI Agent 长期记忆审查与归档
    +-- obsidian-kb-builder/          # Karpathy LLM-Wiki 本地双链 Obsidian 知识库
    +-- pdf2md/                       # 高精度学术与工业 PDF 转 Markdown 引擎
```

---

## 技能全景矩阵 (Skill Catalog)

| 技能名称 | 分类 | 核心定位与功能 | 交互命令 / 触发关键词 | 依赖环境 |
|---|---|---|---|---|
| **de-ai-writing** | 写作 | 36 种 AI 腔调模式检测、3 层词汇过滤、5 步活人声纹校准 | `/de-ai`, 去AI味, 人味改写 | 无 |
| **wechat-article-writer** | 写作 | 痛点驱动选题、熊叔三段式骨架、情绪地图、低创作度合规 | 写公众号, 自媒体文章, 爆款文案 | 无 |
| **weitoutiao-creator** | 写作 | 5 种文风 x 10 种框架，300 字高转化微头条分步生成 | 微头条, 头条文案, 300字爆款 | 无 |
| **snowflake-novel-writer** | 写作 | 雪花法 10 步逐层精细长篇创作、欲望弧光、去 AI 味三遍法 | 写小说, 雪花写作法, 故事创作 | 无 |
| **novel-writing** | 写作 | 基于 LOCK 系统与三幕两门结构的叙事小说极速骨架搭建 | 英文小说, LOCK系统, 故事骨架 | 无 |
| **article-deconstructor** | 写作 | 10 维度爆款文章逆向拆解、情绪曲线与刺痛句式提取 | 拆解文章, 爆款分析, 写作模板提取 | 无 |
| **black-humor-writing** | 写作 | 单立人黑色幽默五步法（主题/态度/预期违背/冲突放大） | 黑色幽默, 脱口秀段子, 讽刺文案 | 无 |
| **video-minutes** | 媒体 | 7 种视频类型自动分类、Faster-Whisper int8 转录、@tags 任务派发 | `generate_minutes.py`, 视频纪要, 视频总结 | Python, FFmpeg, faster-whisper |
| **video-dubbing** | 媒体 | ASR 转录 -> AI 翻译 -> TTS 配音 -> 分段变速对齐 -> 压制硬字幕 | `dub_segments.py`, 视频配音, 视频翻译 | Python, FFmpeg, whisper, mlx-audio |
| **mlx-tts** | 媒体 | Apple Silicon 本地 Qwen3-TTS / CosyVoice 毫秒级语音合成 | `mlx_audio.tts`, 本地语音合成, TTS | macOS, uv, mlx-audio |
| **image-design** | 媒体 | 摄影学五维模型（主体/构图/光影/镜头/胶片）AI 绘图提示词 | 生图提示词, Midjourney, 摄影描述 | 无 |
| **mckinsey-cover** | 媒体 | 麦肯锡/波士顿咨询风格研报封面与信息图结构化提示词 | `/mckinsey-cover`, 咨询封面, 研报配图 | 无 |
| **infocard** | 媒体 | 自动适配内容骨架，10+ 套杂志/看板风高清信息卡片渲染 | `/infocard <URL/文本>`, 信息卡片 | Node.js, Canvas/Playwright |
| **agent-coding-style** | 工程 | Coding Agent 的确定性回复、搜索、编辑、Git、规划、审阅与前端生成规则 | coding style, Agent 编码规范, 确定性操作 | 无 |
| **claude-simplify** | 工程 | 代码提交前三 Agent 并行审查（代码复用 / 坏味道 / 运行效率） | `/simplify`, 代码审查, 重构精简 | Git |
| **clean-code** | 工程 | Uncle Bob《Clean Code》全书 17 章知识体系蒸馏与重构指南 | 代码异味, 代码整洁之道, 重构指南 | 无 |
| **skill-security-check** | 工程 | 11 项静态安全审计扫描（注入、越权、敏感路径、凭证泄漏） | `security-check.js`, 技能审计, 漏洞扫描 | Node.js, TypeScript |
| **github-analyzer** | 工程 | 5 维度 GitHub 仓库极速解构分析（定位/痛点/架构/上手/亮点） | 分析 GitHub 项目, review this repo | Python / Node.js, curl |
| **design-md-extractor** | 工程 | 从 Web 逆向提取排版/配色/空间规范并输出 DESIGN.md | 提取设计系统, 页面设计规范, DESIGN.md | 浏览器 / Node.js |
| **jira-server-pat-cli** | 工程 | 通用 Jira Server/Data Center REST CLI，支持 PAT、内部 CA、元数据发现和完整 issue 生命周期 | Jira CLI, PAT, JQL, issue 管理 | Python 3 标准库 |
| **llm-aiops** | 工程 | 大模型在云原生运维、故障定位（RCA）与日志解析的研究知识库 | AIOps, 根因定位, 故障排查知识库 | 无 |
| **grasp** | 认知 | 十维认知框架 x 费曼交互式学习协议（含主动回忆与概念地图） | `/grasp <主题>`, 深度学习, 掌握概念 | 无 |
| **teach-eli5** | 认知 | Matt Pocock 教学法：生活类比先行、自包含 HTML 交互课件 | `/eli5 <主题>`, 给小白讲明白, 看图就懂 | 浏览器打开 HTML |
| **curriculum-design** | 认知 | 基于 OBE 成果导向与布鲁姆认知模型的教学大纲与教案设计 | 课程大纲设计, 教案编写, OBE教学 | 无 |
| **edulab** | 认知 | 中高考数学可视化：SymPy 向量建系 + Three.js 3D/2D 动态题解 | `/edulab`, 数学可视化, 几何建系 | Python (sympy), Three.js |
| **obsidian-kb-builder** | 知识 | Karpathy LLM-Wiki 模式构建本地双链图谱，支持图数据导出 | 知识库构建, Obsidian 双链, 知识图谱 | Python |
| **pdf2md** | 知识 | 基于 OpenDataLoader 的高保真 PDF 解析（支持公式、复杂跨页表格） | `pdf2md.py`, pdf 转 markdown, 论文提取 | Python, opendataloader-pdf |
| **claude-remember** | 知识 | Layer 1/2/3 记忆系统审查、提炼与去重归档工具 | 整理记忆, 记忆归档, 更新长期记忆 | 无 |

---

## 28 个技能详细功能与使用指南

### 一、深度写作与自媒体矩阵 (Content Creation & Media)

#### 1. de-ai-writing (文本去 AI 味与活人声纹校准)
- **功能特性**：作为全库反 AI 腔调的**唯一真源**。内置 36 种机器行文模式检测（包括虚空升华、非必要对称排比、以 -ing 结尾的肤浅分析、公文腔连词）、3 层禁用词表（Tier 1/2/3 绝对禁用与置换）以及 5 步活人重写流程。
- **触发意图**：去AI味、消除机器感、把这段话改得像真人写的、去除公文腔。
- **调用方式**：
  ```
  /de-ai <待修改文本> [--strength=light|medium|heavy]
  ```
- **核心产出**：去 AI 味前后的对比文本、修改项溯源清单、声纹自然度自检分。

#### 2. wechat-article-writer (自媒体与微信公众号爆款长文创作流)
- **功能特性**：集成「痛点驱动选题法」、「熊叔三段式框架」（01/02/03 结构分段）、4 种高转化开头与 3 种强收尾模式。严格执行微信官方「低创作度规避标准」，在输出前进行信息增量、原创度、内容密度与 AI 参与度 4 维严审（满分 20 分，<12 分自动打回）。
- **触发意图**：写公众号文章、自媒体长文、深度商业故事、爆款推文。
- **调用方式**：
  ```
  写公众号文章：[主题/痛点素材] --platform=wechat --target-words=2500
  ```
- **核心产出**：3 组备选爆款标题、完整可发布长文正文、情绪起伏地图、预埋金句清单、低创作度合规评分表。

#### 3. weitoutiao-creator (微头条短文案 6 步爆款生成器)
- **功能特性**：专为 300 字以内高互动短内容设计。提供 5 种成熟写作风格（故事叙述、悬念引导、数据事实、情感共鸣、直接对话）和 10 种经典结构框架（如「惊人事实-数据-分析-互动」）。采用交互式 6 步 SOP，每一步均需用户确认后推进。
- **触发意图**：微头条、头条短文案、社交平台短帖、高互动文案。
- **调用方式**：
  ```
  生成微头条：[领域标签/核心观点]
  ```
- **核心产出**：15-25 字吸睛标题、300 字以内正文、评论区互动引导钩子。

#### 4. snowflake-novel-writer (雪花写作法 10 步精细长篇创作)
- **功能特性**：基于经典雪花写作法（Snowflake Method），从「一句话概括」逐层展开为「结构骨架 -> 主题反主题 -> 人物弧线 -> 关系网与秘密 -> 一页大纲 -> 场景清单 -> 叙述声音 -> 样章与全文」。内置小说专用的「去 AI 味三遍法」与反俗套检查清单。
- **触发意图**：写长篇小说、网文构思、雪花法大纲、设定人物弧光、小说样章。
- **调用方式**：
  ```
  雪花写小说：[题材与核心设定]
  ```
- **核心产出**：故事核心命题、人物三层标签档案（表层/深层/反差）、场景细化清单、1500-2500 字样章及全文正文。

#### 5. novel-writing (LOCK 系统叙事小说创作骨架)
- **功能特性**：基于 James Scott Bell 的 LOCK 系统（Lead 主角、Objective 目标、Conflict 冲突、Knockout 结局）与经典三幕两门（Two Doorways of No Return）结构。侧重快速搭建高张力的叙事主线与情节大纲。
- **触发意图**：英文故事创作、三幕式大纲、LOCK 系统构思、短篇叙事骨架。
- **调用方式**：
  ```
  /novel-writing [故事概念/主角设定]
  ```
- **核心产出**：LOCK 四要素分析表、三幕式 8 节点剧情线、核心转折点设计。

#### 6. article-deconstructor (爆款文章 10 维度深度拆解器)
- **功能特性**：对标业界顶尖文章，从选题价值、标题公式、Hook 钩子、论证逻辑、案例密度、情绪曲线、刺痛句式、行文节奏、金句提炼及可复用模板 10 个维度进行全景逆向解构。
- **触发意图**：拆解文章、分析爆款逻辑、提取写作套路、文章结构逆向工程。
- **调用方式**：
  ```
  拆解这篇文章：[文章链接或正文全文]
  ```
- **核心产出**：10 维解构报告图表、作者论证骨架图、可直接套用的空白结构模板。

#### 7. black-humor-writing (单立人黑色幽默五步创作法)
- **功能特性**：基于单立人脱口秀与讽刺文学创作逻辑，采用「锁定严肃主题 -> 明确讽刺态度 -> 铺垫常规预期 -> 植入荒诞事实打破预期 -> 逻辑自洽地放大冲突」五步流水线，制造高质量荒谬感与喜剧张力。
- **触发意图**：黑色幽默、讽刺段子、脱口秀剧本、荒诞短文、反讽文案。
- **调用方式**：
  ```
  写黑色幽默段子：[社会现象/吐槽主题]
  ```
- **核心产出**：段子铺垫与包袱（Setup & Punchline）结构表、荒诞逻辑推演链、成稿文本。

---

### 二、多媒体工程与音视频合成 (Multimedia & Audio/Video Engineering)

#### 8. video-minutes (智能视频纪要生成与 @tags 任务分发引擎)
- **功能特性**：集成 `faster-whisper` 高性能转录（支持 int8 量化与 VAD 过滤，转录速度提升 2-4 倍）。具备 7 种视频类型自动分类算法（会议、课程、访谈、演讲、播客、教程、录屏），并支持在纪要中自动提取 `@dev`、`@design`、`@article`、`@reminder` 等任务标签。
- **触发意图**：视频总结、视频转文字、会议录像整理、提取网课笔记、生成字幕。
- **CLI 调用方式**：
  ```bash
  # 处理本地会议视频并生成 Markdown 纪要
  python3 video-minutes/scripts/generate_minutes.py meeting.mp4 --type meeting --language zh

  # 批量扫描并处理 Zoom/录屏目录
  python3 video-minutes/scripts/scan-and-process.py ~/Recordings/ --since-hours 24
  ```
- **核心产出**：结构化视频纪要（Markdown / Obsidian 双链 / Notion 格式）、时间戳大纲、决议清单、待办 TODO 列表。

#### 9. video-dubbing (全流程视频翻译、AI 语音克隆配音与字幕压制)
- **功能特性**：完整的端到端视频多语言转译流水线：抽音轨 (16kHz) -> Whisper ASR -> 逐句严密翻译 -> MLX-TTS 语音生成（基于第一句维持音色一致性）-> 智能分段变速对齐 (0.88-1.20x 保持原音画时序) -> FFmpeg 音视频合流与硬字幕压制。
- **触发意图**：视频翻译、视频自动配音、外语视频汉化、双语字幕压制。
- **CLI 调用方式**：
  ```bash
  # 1. 抽取音频并获取精确时间戳 SRT
  ffmpeg -y -i input.mp4 -ar 16000 -ac 1 audio16k.wav
  whisper audio16k.wav --model large-v3-turbo --output_format srt

  # 2. 生成对齐音频并压制硬字幕
  python3 video-dubbing/scripts/dub_segments.py audio16k.srt translated.txt dubbing.wav subtitle_synced.srt --lang zh
  python3 video-dubbing/scripts/burn_subtitles.py output_temp.mp4 subtitle_synced.srt output_final.mp4
  ```
- **核心产出**：`output_final.mp4`（带对齐新音轨与烧录硬字幕的视频文件）、`subtitle_synced.srt`。

#### 10. mlx-tts (Apple Silicon 专用本地极速语音合成)
- **功能特性**：专为 macOS M 系列芯片优化的本地 TTS 引擎，基于 MLX 框架驱动 Qwen3-TTS / CosyVoice 模型。支持零样本文色克隆（Voice Cloning）、跨语种合成与 Prompt 情感控制，脱离云端 API 实现毫秒级离线渲染。
- **触发意图**：本地语音合成、文本转语音、Qwen3-TTS、MLX 语音生成、声音克隆。
- **CLI 调用方式**：
  ```bash
  # 基本文本朗读
  mlx_audio.tts --model mlx-community/Qwen3-TTS-12B-Instruct --text "欢迎使用开源 Agent 技能库。" --output speech.wav

  # 音色参考克隆合成
  mlx_audio.tts --ref_audio speaker_sample.wav --ref_text "参考音频文本" --text "克隆生成的目标语音" --output cloned.wav
  ```
- **核心产出**：高保真 WAV 音频文件、音色设计 Prompt 配置文件。

#### 11. image-design (摄影学五维 AI 绘图提示词生成器)
- **功能特性**：基于真实摄影工业标准，从「主体动态与材质 (Subject)」、「经典画幅构图 (Composition)」、「物理光线逻辑 (Lighting)」、「相机焦段与光圈视角 (Lens & Angle)」、「胶片颗粒与色彩科学 (Film Tone & Color)」五维解构需求，生成 Midjourney v6 / Stable Diffusion 工业级 Prompt。
- **触发意图**：画图提示词、Midjourney Prompt 生成、摄影级生图描述、Stable Diffusion 调优。
- **调用方式**：
  ```
  设计摄影生图提示词：[场景概念/主体描述] --aspect-ratio=16:9 --style=cinematic
  ```
- **核心产出**：中英文双语 Prompt、负向提示词 (Negative Prompt)、相机参数推荐清单（焦段/光圈/ISO/胶卷型号）。

#### 12. mckinsey-cover (麦肯锡与顶级咨询风研报封面生成器)
- **功能特性**：基于 Adrian Punk 原创设计方法论，针对商业白皮书、战略研报与咨询 PPT，生成具备顶级机构质感（极简几何分区、瑞士平面排版网格、非饱和沉稳商务配色、隐喻性抽象 3D 图形）的视觉生成指令。
- **触发意图**：麦肯锡封面、咨询研报封面、商业计划书配图、高端 PPT 封面。
- **调用方式**：
  ```
  /mckinsey-cover [报告主题/行业领域]
  ```
- **核心产出**：封面排版结构图（ASCII Grid）、Midjourney/DALL-E 3 专用英文生图 Prompt、配色色值方案（HEX/CMYK）。

#### 13. infocard (高清自适应现代信息卡片渲染引擎)
- **功能特性**：根据输入文本或 URL 内容的信息密度与情绪，自适应匹配最佳排版骨架（杂志风 Editorial、看板 Dashboard、暗黑 Slate、国风 Guofeng、海洋 Ocean 等 10+ 款主题），直接通过本地 Node.js + Playwright/Canvas 渲染并输出高分辨率 PNG 图片。
- **触发意图**：生成信息卡片、文章转长图、卡片总结、可视化摘要图片。
- **调用方式**：
  ```bash
  # 从 URL 提取并生成 Slate 主题卡片
  /infocard https://example.com/article --theme=slate

  # 从纯文本生成双语对照卡片
  /infocard "输入你的核心文本" --theme=editorial --lang=zh
  ```
- **核心产出**：保存至 `~/Downloads/infocard-img/` 的高清 PNG 渲染图片文件。

---

### 三、代码工程与研发安全 (Code Engineering & DevSecOps)

#### 14. agent-coding-style (Coding Agent 确定性行为规范)
- **功能特性**：将 Coding Agent 的回复格式、搜索策略、精准编辑、Git 安全、任务规划、代码审阅和前端生成规则统一为 43 条确定性约束，减少过度修改、无验证交付、危险 Git 操作和格式漂移。
- **触发意图**：Agent 编码规范、确定性代码修改、统一 Coding Agent 行为、提交前操作约束。
- **调用方式**：
  ```
  按 agent-coding-style 规范完成以下代码任务：[任务描述]
  ```
- **核心产出**：边界明确的修改方案、最小代码变更、验证结果和可审计的 Git 操作说明。

#### 15. claude-simplify (三 Agent 并行代码审查与精简流水线)
- **功能特性**：在 Git Commit 或 PR 提交前触发。基于分支差异（`git diff`），并行调度三个独立审计角色：
  - **Reuse Reviewer**：扫描是否重复造轮子、是否存在项目中已有的工具函数未被复用；
  - **Quality Reviewer**：检查代码异味、圈复杂度过高、深层嵌套、不合规范的命名与硬编码；
  - **Efficiency Reviewer**：审查内存泄漏、不必要的大对象拷贝、异步死锁与慢查询。
- **触发意图**：`/simplify`、代码审查、提交前检查、代码重构、代码精简。
- **调用方式**：
  ```bash
  /simplify [commit/branch/HEAD~1]
  ```
- **核心产出**：三维度代码审查报告、精确到文件和行号的修改建议、精简前后的代码对比补丁。

#### 16. clean-code (《Clean Code》全书 17 章知识体系与重构指南)
- **功能特性**：将 Robert C. Martin (Uncle Bob)《代码整洁之道》全书 17 章核心原则（有意义的命名、函数单一职责与单一抽象层、注释准则、对象与数据结构、异常处理与消灭 null、边界隔离、TDD 三定律、并发防御、Smells and Heuristics 代码异味全集）进行系统化蒸馏，并提供现代语言（TypeScript, Python, Go, Rust, C++）的现代化代码映射。
- **触发意图**：Clean Code、代码整洁规范、代码坏味道检查、重构原则咨询。
- **调用方式**：
  ```
  按照 Clean Code 审查并重构以下代码：[代码片段]
  ```
- **核心产出**：代码异味诊断清单（带 Uncle Bob 原书规则编号如 `F1`, `G14`）、重构后的整洁代码、设计原则说明。

#### 17. skill-security-check (Agent Skill 11 项静态漏洞与安全审计器)
- **功能特性**：在安装、导入或运行第三方 Agent Skill 之前执行静态安全扫描。覆盖 11 类核心威胁（提示词注入、任意代码执行、危险 shell 命令、敏感路径越权访问、环境变量与 Token 窃取、网络外发挂马等），输出严格的风险评级（P0 阻断 / P1 警告 / P2 安全）。
- **触发意图**：检查技能安全性、审查 Skill、扫描 SKILL.md、技能安全审计。
- **CLI 调用方式**：
  ```bash
  node skill-security-check/scripts/security-check.js /path/to/skill-folder
  ```
- **核心产出**：静态代码与 Markdown 审计报告、漏洞定位（文件与行号）、安全风险评分（P0/P1/P2）。

#### 18. github-analyzer (GitHub 仓库极速 5 维解构报告生成器)
- **功能特性**：针对用户提供的 GitHub 仓库链接，自动抓取 `README.md`、仓库元数据、目录结构与依赖包，在 60 秒内输出五章节结构化分析研报（是什么、核心痛点、关键特性、3 分钟快速上手指南、架构与实现亮点）。
- **触发意图**：分析 GitHub 项目、帮我看下这个仓库、analyze repo、这个项目是干啥的。
- **调用方式**：
  ```
  分析这个开源项目：https://github.com/owner/repo
  ```
- **核心产出**：标准 Markdown 格式的项目解析研报、技术栈雷达、适用场景评估。

#### 19. design-md-extractor (Web 视觉设计系统逆向提取器)
- **功能特性**：通过读取目标网页的 DOM、计算样式（Computed Styles）与视觉截屏，逆向推导并生成符合 Google Labs 规范的 `DESIGN.md` 设计规范文件，提取包含色彩语义系统（Tokens）、字体层级、排版间距、阴影网格与组件样式的设计系统文档。
- **触发意图**：提取网站设计规范、生成 DESIGN.md、分析页面 UI 风格、提取设计 Token。
- **调用方式**：
  ```
  从这个网站提取设计系统：https://example.com/
  ```
- **核心产出**：标准 `DESIGN.md` 文档、CSS Variables 定义代码块、Tailwind 配色扩展配置。

#### 20. jira-server-pat-cli (Jira Server/Data Center 通用管理 CLI)
- **功能特性**：提供纯 Python 标准库 Jira REST CLI，支持 PAT、Cookie、Basic Auth、组织 CA 和 context path。所有 issue type、custom field、transition、priority、component、version 与用户标识均从目标实例动态发现，避免固定 ID 和环境隐私泄露。
- **触发意图**：Jira CLI、PAT 管理 Jira、JQL 搜索、批量 issue 操作、内部 CA Jira 自动化。
- **CLI 调用方式**：
  ```bash
  export JIRA_BASE_URL="https://jira.example.com/jira"
  export JIRA_PAT="<secret>"
  python3 jira-server-pat-cli/scripts/jira_cli.py whoami
  python3 jira-server-pat-cli/scripts/jira_cli.py search "project = PROJ ORDER BY updated DESC" --limit 100
  ```
- **核心产出**：实例与权限探测结果、JQL JSON 数据、issue CRUD、transition、评论、工时、附件、链接、watcher 和 vote 操作结果；写操作支持 dry-run，破坏性及 raw REST 写操作要求 `--yes`。

#### 21. llm-aiops (大模型 AIOps 运维与根因定位研究参考库)
- **功能特性**：汇集 78+ 篇国际顶会及工业界前沿论文精华的 LLM for AIOps 知识库。覆盖大模型在日志异常检测、时序指标告警收敛、微服务调用链分布式追踪、根因定位（RCA）、自动故障修复（Auto-Remediation）与安全合规运维领域的成熟落地模式与架构方案。
- **触发意图**：LLM AIOps、智能运维、大模型故障诊断、根因分析算法、日志大模型。
- **调用方式**：
  ```
  AIOps 咨询：[故障场景/日志异常排查思路]
  ```
- **核心产出**：AIOps 算法选型矩阵、微服务故障诊断 Agent 拓扑设计图、学术参考文献引用。

---

### 四、认知学习与教育实验室 (Cognitive Learning & Education)

#### 22. grasp (十维认知框架 x 费曼加速学习协议)
- **功能特性**：基于「十维认知模型」（名称、类别、定义、特征、结构、功能、运行条件、历史演进、未来趋势、潜在风险）与费曼教学法。提供 7 个交互式学习阶段（锚定、探索、结构化、费曼输出、主动回忆、跨领域迁移、复习），构建深层概念理解。
- **触发意图**：`/grasp <主题>`、深度学习一个概念、彻底搞懂某技术、概念拆解。
- **调用方式**：
  ```
  /grasp Transformer架构 [--phase=1]
  ```
- **核心产出**：十维概念雷达图、概念架构 ASCII 关系图、主动回忆自测题库。

#### 23. teach-eli5 (Matt Pocock 教学法小白友好交互课件引擎)
- **功能特性**：融合 Matt Pocock `teach` 教学方法论（MISSION 学习目标锚定、最近发展区 ZPD 选材、术语表 glossary 与学习记录 ADR 沉淀、资产 assets 复用）与 ELI5（Explain Like I'm 5）小白约束。将复杂主题拆解为「图多、字少、生活类比先行」的独立自包含精美 HTML 教学页。
- **触发意图**：`/eli5 <主题>`、用大白话讲明白、给外行解释技术、做个看图就懂的教学页。
- **调用方式**：
  ```
  /eli5 量子纠缠 --mission="给中学生解释清楚原理"
  ```
- **核心产出**：`./lessons/0001-<slug>.html`（自包含可打印 HTML 课件，内联 SVG 机制图与类比卡片）、`references/glossary.md`、`learning-records/`。

#### 24. curriculum-design (OBE 成果导向与布鲁姆认知模型课程设计系统)
- **功能特性**：基于 OBE（Outcome-Based Education）产出导向教育理念与布鲁姆教育目标六层认知分类学（记忆、理解、应用、分析、评价、创造），生成符合高等院校与专业培训标准的教学大纲、教学日历与单课结构化教案。
- **触发意图**：课程大纲设计、编写教案、教学设计、OBE 教学方案、培训课程规划。
- **调用方式**：
  ```
  设计课程大纲：[课程名称] --target-audience=[受众背景] --duration=[课时]
  ```
- **核心产出**：课程教学目标矩阵（含布鲁姆层级对应）、学时分配表、期末考核评价权重表、分课时标准教案文档。

#### 25. edulab (中高考数学可视化解题实验室)
- **功能特性**：面向初高中数学几何与函数题目的专业可视化求解与动态演示工具。支持：
  - **3D 立体几何**：通过 Python SymPy 空间向量自动建系求解，输出 Three.js 交互式 3D 解题页面（可旋转视角、显示垂线投影与法向量）；
  - **2D 函数与解析几何**：输出带参数滑块控制的 2D 交互图表，动态展现参数变化对图像交点、极值点与单调区间的影响。
- **触发意图**：`/edulab`、数学题可视化、立体几何建系、函数图像动态演示。
- **调用方式**：
  ```
  /edulab [题目文本/几何条件] --mode=3d-geometry
  ```
- **核心产出**：Python 向量代数严密演算推导过程、自包含交互式 HTML 可视化演示网页。

---

### 五、知识库与记忆管理 (Knowledge Base & Memory Management)

#### 26. obsidian-kb-builder (Karpathy LLM-Wiki 本地双链 Obsidian 知识库)
- **功能特性**：遵循 Andrej Karpathy LLM-Wiki 架构模式。支持输入本地文件、文档目录或网络 URL，自动化抽取核心实体与关系，生成符合严格 Wiki-Schema 规范的本地 Markdown 双链笔记库（`[[双链]]` 互联），并支持导出结构化图数据供图计算分析。
- **触发意图**：搭建知识库、构建 Obsidian vault、文档双链化、导出知识图谱。
- **CLI 调用方式**：
  ```bash
  # 从指定目录扫描并构建知识库图谱
  python3 obsidian-kb-builder/scripts/build_kb.py --input ~/Documents/Papers/ --vault ~/Documents/MyVault/
  ```
- **核心产出**：Obsidian Vault 笔记集合（含 YAML Frontmatter、双链与标签）、`graph_data.json` 知识图谱结构数据。

#### 27. pdf2md (基于 OpenDataLoader 的高精度 PDF 转 Markdown 引擎)
- **功能特性**：基于 OpenDataLoader-PDF 混合解析技术。专为学术论文、技术研报、财务报表等复杂版式 PDF 设计，能够高精度识别 LaTeX 数学公式、复杂跨页表格结构、代码块、双栏排版与内嵌图片，输出极度干净的 Markdown 格式文本。
- **触发意图**：PDF 转 Markdown、提取 PDF 论文、解析 PDF 表格公式。
- **CLI 调用方式**：
  ```bash
  python3 pdf2md/scripts/pdf2md.py input_paper.pdf --output output.md --extract-images
  ```
- **核心产出**：高精度 `output.md` 文档、提取的插图文件夹 `images/`。

#### 28. claude-remember (多层级 AI Agent 长期记忆审查与归档工具)
- **功能特性**：规范管理 Agent 的三层记忆架构（Layer 1 云端全局记忆、Layer 2 用户级持久化规范 `~/.claude/MEMORY.md`、Layer 3 项目级日常工作日志 `YYYY-MM-DD.md` 与精炼记忆 `MEMORY.md`）。提供记忆冗余检测、矛盾解决与超过 30 天日志的蒸馏归档能力。
- **触发意图**：整理记忆、审查记忆文件、记忆去重与归档、更新长期记忆。
- **调用方式**：
  ```
  整理当前项目的长期记忆与工作日志
  ```
- **核心产出**：更新后的精炼 `MEMORY.md`、蒸馏清理后的历史归档记录。

---

## 快速开始与环境安装

### 1. 安装 Skill 至本地 Agent 环境

本仓库的所有技能均遵循通用规范。你可以将整个仓库或特定技能软链 / 复制到你的全局或项目级技能目录下：

```bash
# 克隆仓库
git clone https://github.com/your-username/agent-skills.git ~/workspace/agent-skills

# 方式 A：安装特定技能到全局 skills 目录 (推荐)
mkdir -p ~/.claude/skills
cp -r ~/workspace/agent-skills/de-ai-writing ~/.claude/skills/
cp -r ~/workspace/agent-skills/infocard ~/.claude/skills/

# 方式 B：全量批量软链接
for dir in ~/workspace/agent-skills/*/; do
  skill_name=$(basename "$dir")
  if [ -f "$dir/SKILL.md" ]; then
    ln -sfn "$dir" ~/.claude/skills/"$skill_name"
  fi
done
```

### 2. 常用运行时环境依赖配置

部分多媒体与数据处理类技能依赖特定的底层 CLI 工具与 Python 库，推荐根据需要快速安装：

```bash
# 1. 音视频处理依赖 (macOS / Ubuntu)
brew install ffmpeg uv           # macOS
sudo apt install ffmpeg          # Ubuntu

# 2. 本地 TTS 极速引擎 (Apple Silicon macOS)
uv tool install --force "mlx-audio" --prerelease=allow

# 3. 高精度 PDF 解析依赖
pip install "opendataloader-pdf[hybrid]"

# 4. 视频转录与纪要依赖
pip install faster-whisper moviepy pyyaml requests
```

---

## 技能开发规范与贡献指南

我们欢迎社区贡献新的生产级 Agent Skill！提交 PR 前请确保满足以下规范：

1. **目录结构**：
   ```
   my-new-skill/
   +-- SKILL.md                 # 必需：完整行为规范与契约文档
   +-- scripts/                 # 可选：Python/Node.js/Shell 执行脚本
   +-- references/              # 可选：模块化参考资料与 Schema 定义
   +-- assets/                  # 可选：静态模板、组件与样式表
   ```
2. **SKILL.md 必备结构**：
   - **YAML Frontmatter**：包含 `name`, `description`, `version`, `argument-hint` 等元数据。
   - **Outcome Contract**：明确定义产出内容（Outcome）、完成判定（Done When）与验证凭证（Evidence）。
   - **Hard Rules**：列出绝对禁止的负向行为与执行硬边界。
   - **去 AI 味与纯 ASCII 约束**：生成内容严禁使用易引起乱码的 Unicode 字符，必须使用纯 ASCII 符号替代。
3. **安全审查通过**：新增技能必须通过 `skill-security-check` 的静态安全审计（无 P0/P1 风险项）。

---

## 开源协议与声明

本项目采用 [MIT License](LICENSE) 开源协议。所有技能均经过安全审查与实践工程验证，请放心在企业与个人生产环境中集成使用。
