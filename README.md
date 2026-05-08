# Agent Skills Collection

Claude Code 智能技能集合 - 自动化内容创作、社交媒体管理、安全检查与生产力工具箱。

## 项目简介

本项目是一系列为 Claude Code 设计的 Skill（技能）模块，每个 Skill 都是针对特定场景的自动化解决方案。从视频内容处理到社交媒体运营，从文章分析到内容生成，从安全检查到翻译优化，帮助用户提升工作效率，实现智能化创作流程。

## Skill 目录

### 📊 内容策展与分析

| Skill | 描述 | 状态 |
|-------|------|------|
| [attention-daily](#attention-daily) | 每日科技情报报告（GitHub + AttentionVC） | ✅ v2.0 |
| [article-deconstructor](#article-deconstructor) | 文章拆解分析器 | ✅ 可用 |
| [infocard](#infocard) | 智能信息卡片生成器 | ✅ v5.0 |
| [pdf2md](#pdf2md) | PDF 转 Markdown 工具 | ✅ 可用 |

### ✍️ 内容创作与生成

| Skill | 描述 | 状态 |
|-------|------|------|
| [wechat-autopilot](#wechat-autopilot) | 公众号自动化运营系统 | ✅ 可用 |
| [wechat-article-writer](#wechat-article-writer) | 专业自媒体文章写作工具 | ✅ 可用 |
| [weitoutiao-creator](#weitoutiao-creator) | 微头条爆款文案生成器 | ✅ 可用 |
| [snowflake-novel-writer](#snowflake-novel-writer) | 雪花写作法小说创作助手 | ✅ 可用 |
| [image-design](#image-design) | 高级质感 AI 图片设计 | ✅ 可用 |
| [frontend-design](#frontend-design) | 高保真前端界面设计 | ✅ 可用 |
| [twitter-one-liner](#twitter-one-liner) | Twitter/X 推文生成器 | ✅ 可用 |
| [life-quotes](#life-quotes) | 人生感悟与金句生成 | ✅ 可用 |
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
| [translate-polisher](#translate-polisher) | 高质量文章翻译 | ✅ 可用 |
| [claude-simplify](#claude-simplify) | 代码简化与质量检查 | ✅ 可用 |
| [claude-remember](#claude-remember) | 自动记忆管理与整理 | ✅ 可用 |

---

## Skill 详情

### attention-daily

**每日科技情报报告** - 自动生成综合日报，整合 GitHub Trending 热门项目和 AttentionVC.ai 热门文章分析。

#### ✨ v2.0 新功能

**🔥 Part 1: GitHub 热门项目**
- 获取 GitHub Trending Top 10 开源项目
- 项目语言、Stars、简介一览
- 热门语言统计和趋势分析

**📰 Part 2: 热门文章深度分析**
- 从 AttentionVC.ai 获取 Tech + AI 文章（各10篇）
- **多视角点评**：技术、商业、用户、趋势四个视角
- **智能分析**：关键词提取、热度计算、内容总结

**🎯 智能总结**
- GitHub 项目与社区讨论关联分析
- 热门关键词统计
- 关键趋势和洞察

**使用方式：**
```bash
cd attention-daily/scripts
npm install
npm run daily
```

**输出：**
- 格式：Markdown 报告
- 位置：`scripts/output/daily-report-{date}.md`
- 内容：GitHub 项目 + 文章分析 + 综合总结

[查看完整文档](attention-daily/SKILL.md)

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
- 🧠 **智能内容梳理** - 分析内容类型，自动提取核心要点
- 🎨 **动态布局选择** - 根据内容特征选择最适合的视觉呈现
  - 列表布局（痛点/问题）
  - 代码块（安装步骤/命令）
  - 卡片网格（功能特性/集成方式）
  - 对比布局（方案对比）
- 🌈 **多主题配色** - 7 种预设主题（slate/ocean/sunset/coral/indigo/forest/dark）
- 📷 **图片导出** - HTML 转 PNG，支持自适应高度

**使用方式：**
```bash
/infocard <URL>                       # 默认主题
/infocard <URL> --theme=slate        # Slate 主题
/infocard <URL> --theme=ocean --width=1200
```

[查看完整文档](infocard/SKILL.md)

---

### twitter-one-liner

**一句话生成高质量 Twitter/X 推文。**

**输出格式：**
- 🎯 **直击型** - 简短有力，直接表达核心观点
- 📖 **故事型** - 加入个人经历、情感或叙事
- 💡 **价值型** - 提供实用建议、技巧或 insights

**使用方式：**
直接输入主题或想法，例如："关于早起的好处"

[查看完整文档](twitter-one-liner/SKILL.md)

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

### wechat-autopilot

**微信公众号自动化运营系统** - 全自动收集资讯、AI 生成文章、AI 配图、自动发布。

**核心功能：**
- 📰 Google News RSS 自动抓取资讯
- ✍️ AI 整理改写，支持多种写作风格
- 🎨 文生图 API 自动生成封面+正文配图
- 📤 微信公众号 API 自动发文
- ⏰ 可设置每日定时执行

**使用方式：**
```bash
/wechat-autopilot setup    # 初始化配置
/wechat-autopilot run      # 立即运行
/wechat-autopilot daily    # 启动定时任务
```

**案例效果：**
- 每篇文章成本：约 ¥1-1.5（API 费用）
- 平均阅读量：300-500
- 爆文记录：10w+、1.8w+

[查看完整文档](wechat-autopilot/SKILL.md)

---

### skill-security-check

**Skill 安装前安全检查** - 全面的安全检查工具，支持多种编程语言。

**支持语言：**
JavaScript/TypeScript, Python, Rust, Java, Go, C/C++, Ruby, PHP, Shell, PowerShell, Perl

**11项安全检查：**
1. ✅ 数据外泄 - 检查外部服务器通信
2. ✅ 凭证访问 - 检查环境变量访问
3. ✅ 文件系统越界 - 检查文件操作范围
4. ✅ 身份文件访问 - 检查敏感文件访问
5. ✅ 动态代码执行 - 检查 eval/exec/subprocess
6. ✅ 权限提升 - 检查 sudo/chmod/chown
7. ✅ 持久化机制 - 检查后台驻留
8. ✅ 运行时安装 - 检查依赖声明
9. ✅ 代码混淆 - 检查代码可读性
10. ✅ 进程侦察 - 检查系统扫描
11. ✅ 浏览器会话访问 - 检查自动化配置

**使用方式：**
```bash
node scripts/security-check.js <skill-path>
```

**报告格式：**
- 风险等级：🟢 LOW / 🟡 MEDIUM / 🔴 HIGH
- 最终评级：✅ SAFE / ⚠️ REVIEW_NEEDED / ❌ UNSAFE
- 安全优势 + 注意事项 + 风险分析

[查看完整文档](skill-security-check/README.md)

---

### translate-polisher

**高质量文章翻译** - 采用"分析→初译→审校→终稿"四步精翻工作流。

**支持语言：**
- 中文 ↔ 英文
- 中文 ↔ 日文

**工作流程：**
1. **分析** - 理解原文语境和风格
2. **初译** - 完成第一版翻译
3. **审校** - 优化表达和术语
4. **终稿** - 润色输出最终版本

**使用方式：**
```
/translate-polisher <text or URL>
```

[查看完整文档](translate-polisher/SKILL.md)

---

### claude-simplify

**代码简化与质量检查** - 审查变更代码的可复用性、质量和效率，并修复发现的问题。

**功能特性：**
- 🔍 **代码复用审查** - 检查是否有现有工具/辅助函数可替代新代码
- ✨ **代码质量审查** - 识别冗余状态、参数蔓延、重复代码、不良抽象等问题
- ⚡ **效率审查** - 发现不必要的工作、错失的并发机会、内存泄漏等

**使用方式：**
```
/claude-simplify [可选: 关注区域]
```

**触发短语：**
- "simplify this"
- "review my changes"
- "clean up the code"
- "check for issues"
- "refactor"
- "code review"
- "optimize"

[查看完整文档](claude-simplify/SKILL.md)

---

### claude-remember

**自动记忆管理与整理** - 审查自动记忆条目并提议提升到 CLAUDE.md、CLAUDE.local.md 或共享记忆中。同时检测过时、冲突和重复的记忆条目。

**功能特性：**
- 📋 **记忆分类** - 自动分类记忆条目到合适的存储位置
- 🔍 **重复检测** - 识别跨记忆层的重复条目
- ⚠️ **冲突识别** - 检测不同记忆层之间的冲突
- 🧹 **清理建议** - 提议删除过时或重复的记忆

**使用方式：**
```
/claude-remember [可选: 关注区域或特定记忆]
```

**触发短语：**
- "review my memories"
- "organize memories"
- "promote to CLAUDE.md"
- "clean up memories"
- "memory review"
- "check for duplicate memories"
- "what should go in CLAUDE.md"

[查看完整文档](claude-remember/SKILL.md)

---

### pdf2md

**PDF 转 Markdown 工具** - 高质量 PDF 转换器，支持复杂布局、表格、公式、图片提取。

**核心能力：**
- 📄 **高质量转换** - 基于 OpenDataLoader PDF - Benchmark #1 准确率
- 📊 **复杂布局支持** - 处理多栏、表格、图文混排
- 🔢 **公式识别** - 支持数学公式转换为 LaTeX/Markdown
- 🖼️ **图片提取** - 自动提取并保存文档中的图片
- 📑 **大文件处理** - 自动分页处理超大文档

**使用方式：**
```bash
/pdf2md <pdf路径>
/pdf2md <pdf路径> --output=./output
/pdf2md <pdf路径> --mode=fast          # 快速模式
/pdf2md <pdf路径> --mode=hybrid        # 混合模式（推荐）
/pdf2md <pdf路径> --extract-images=true
/pdf2md <pdf路径> --ocr-lang=chi_sim   # OCR 中文
```

[查看完整文档](pdf2md/README.md)

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

## 快速开始

### 环境要求

- Claude Code 或兼容的 AI 编程助手
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

**attention-daily：**
```bash
cd attention-daily/scripts
npm install
```

**skill-security-check：**
```bash
cd skill-security-check
# 无需额外依赖，使用 Node.js 内置功能
```

**translate-polisher：**
```bash
# 直接使用，无需安装
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
├── attention-daily/              # 每日科技情报报告
│   ├── scripts/
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
├── translate-polisher/           # 高质量翻译
│   ├── SKILL.md
│   └── references/
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
├── wechat-autopilot/            # 公众号自动化
│   ├── references/
│   ├── assets/
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
├── infocard/                    # 信息卡片生成器 v5.0
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
├── mlx-tts/                     # Apple Silicon 本地 TTS
│   └── SKILL.md
│
├── .staged-skills/              # 待发布技能
│   └── frontend-design/         # 高保真前端设计
│       ├── LICENSE.txt
│       └── SKILL.md
│
├── twitter-one-liner/           # Twitter 推文生成
│   └── SKILL.md
│
├── life-quotes/                 # 人生感悟与金句生成
│   └── SKILL.md
│
├── viral-hook/                  # 社交媒体爆款文案生成器
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

> 💡 **提示**：每个 Skill 都是独立的模块，可以单独使用。建议先阅读各 Skill 的 SKILL.md 了解详细功能和使用方法。
