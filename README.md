# Agent Skills Collection

Claude Code 智能技能集合 - 自动化内容创作、社交媒体管理与生产力工具箱。

## 项目简介

本项目是一系列为 Claude Code 设计的 Skill（技能）模块，每个 Skill 都是针对特定场景的自动化解决方案。从视频内容处理到社交媒体运营，从文章分析到内容生成，帮助用户提升工作效率，实现智能化创作流程。

## Skill 目录

| Skill | 描述 | 状态 |
|-------|------|------|
| [video-minutes](#video-minutes) | 智能视频纪要生成器 | ✅ 可用 |
| [wechat-autopilot](#wechat-autopilot) | 公众号自动化运营系统 | ✅ 可用 |
| [twitter-one-liner](#twitter-one-liner) | Twitter/X 推文生成器 | ✅ 可用 |
| [attention-daily](#attention-daily) | 每日内容策展报告 | ✅ 可用 |
| [article-deconstructor](#article-deconstructor) | 文章拆解分析器 | ✅ 可用 |
| [infocard](#infocard) | 智能信息卡片生成器 | ✅ 可用 |
| [gemini-text-to-image](#gemini-text-to-image) | Gemini 文生图工具 | ✅ 可用 |
| [gemini-flash-lite-toolkit](#gemini-flash-lite-toolkit) | Gemini Flash Lite 工具集 | ✅ 可用 |
| [fengshuixue](#fengshuixue) | 风水/八字知识库 | 📚 资料 |
| [openclaw-install-scripts](#openclaw-install-scripts) | OpenClaw 安装脚本 | 🛠️ 工具 |

---

## Skill 详情

### video-minutes

智能视频纪要生成器 - 自动提取视频语音、生成字幕、智能分类总结。

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

### wechat-autopilot

微信公众号自动化运营系统 - 全自动收集资讯、AI 生成文章、AI 配图、自动发布。

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

### twitter-one-liner

一句话生成高质量 Twitter/X 推文。

**输出格式：**
- 🎯 **直击型** - 简短有力，直接表达核心观点
- 📖 **故事型** - 加入个人经历、情感或叙事
- 💡 **价值型** - 提供实用建议、技巧或 insights

**使用方式：**
直接输入主题或想法，例如："关于早起的好处"

[查看完整文档](twitter-one-liner/SKILL.md)

---

### attention-daily

每日 Twitter/X 内容策展 - 从 AttentionVC.ai 获取热门 AI、Crypto、Tech 文章，生成日报和高互动性帖子。

**功能：**
1. 获取 AttentionVC.ai 热门文章（AI/Crypto/Tech）
2. 分析互动数据（浏览量、点赞、回复、转发）
3. 生成格式化日报报告
4. 创建 5 种不同角度的发帖方案

**使用方式：**
```bash
cd attention-daily/scripts && npm install
npm run daily
```

[查看完整文档](attention-daily/SKILL.md)

---

### article-deconstructor

文章拆解器 - 分析高流量文章的核心要素，提取结构、说服策略、情绪触发点和金句。

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

### infocard

智能信息卡片生成器 - 从 URL 提取内容，自动生成可定制样式的信息卡片图片。

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

**示例：**
```bash
# 生成产品功能介绍卡片
/infocard https://example.com/product --theme=blue

# 生成 Twitter 内容总结卡片
/infocard https://x.com/user/status/xxx --theme=purple
```

[查看完整文档](infocard/SKILL.md)

---

### gemini-text-to-image

Gemini 文生图工具 - 使用 Google Gemini API 生成图像。

[查看文档](gemini-text-to-image/SKILL.md)

---

### gemini-flash-lite-toolkit

Gemini Flash Lite 工具集 - 轻量级 AI 工具集合。

[查看文档](gemini-flash-lite-toolkit/SKILL.md)

---

### fengshuixue

风水/八字知识库 - 传统命理学习资料。

包含内容：
- 风水教学
- 八字知识简易入门

[查看资料](fengshuixue/)

---

### openclaw-install-scripts

OpenClaw 安装脚本 - 自动化安装工具。

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

### 配置

部分 Skill 需要配置 API 密钥：

1. 复制 `.env.example` 到 `.env`（如果有）
2. 填写相应的 API 密钥
3. 运行配置向导（部分 Skill 提供）

---

## 项目结构

```
agent-skills/
├── README.md                 # 本文件
├── LICENSE                   # 开源协议
├── video-minutes/           # 视频纪要生成器
│   ├── scripts/             # Python 脚本
│   ├── templates/           # 输出模板
│   └── README.md
├── wechat-autopilot/        # 公众号自动化
│   ├── references/          # 参考文档
│   └── SKILL.md
├── twitter-one-liner/       # Twitter 推文生成
│   └── SKILL.md
├── attention-daily/         # 每日内容策展
│   ├── scripts/             # Node.js 脚本
│   └── SKILL.md
├── article-deconstructor/   # 文章拆解分析
│   ├── references/          # 分析维度文档
│   └── SKILL.md
├── infocard/                # 信息卡片生成器
│   ├── assets/              # HTML 模板和截图工具
│   ├── references/          # 布局规范文档
│   └── SKILL.md
├── gemini-text-to-image/    # Gemini 文生图
├── gemini-flash-lite-toolkit/  # Gemini 工具集
├── fengshuixue/             # 风水八字知识
└── openclaw-install-scripts/  # 安装脚本
```

---

## 贡献指南

欢迎贡献新的 Skill 或改进现有 Skill！

### 添加新 Skill 的步骤

1. 创建新的目录 `your-skill-name/`
2. 编写 `SKILL.md` 文档，包含：
   - Skill 名称和描述
   - 使用方法
   - 配置说明
   - 示例输出
3. 如有代码，放入 `scripts/` 目录
4. 更新本 README 的 Skill 目录

### Skill 文档规范

每个 Skill 应包含：
- **SKILL.md** - 完整使用文档（必需）
- **README.md** - 快速入门（可选）
- **scripts/** - 执行脚本（如有代码）
- **references/** - 参考资料（可选）

---

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 相关链接

- [Claude Code 文档](https://docs.anthropic.com/en/docs/claude-code/overview)
- [Claude 官方文档](https://docs.anthropic.com/)
- [Claude Code 社区](https://github.com/anthropics/claude-code)

---

<p align="center">
  Built with ❤️ for Claude Code
</p>
