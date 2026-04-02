# Agent Skills Collection

Claude Code 智能技能集合 - 自动化内容创作、社交媒体管理、安全检查与生产力工具箱。

## 项目简介

本项目是一系列为 Claude Code 设计的 Skill（技能）模块，每个 Skill 都是针对特定场景的自动化解决方案。从视频内容处理到社交媒体运营，从文章分析到内容生成，从安全检查到翻译优化，帮助用户提升工作效率，实现智能化创作流程。

## Skill 目录

### 📊 内容策展与分析

| Skill | 描述 | 状态 |
|-------|------|------|
| [attention-daily](#attention-daily) | 每日科技情报报告（GitHub + AttentionVC） | ✅ v2.0 新版 |
| [article-deconstructor](#article-deconstructor) | 文章拆解分析器 | ✅ 可用 |
| [video-minutes](#video-minutes) | 智能视频纪要生成器 | ✅ 可用 |
| [infocard](#infocard) | 智能信息卡片生成器 | ✅ 可用 |
| [pdf2md](#pdf2md) | PDF 转 Markdown 工具 | ✅ 可用 |

### ✍️ 内容创作与生成

| Skill | 描述 | 状态 |
|-------|------|------|
| [twitter-one-liner](#twitter-one-liner) | Twitter/X 推文生成器 | ✅ 可用 |
| [wechat-autopilot](#wechat-autopilot) | 公众号自动化运营系统 | ✅ 可用 |
| [wechat-article-writer](#wechat-article-writer) | 专业自媒体文章写作工具 | ✅ 可用 |
| [gemini-text-to-image](#gemini-text-to-image) | Gemini 文生图工具 | ✅ 可用 |
| [gemini-flash-lite-toolkit](#gemini-flash-lite-toolkit) | Gemini Flash Lite 工具集 | ✅ 可用 |

### 🛡️ 工具与安全

| Skill | 描述 | 状态 |
|-------|------|------|
| [skill-security-check](#skill-security-check) | Skill 安装前安全检查 | ✅ 新版 |
| [translate-polisher](#translate-polisher) | 高质量文章翻译 | ✅ 可用 |
| [claude-simplify](#claude-simplify) | 代码简化与质量检查 | ✅ 可用 |
| [claude-remember](#claude-remember) | 自动记忆管理与整理 | ✅ 可用 |
| [openclaw-install-scripts](#openclaw-install-scripts) | OpenClaw 安装脚本 | 🛠️ 工具 |

### 📚 知识库

| Skill | 描述 | 状态 |
|-------|------|------|
| [fengshuixue](#fengshuixue) | 风水/八字知识库 | 📚 资料 |

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
- 🌈 **多主题配色** - 6 种预设主题（green/blue/purple/orange/pink/dark）
- 📷 **图片导出** - HTML 转 PNG，支持自适应高度

**使用方式：**
```bash
/infocard <URL>                    # 默认 green 主题
/infocard <URL> --theme=blue      # 蓝色主题
/infocard <URL> --theme=purple --width=1200
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

### gemini-text-to-image

**Gemini 文生图工具** - 使用 Google Gemini API 生成图像。

[查看文档](gemini-text-to-image/SKILL.md)

---

### gemini-flash-lite-toolkit

**Gemini Flash Lite 工具集** - 轻量级 AI 工具集合。

[查看文档](gemini-flash-lite-toolkit/SKILL.md)

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

### fengshuixue

**风水/八字知识库** - 传统命理学习资料。

包含内容：
- 风水教学
- 八字知识简易入门

[查看资料](fengshuixue/)

---

### openclaw-install-scripts

**OpenClaw 安装脚本** - 自动化安装工具。

支持平台：
- Windows (.bat)
- macOS (.sh)
- Linux (.sh)

[查看脚本](openclaw-install-scripts/)

---

## 快速开始

### 环境要求

- Claude Code 或兼容的 AI 编程助手
- 部分 Skill 需要：
  - Python 3.8+
  - Node.js 14+
  - FFmpeg（video-minutes）

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
├── attention-daily/              # 每日科技情报报告 ⭐ v2.0
│   ├── scripts/
│   │   ├── github-trending.js    # GitHub 数据获取
│   │   ├── attentionvc-fetcher.js # AttentionVC 数据获取
│   │   ├── article-analyzer.js   # 文章分析模块
│   │   ├── report-generator.js   # 报告生成器
│   │   └── main.js               # 主程序
│   └── SKILL.md
│
├── skill-security-check/         # Skill 安全检查 🛡️
│   ├── scripts/
│   │   └── security-check.js     # 安全检查脚本
│   ├── SKILL.md
│   └── README.md
│
├── claude-simplify/              # 代码简化与质量检查 ✨
│   └── SKILL.md
│
├── claude-remember/              # 自动记忆管理与整理 🧠
│   └── SKILL.md
│
├── translate-polisher/           # 高质量翻译 🌐
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
├── wechat-autopilot/            # 公众号自动化
│   ├── references/
│   └── SKILL.md
│
├── infocard/                    # 信息卡片生成器
│   ├── assets/
│   └── SKILL.md
│
├── twitter-one-liner/           # Twitter 推文生成
│   └── SKILL.md
│
├── gemini-text-to-image/        # Gemini 文生图
│   └── SKILL.md
│
├── gemini-flash-lite-toolkit/   # Gemini 工具集
│   └── SKILL.md
│
├── pdf2md/                      # PDF 转 Markdown 工具 ⭐ 新增
│   ├── scripts/
│   └── README.md
│
├── wechat-article-writer/       # 专业自媒体文章写作 ⭐ 新增
│   └── SKILL.md
│
├── fengshuixue/                 # 风水八字知识
│   └── 风水教学.md
│
└── openclaw-install-scripts/    # 安装脚本
    ├── openclaw-install-windows.bat
    ├── openclaw-install-macos.sh
    └── openclaw-install-linux.sh
```

---

## 最新更新

### 2026-04-02

**新增 Skill** 🎉

- **[claude-simplify](#claude-simplify)** - 代码简化与质量检查工具，自动审查代码复用性、质量和效率问题
- **[claude-remember](#claude-remember)** - 自动记忆管理与整理工具，帮助组织和优化 CLAUDE.md 记忆文件

**Skill 重命名** 📝
- `simplify` → `claude-simplify`
- `remember` → `claude-remember`

---

### 2026-03-30

**新增 Skill** 🎉

- **[pdf2md](#pdf2md)** - PDF 转 Markdown 工具，支持复杂布局、表格、公式、图片提取
- **[wechat-article-writer](#wechat-article-writer)** - 专业自媒体文章写作工具，支持公众号、小红书、知乎、头条等平台

**README 更新** 📝
- 同步所有现有 Skill 到文档
- 更新项目结构说明

---

### 2026-03-25

**attention-daily v2.0** 🎉
- 新增 GitHub Trending 项目获取
- 新增文章多视角分析功能（技术/商业/用户/趋势）
- 新增智能总结和洞察生成
- 支持 Tech 和 AI 分类文章（各10篇）

**skill-security-check** 🛡️
- 新增多语言支持（11种编程语言）
- 11项全面的安全检查
- 生成详细的安全审查报告

**translate-polisher(复制别人的 挺好用就保留到我项目了)** 🌐
- 四步精翻工作流
- 支持中日英三语互译

---

### Skill 文档规范

每个 Skill 应包含：
- **SKILL.md** - 完整使用文档（必需）
- **README.md** - 快速入门（可选）
- **scripts/** - 执行脚本（如有代码）
- **references/** - 参考资料（可选）

---