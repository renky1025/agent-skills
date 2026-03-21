# Video Minutes

智能视频纪要生成器 - 自动提取视频语音、生成字幕、智能分类总结，输出结构化纪要文档。

## 功能特性

- 🤖 **AI 自动分类**: 识别 7 种视频类型（会议/课程/访谈等）
- 📝 **智能总结**: 提取核心要点、行动项、关键决策
- 🏷️ **任务分发**: 通过 @tags 将待办分发给其他 skill
- 🔗 **多源支持**: 本地文件、Zoom/腾讯会议、在线视频
- 🌐 **多语言**: 自动检测语言，支持 99+ 语言
- 📊 **多种输出**: Markdown/Obsidian/Notion/飞书文档

## 快速开始

### 安装依赖

```bash
# 安装 ffmpeg
brew install ffmpeg  # macOS
# sudo apt install ffmpeg  # Ubuntu

# 安装 Python 依赖
pip install -r requirements.txt
```

### 首次使用

```bash
# 运行配置向导
python scripts/config_wizard.py

# 或者直接处理视频（会自动提示配置）
python scripts/generate_minutes.py meeting.mp4
```

### 基本用法

```bash
# 处理单个视频（自动分类）
python scripts/generate_minutes.py meeting.mp4

# 指定类型
python scripts/generate_minutes.py lecture.mp4 --type lecture

# 批量处理目录
python scripts/generate_minutes.py ~/Recordings --batch

# 仅提取字幕
python scripts/generate_minutes.py video.mp4 --transcript-only

# 查看更多选项
python scripts/generate_minutes.py --help
```

## 支持的视频类型

| 类型 | 特征 | 输出重点 |
|------|------|----------|
| meeting | 多人参与、任务分配 | 待办事项 + 决议 |
| lecture | 课程/讲座 | 知识点图谱 + 时间戳 |
| interview | 问答形式 | Q&A 整理 + 观点对比 |
| presentation | 演讲/汇报 | 核心论点 + 数据 |
| podcast | 播客/对话 | 金句摘录 + 话题索引 |
| tutorial | 教程/演示 | 步骤清单 + 截图提示 |
| note | 个人录屏 | 格式化文本 |

## 任务分发 (@tags)

自动识别并分发任务：
- `@Codex` - 代码任务 → agent-swarm
- `@article` - 写文章 → content-publisher
- `@reminder` - 定时提醒 → cron
- `@research` - 调研 → web_search
- `@design` - 设计 → image-gen

## 配置

配置文件位置：`~/.opencode/skills/video-minutes/config.yaml`

```yaml
output:
  language: auto
  format: obsidian
  directory: ~/Documents/video-minutes

whisper:
  model: base  # tiny/base/small/medium/large

dispatch:
  confirm_before_dispatch: true

scanning:
  enabled: true
  paths:
    - ~/Documents/Zoom
```

## 目录结构

```
video-minutes/
├── SKILL.md                 # 完整文档
├── README.md               # 本文件
├── templates/              # 7种类型模板
├── scripts/                # 核心脚本
│   ├── generate_minutes.py # 主入口
│   ├── config_manager.py   # 配置管理
│   ├── classifier.py       # 视频分类
│   ├── video_processor.py  # 处理流程
│   └── dispatcher.py       # 任务分发
└── references/             # 参考文档
```

## 相关 Skill

- `agent-swarm` - 接收代码任务
- `content-publisher` - 文章发布
- `elyfinn-voice-notes` - 语音备忘录 (姊妹 skill)

## 版本

v1.2.0 - 2026-03-21

完整文档见 [SKILL.md](SKILL.md)
