# Agent Skills Collection

通用 AI Agent 智能技能集合 — 自动化内容创作、社交媒体管理、安全检查与生产力工具箱。

## 项目简介

本项目是一系列为 AI 助手设计的 Skill（技能）模块，每个 Skill 都是针对特定场景的自动化解决方案。从视频内容处理到社交媒体运营，从文章分析到内容生成，从安全检查到翻译优化，帮助用户提升工作效率，实现智能化创作流程。

## Skill 目录

### 📊 内容策展与分析

| Skill | 描述 | 状态 |
|-------|------|------|
| [article-deconstructor](#article-deconstructor) | 文章拆解分析器 | ✅ 可用 |
| [infocard](#infocard) | 智能信息卡片生成器 | ✅ v6.6 |
| [pdf2md](#pdf2md) | PDF 转 Markdown 工具 | ✅ 可用 |
| [design-md-extractor](#design-md-extractor) | URL 设计系统提取器 | ✅ 可用 |
| [github-analyzer](#github-analyzer) | GitHub 项目一键分析 | ✅ 可用 |

### ✍️ 内容创作与生成

| Skill | 描述 | 状态 |
|-------|------|------|
| [wechat-article-writer](#wechat-article-writer) | 专业自媒体文章写作工具 | ✅ 可用 |
| [weitoutiao-creator](#weitoutiao-creator) | 微头条爆款文案生成器 | ✅ 可用 |
| [snowflake-novel-writer](#snowflake-novel-writer) | 雪花写作法小说创作助手 | ✅ 可用 |
| [image-design](#image-design) | 高级质感 AI 图片设计 | ✅ 可用 |
| [frontend-design](#frontend-design) | 高保真前端界面设计 | ✅ 可用 |
| [curriculum-design](#curriculum-design) | 专业课程设计与教学设计 | ✅ 可用 |
| [de-ai-writing](#de-ai-writing) | 文本去AI味，五步法保留真实人味 | ✅ 可用 |
| [life-quotes](#life-quotes) | 人生感悟与金句生成 | ✅ 可用 |
| [material-to-slides](#material-to-slides) | 资料转 HTML 幻灯片 | ✅ 可用 |
| [viral-hook](#viral-hook) | 社交媒体爆款文案生成器 | ✅ 可用 |

### 🎬 音视频处理

| Skill | 描述 | 状态 |
|-------|------|------|
| [video-minutes](#video-minutes) | 智能视频纪要生成器 | ✅ 可用 |
| [video-dubbing](#video-dubbing) | AI 视频配音与翻译 | ✅ 可用 |
| [mlx-tts](#mlx-tts) | Apple Silicon 本地 TTS | ✅ 可用 |

### 🛡️ 工具与安全

| Skill | 描述 | 状态 |
|-------|------|------|
| [skill-security-check](#skill-security-check) | Skill 安装前安全检查 | ✅ 可用 |
| [claude-simplify](#claude-simplify) | 代码简化与质量检查（三 Agent 并行审查） | ✅ 可用 |
| [claude-remember](#claude-remember) | 记忆管理与整理 | ✅ 可用 |

### 🧠 学习与效率

| Skill | 描述 | 状态 |
|-------|------|------|
| [blitz](#blitz) | 通用加速学习协议 — 7 阶段交互式学习（费曼技巧、主动回忆、间隔重复） | ✅ 可用 |
| [llm-aiops](#llm-aiops) | LLM + AIOps 研究参考指南（78+ 论文） | ✅ 可用 |

### 🤖 AI Agent 与自动化

| Skill | 描述 | 状态 |
|-------|------|------|
| [hermes-setup](#hermes-setup) | Hermes Agent 全自动安装与配置 | ✅ 可用 |
| [claude-simplify](#claude-simplify-1) | 三 Agent 并行代码审查（复用/质量/效率） | ✅ 可用 |

---

## Skill 详情

### blitz

**通用加速学习协议** — 基于 7 个验证有效的学习科学方法（费曼技巧、第一性原理、主动回忆、间隔重复等），快速上手任何知识领域。

**7 阶段交互式流程：**

| 阶段 | 名称 | 核心问题 |
|------|------|----------|
| 1 | **费曼学习法** | "你能用简单语言解释一遍吗？" |
| 2 | **第一性原理拆解** | "不可再简化的底层要素是什么？" |
| 3 | **主动回忆训练** | "不翻笔记能答对吗？" |
| 4 | **间隔重复表** | "什么时候复习什么？" |
| 5 | **知识提炼** | "一页速查表长什么样？" |
| 6 | **学习路线图** | "通往精通的路径是什么？" |
| 7 | **薄弱点诊断** | "我盲区在哪？" |

**使用方式：**
```bash
/blitz <topic>              # 全流程顺序进行
/blitz <topic> --phase=N    # 跳到指定阶段
/blitz <topic> --phase=all  # 一口气跑完所有阶段
```

**适用场景：**
- 快速理解新领域
- 备考复习
- 复杂概念拆解
- 知识盲区排查

[查看完整文档](blitz/SKILL.md)

---

### design-md-extractor

**URL 设计系统提取器** - 输入任意网站 URL，提取其视觉设计系统，生成符合 `@google/design.md` 规范的 DESIGN.md 文档。

**核心能力：**
- 🔗 **URL 视觉分析** - 自动抓取网页，提取颜色、字体、间距、圆角、阴影等设计 Token
- 📝 **符合 Spec 的 DESIGN.md** - YAML front matter + 8 段 Markdown（Overview / Colors / Typography / Layout / Elevation / Shapes / Components / Do's & Don'ts）
- 🧩 **组件状态覆盖** - 记录按钮、输入框、卡片等组件的 hover / focus / active 等所有状态
- 🔗 **Token 引用** - 组件属性使用 `{colors.primary}` 引用语法，符合 W3C DTCG 标准
- ✅ **内置校验** - 支持 `npx @google/design.md lint` 验证结构正确性

**使用方式：**
```
DESIGN.md for https://example.com
extract design tokens from https://stripe.com
帮我分析 https://linear.app 的设计系统
```

**参考项目：**
- [rico-skills/rico-design-md](https://github.com/ricocc/rico-skills) — 灵感来源
- [google-labs-code/design.md](https://github.com/google-labs-code/design.md) — 输出规范

[查看完整文档](design-md-extractor/SKILL.md)

---

### github-analyzer

**GitHub 项目一键分析** - 快速分析任意 GitHub 仓库，回答项目是什么、有什么用、怎么用。

**核心能力：**
- 📖 **README 理解** - 自动分析项目文档和代码结构
- 📊 **五章节报告** - 项目概述、核心亮点、技术栈、使用指南、社区活跃度
- 🔍 **智能评估** - 代码质量、文档完整度、维护状态

**使用方式：**
```
分析 https://github.com/xxx/xxx
这个项目是做什么的
```

[查看完整文档](github-analyzer/SKILL.md)

---

### article-deconstructor

**文章拆解器** - 分析高流量文章的核心要素，提取结构、说服策略、情绪触发点和金句。

**拆解维度（10个）：**
1. 核心观点分析
2. 副观点/支撑论点
3. 说服策略识别
4. 情绪触发点标注
5. 金句提取
6. 情感曲线分析
7. 情感层次分析
8. 论证方式多样性
9. 视角转化分析
10. 语言风格特征

**使用场景：**
- 内容创作分析
- 文案学习
- 爆款文章研究
- 对标账号分析

[查看完整文档](article-deconstructor/SKILL.md)

---

### video-minutes

**智能视频纪要生成器** - 自动提取视频语音、生成字幕、智能分类总结。

**功能特性：**
- 🤖 AI 自动分类 7 种视频类型（会议/课程/访谈/演讲/播客/教程/录屏）
- 📝 智能总结核心要点、行动项、关键决策
- 🏷️ 任务分发：通过 @tags 将待办分发给其他 skill
- 🔗 多源支持：本地文件、Zoom/腾讯会议、YouTube/B站链接
- 🌐 多语言支持 99+ 语言

**使用方式：**
```bash
python scripts/generate_minutes.py meeting.mp4
python scripts/generate_minutes.py lecture.mp4 --type lecture
python scripts/generate_minutes.py ~/Recordings --batch
```

[查看完整文档](video-minutes/README.md)

---

### infocard

**智能信息卡片生成器** - 从 URL 提取内容，自动生成可定制样式的信息卡片图片。

**核心能力：**
- 🔗 **URL 内容抓取** - 自动读取并解析网页/Twitter 内容
- 🧠 **智能内容梳理** - 分析内容类型，自动提取核心要点，以"知识分享"而非"摘要"方式呈现
- 🎨 **内容驱动布局** - 三个维度（密度/结构/情绪）自动选择最佳视觉形式
- 🌈 **10 种主题配色** - slate/ocean/sunset/coral/indigo/forest/dark/purple/dashboard/guofeng
- 📷 **图片导出** - HTML 转 PNG，支���自适应高度
- 🌐 **多语言支持** - 自动检测语言，支持中英双语输出

**使用方式：**
```bash
/infocard <URL>                       # 默认主题
/infocard <URL> --theme=slate        # Slate 主题
/infocard <URL> --theme=ocean --width=1200
```

[查看完整文档](infocard/SKILL.md)

---

### life-quotes

**人生感悟与金句生成器** - 根据任意话题生成人生感悟、哲理警句或心灵鸡汤文案。

**适用场景：**
- 视频号文案
- 朋友圈金句
- 每日感悟
- 情感共鸣内容创作

**输出格式：**
每次生成 3 条不同风格的警句，可选风格包括：
- **哲思类** —— 通透、有洞察、带一点反常识
- **治愈类** —— 温暖、安抚、给人力量
- **诗意类** —— 优美、意象化、有文学感
- **反讽类** —— 尖锐、自嘲、带一点黑色幽默
- **行动类** —— 激励、推动、让人想立刻做点什么

**使用方式：**
```
/life-quotes <话题>
```

[查看完整文档](life-quotes/SKILL.md)

---

### material-to-slides

**资料转 HTML 幻灯片** - 将任意资料（URL / 本地文件 / 粘贴文本）阅读理解后，生成可直接播放的 HTML 幻灯片。

**核心工作流（四阶段）：**
1. **读取内容** - 支持 URL、本地文件、粘贴文本、搜索需求等多种输入
2. **深度理解** - 逐段分析，提取核心论点、结构分析、逻辑关系
3. **幻灯片生成** - 默认风格：贵臧编辑部纸墨印刷感，支持 5 种配色
4. **备选色板** - Slate（石板）、Warm（暖阳）、Forest（林间）适配不同内容氛围

**导航支持：** ←/→ 键翻页、Hash 同步、PPTX 友好打印

**使用方式：**
```
/把这个做成PPT <URL>
/generate slides from <file>
```

[查看完整文档](material-to-slides/SKILL.md)

---

### viral-hook

**社交媒体爆款文案生成器** - 阅读理解图片或文本内容，生成社交媒体爆款标题、评论描述和标签。

**支持平台：**
- 小红书
- 微博
- Twitter/X
- 朋友圈

**标题风格：**
- **悬念型** —— 制造好奇心，让人忍不住点开
- **数据型** —— 用数字增强可信度
- **对比型** —— 制造反差和冲突
- **情绪型** —— 触发情感共鸣
- **反常识型** —— 打破认知惯性

**使用方式：**
```bash
/viral-hook <图片路径或文本>
/viral-hook <文本> --platform=小红书 --style=悬念 --count=3
```

[查看完整文档](viral-hook/SKILL.md)

---

### novel-writing

**小说创作专业助手** - 基于 LOCK 系统、三幕结构和人物弧光的系统化小说创作框架。

**核心系统：**
- **LOCK 系统** - Lead（主角）、Objective（目标）、Conflict（冲突）、Knockout（结局）
- **三幕结构 + 两扇门** - 经典叙事结构，控制故事节奏
- **对话与冲突设计** - 制造张力和推动情节
- **人物弧光** - 设计角色的成长轨迹

**适用场景：**
- 规划或大纲新故事
- 塑造主角、反派或配角
- 构建跨幕的情节结构
- 撰写有张力的对话
- 诊断故事问题（扁平角色、拖沓中段、薄弱高潮）

[查看完整文档](novel-writing/SKILL.md)

---

### wechat-article-writer

**专业自媒体文章写作工具** - 创作有传播力的新媒体内容，包括热点文章、情感故事、观点评论、人物稿等。

**适用场景：**
- 📰 公众号文章
- 📝 自媒体内容
- 💥 爆款文案
- 📕 小红书笔记
- ❓ 知乎回答
- 📰 头条文章

**内容类型：**
- 热点文章
- 情感故事
- 观点评论
- 人物稿
- 教程指南
- 产品评测

**使用方式：**
```bash
/wechat-article-writer "主题或关键词"
```

[查看完整文档](wechat-article-writer/SKILL.md)

---

### weitoutiao-creator

**微头条爆款文案生成器** - 帮助用户生成微头条平台爆款文案，提供选题指导、风格选择、框架构建和文案优化的完整6步工作流程。

**核心能力：**
1. **选题分析** - 根据账号标签和目标受众提供选题建议
2. **素材获取** - 支持热点查询、爆款拆解、原创思路三种路径
3. **风格选择** - 5种写作风格（故事、悬念、数据、情感、对话）
4. **框架构建** - 10种文案框架结构
5. **文案生成** - 输出300字以内的爆款文案
6. **优化迭代** - 根据反馈持续优化

**使用方式：**
```bash
/weitoutiao-creator
```

[查看完整文档](weitoutiao-creator/SKILL.md)

---

### snowflake-novel-writer

**雪花写作法小说创作助手** - 使用雪花写作法（The Snowflake Method）引导用户创作约15000字短篇小说的专业写作助手。

**核心流程（10步）：**
1. 一句话概括
2. 一段式概括
3. 人物设定
4. 一页纸大纲
5. 人物详细背景
6. 四页纸大纲
7. 人物完整档案
8. 场景清单
9. 场景规划
10. 初稿写作

**适用题材：**
- 职场、校园、仙侠、穿越、悬疑、言情等各类小说

**使用方式：**
```bash
/snowflake-novel-writer
```

[查看完整文档](snowflake-novel-writer/SKILL.md)

---

### image-design

**高级质感 AI 图片设计** - 基于摄影逻辑的 AI 图片提示词生成技能，生成专业级 AI 绘图提示词。

**五大核心维度：**
1. **主体描述 + 构图位置** - 三分法、动线引导、平衡元素
2. **光线逻辑** - 方向 × 光比 × 色温的三角公式
3. **相机视角** - 平视/仰视/俯视 + 焦段选择（24mm/50mm/85mm）
4. **风格与质感** - 胶片模拟、3D渲染、导演风格借用
5. **真实感增强** - iPhone风格、抓拍感、动态模糊

**适用平台：**
GPT-image2、Midjourney、Stable Diffusion、nanobanana 等

**核心公式：**
```
[主体描述] + [构图位置] + [光线逻辑] + [相机视角] + [风格与质感]
```

[查看完整文档](image-design/SKILL.md)

---

### frontend-design

**高保真前端界面设计** - 创建独特、生产级的前端界面，避免"AI 生成"的千篇一律感。

**设计原则：**
- 🎨 **大胆的美学方向** - 极简、极繁、复古未来主义、有机自然等
- ✨ **独特字体选择** - 避免 Arial/Inter 等通用字体
- 🎭 **精心设计的动画** - CSS 动画、滚动触发、悬停效果
- 📐 **非对称布局** - 破格网格、重叠元素、负空间
- 🖼️ **背景与质感** - 渐变网格、噪点纹理、几何图案

**输出：**
生产级、可工作的 HTML/CSS/JS 或 React/Vue 代码

[查看完整文档](.staged-skills/frontend-design/SKILL.md)

---

### de-ai-writing

**文本去AI味** - 用"检测→删除→声纹校准→改写→反查"五步法去除文字中的AI痕迹，保留真实人味。

**五步工作流：**
1. **检测** - 标记八大AI味特征（意义膨胀、公式化过渡、笼统空洞、情感平整等）
2. **删除** - 砍掉空洞修辞、废话铺垫、AI创作声明
3. **声纹校准** - 从用户过往文字中提取具体特征，校准到个人声音
4. **改写** - 注入事实、立场、描述、温度四个方向
5. **反查** - 用你自己的话逐句自问，确保读起来像人说的

**适用场景：**
- 自媒体文章、职场周报、个人随笔
- 产品文案、朋友圈、小红书笔记、邮件
- 任何需要去除机器味的文字

[查看完整文档](de-ai-writing/SKILL.md)

---

### curriculum-design

**专业课程设计与教学设计** - 基于 OBE 成果导向与两性一度标准的课程级和课堂级设计方案输出。

**核心设计理念：**
- **成果导向（OBE）反向设计** - 人才培养目标 → 专业毕业要求 → 课程教学目标 → 教学活动 → 考核评估
- **两性一度标准** - 高阶性（知识+能力+素质三维）、创新性（PBL/TBL/混合式/翻转课堂）、挑战度（形成性评价）
- **布鲁姆认知六层次** - 记忆→理解→应用→分析→评价→创造，每个知识点对应可衡量行为动词

**双层面输出：**
- **课程级** - 教学大纲：需求分析、课程目标、内容组织、教学方法、考核评估
- **课堂级** - 教案：学情分析、教学目标、教学流程（BOPPPS 等）、板书设计、课后反思

**适用场景：**
- 高校教师教学发展、一流课程建设、课程思政设计
- 职业院校课程建设、产教融合方案
- 企业培训课程开发、在线课程设计

[查看完整文档](curriculum-design/SKILL.md)

---

### video-dubbing

**AI 视频配音与翻译** - 完整的视频配音流程，将视频音频翻译成其他语言并保持时间节奏。

**工作流程：**
```
Input Video → Demucs(分离人声) → Whisper(转录) → translate-polisher(精翻) → mlx-tts(合成) → FFmpeg(合并) → Output Video
```

**核心能力：**
- 🔊 **人声分离** - 使用 Demucs 分离人声和背景音乐
- 📝 **AI 转录** - Whisper 自动转录字幕
- 🌐 **高质量翻译** - 集成 translate-polisher 四步精翻
- 🗣️ **音色一致** - 解决 TTS 声音突变问题
- 🎵 **音画同步** - 自动调整字幕时间匹配 TTS 时长
- 🎨 **原字幕遮盖** - 可选遮盖原视频字幕区域

**使用方式：**
```bash
# 分步执行（推荐）
python video_dubbing.py input.mp4 --step extract
python video_dubbing.py input.mp4 --step transcribe
python video_dubbing.py input.mp4 --step translate  # 生成待翻译文件
# 使用 /translate-polisher 翻译后保存为 translated.md
python video_dubbing.py input.mp4 --step synthesize
python video_dubbing.py input.mp4 --step merge

# 一键执行（翻译完成后）
python video_dubbing.py input.mp4 --target-lang zh --voice-prompt "a warm female voice"
```

[查看完整文档](video-dubbing/SKILL.md)

---

### mlx-tts

**Apple Silicon 本地 TTS** - 使用 Qwen3-TTS 模型在 Apple Silicon Mac 上进行高质量本地语音合成。

**核心特性：**
- 🚀 **Apple Neural Engine 优化** - 利用 MLX 框架，推理速度快
- 🎤 **Prompt-based 声音设计** - 通过文本描述定义声音风格，无需参考音频
- 🔒 **完全本地** - 无需云端，无需 API 密钥，完全私密
- 💾 **低内存** - 8-bit 量化，16GB Mac 可运行
- 🌏 **多语言支持** - 支持中文、英文、日文等 20+ 语言

**安装：**
```bash
brew install ffmpeg uv && uv tool install --force "mlx-audio" --prerelease=allow
```

**使用方式：**
```bash
# 基础 TTS
mlx_audio.tts.generate --text "你好" --output-path ./output.wav

# 声音设计
mlx_audio.tts.generate \
  --text "我是明日香" \
  --instruct "a confident teenage girl, flirtatious, seductive edge" \
  --output-path ./asuka.wav

# ASR 语音转文字
mlx_audio.stt.generate --audio ./input.wav --output-path ./transcript.txt --language zh
```

[查看完整文档](mlx-tts/SKILL.md)

---

### hermes-setup

**Hermes Agent 全自动安装与配置** - 从零开始搭建一个自我进化的 AI 个人 Operator（NousResearch）。

**覆盖内容（7 天路线）：**
- 🤖 **安装部署** - 从零到一的完整安装流程
- 🆔 **身份/SOUL.md** - 定义 Agent 人格与行事准则
- 🧠 **模型选择** - GPT/Claude/Qwen 等多模型分层策略
- 💾 **记忆系统** - 持久化记忆与上下文管理
- 📡 **消息网关** - Telegram/Discord/Slack/WhatsApp 多端接入
- ⚡ **Skills 技能系统** - 自定义技能与自动化流程
- ⏰ **Cron 定时任务** - 定时调度与自动化执行
- 🎯 **/goal 自主执行** - 自主目标分解与执行
- 📊 **Dashboard/Kanban** - 可视化看板管理
- 🔒 **安全配置** - Bitwarden、egress 权限控制、多 Profile 隔离

**核心来源：**
- 综合 @zaimiri 7日指南 + @PrajwalTomar_ 深度剖析 + Hermes 官方文档

[查看完整文档](hermes-setup/skill.md)

---

---

### llm-aiops

**LLM + AIOps 研究参考指南** - 基于 [awesome-LLM-AIOps](https://github.com/Jun-jie-Huang/awesome-LLM-AIOps) 论文列表（78+ 篇）提炼的 LLM 应用于 AIOps 的综合参考。

**覆盖领域：**
- 🚨 **故障管理** - 全生命周期管理、事件报告、根因分析（RCA）、缓解、事后分析、AIOps Q&A
- 📋 **日志分析** - LLM 驱动的日志解析、日志异常检测、日志语句生成
- ☁️ **基础设施管理** - 基准测试、基础设施即代码（IaC）、LLM 训练平台诊断

**常见技术路线：**
- **Prompting** - ICL（上下文学习）、CoT（思维链）、ToT（思维树）
- **Fine-tuning** - 领域微调（如 OWL for IT ops）
- **Agent-based** - 工具增强型 LLM、多智能体协作、SOP 引导
- **RAG** - 检索增强生成用于故障解决推荐

**关键系统：**
- RCAgent、mABC、Flow-of-Action — 多智能体根因分析
- Nissist、STRATUS — 生产级故障缓解系统
- AIOpsLab、ITBench — AIOps Agent 评测基准

[查看完整文档](llm-aiops/SKILL.md)

---

## 快速开始

### 环境要求

- 通用 AI 编程助手
- 部分 Skill 需要：
  - Python 3.8+
  - Node.js 14+
  - FFmpeg（video-minutes、video-dubbing）

### 安装依赖

**video-minutes：**
```bash
cd video-minutes
pip install -r requirements.txt
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
```

**skill-security-check：**
```bash
cd skill-security-check
# 无需额外依赖，使用 Node.js 内置功能
```

**video-dubbing：**
```bash
pip install openai-whisper demucs
brew install ffmpeg uv
uv tool install --force "mlx-audio" --prerelease=allow
```

**mlx-tts：**
```bash
brew install ffmpeg uv && uv tool install --force "mlx-audio" --prerelease=allow
```

### 配置

部分 Skill 需要配置 API 密钥：

1. 复制 `.env.example` 到 `.env`（如果有）
2. 填写相应的 API 密钥
3. 运行配置向导（部分 Skill 提供）

---

## 项目结构

```
agent-skills/
├── README.md                      # 本文件
├── LICENSE                        # 开源协议
│
├── blitz/                        # 通用加速学习协议
│   └── SKILL.md
│
├── skill-security-check/         # Skill 安全检查 (TypeScript)
│   ├── src/
│   ├── scripts/
│   ├── SKILL.md
│   └── README.md
│
├── claude-simplify/              # 代码简化与质量检查
│   └── SKILL.md
│
├── claude-remember/              # 自动记忆管理与整理
│   └── SKILL.md
│
├── curriculum-design/           # 专业课程设计与教学设计
│   └── SKILL.md
│
├── article-deconstructor/        # 文章拆解分析
│   ├── references/
│   └── SKILL.md
│
├── video-minutes/               # 视频纪要生成器
│   ├── scripts/
│   ├── templates/
│   └── README.md
│
├── video-dubbing/               # AI 视频配音
│   ├── video_dubbing.py
│   └── SKILL.md
│
├── wechat-article-writer/       # 专业自媒体文章写作
│   └── SKILL.md
│
├── weitoutiao-creator/          # 微头条爆款文案生成
│   └── SKILL.md
│
├── snowflake-novel-writer/      # 雪花写作法小说创作
│   └── SKILL.md
│
├── infocard/                    # 信息卡片生成器 v6.6
│   ├── assets/
│   ├── evals/
│   ├── references/
│   └── SKILL.md
│
├── pdf2md/                      # PDF 转 Markdown 工具
│   ├── pdf2md.py
│   └── SKILL.md
│
├── image-design/                # 高级 AI 图片设计
│   ├── evals/
│   └── SKILL.md
│
├── de-ai-writing/               # 文本去AI味
│   └── SKILL.md
│
├── design-md-extractor/         # URL 设计系统提取器
│   ├── references/
│   └── SKILL.md
│
├── github-analyzer/              # GitHub 项目一键分析
│   └── SKILL.md
│
├── mlx-tts/                     # Apple Silicon 本地 TTS
│   └── SKILL.md
│
├── .staged-skills/              # 待发布技能
│   └── frontend-design/         # 高保真前端设计
│       ├── LICENSE.txt
│       └── SKILL.md
│
├── life-quotes/                 # 人生感悟与金句生成
│   └── SKILL.md
│
├── material-to-slides/          # 资料转 HTML 幻灯片
│   ├── references/
│   └── SKILL.md
│
├── viral-hook/                  # 社交媒体爆款文案生成器
│   └── SKILL.md
│
├── curriculum-design/           # 专业课程设计与教学设计
│   └── SKILL.md
│
├── hermes-setup/                # Hermes Agent 安装配置
│   └── skill.md
│
├── llm-aiops/                   # LLM + AIOps 研究参考
│   └── SKILL.md
│
└── novel-writing/               # 小说创作专业助手
    └── SKILL.md
```

---

### Skill 文档规范

每个 Skill 应包含：
- **SKILL.md** - 完整使用文档（必需）
- **README.md** - 快速入门（可选）
- **scripts/** - 执行脚本（如有代码）
- **references/** - 参考资料（可选）

---

## 贡献指南

欢迎提交新的 Skill 或改进现有 Skill！请确保：

1. 每个 Skill 都有完整的 SKILL.md 文档
2. 遵循现有的目录结构和命名规范
3. 在 README 的 Skill 目录和项目结构中添加新 Skill
4. 如果是脚本型 Skill，提供安装和配置说明

---

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 最近更新 (2026-07-25)

### 批量巡视与优化

- **缺陷修复**: pdf2md 残留代码片段清除、video-minutes 重复"依赖安装"章节删除
- **路径通用化**: pdf2md / infocard / video-minutes 的硬编码平台路径更新为工作区相对路径
- **生态适配**: claude-remember 记忆层级改为通用记忆体系描述，不绑定特定平台；video-minutes 任务分发标签泛化
- **交叉引用**: 为重叠技能对添加互引（de-ai-writing↔viral-hook, novel-writing↔snowflake-novel-writer, wechat-article-writer↔weitoutiao-creator）
- **能力增强**: image-design 添加原生图片生成工具链路说明；pdf2md 添加原生 PDF 读取备选方案
- **README 清理**: 移除已不存在的 attention-daily / seed-article，添加 github-analyzer，去除所有平台特定引用

---

> 💡 **提示**：每个 Skill 都是独立的模块，可以单独使用。建议先阅读各 Skill 的 SKILL.md 了解详细功能和使用方法。
