# Video Minutes

智能视频纪要生成器 - 自动提取视频语音、生成字幕、智能分类总结的高性能工具。

## 🚀 新特性 (v2.0)

### insanely-fast-whisper 集成

基于 [faster-whisper](https://github.com/SYSTRAN/faster-whisper) 的高性能转录，比原始 Whisper **快 2-4 倍**！

**性能对比：**

| 指标 | 原始 Whisper | faster-whisper | 提升 |
|------|--------------|----------------|------|
| **速度** | 1x (基准) | 2-4x ⚡ | **2-4 倍** |
| **内存** | 100% | 50% 💾 | **降低 50%** |
| **精度** | float32 | int8/float16 | **可配置** |
| **VAD** | 无 | 内置 🎙️ | **自动过滤静音** |
| **词级时间戳** | 无 | 支持 ✓ | **逐词定位** |

## 📦 安装

### 1. 安装 ffmpeg

```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt update && sudo apt install ffmpeg

# Windows
winget install Gyan.FFmpeg
```

### 2. 安装 Python 依赖

```bash
cd video-minutes
pip install -r requirements.txt
```

## 🎯 快速开始

### 基本用法

```bash
# 处理单个视频（自动分类）
python scripts/generate_minutes.py meeting.mp4

# 指定视频类型
python scripts/generate_minutes.py lecture.mp4 --type lecture

# 指定输出语言
python scripts/generate_minutes.py interview.mp4 --language zh

# 使用高精度模型
python scripts/generate_minutes.py presentation.mp4 --model medium

# 仅提取字幕
python scripts/generate_minutes.py video.mp4 --transcript-only

# 批量处理目录
python scripts/generate_minutes.py ~/Recordings/ --batch
```

## ⚡ 性能优化

### 配置高性能模式

创建 `~/.opencode/skills/video-minutes/config.yaml`：

```yaml
version: "2.0.0"

output:
  language: auto
  format: markdown
  directory: "~/Documents/video-minutes"

# 🚀 insanely-fast-whisper 配置
whisper:
  model: base              # tiny/base/small/medium/large-v3
  device: auto             # auto/cpu/cuda
  compute_type: int8       # int8/int8_float16/float16/float32
  cpu_threads: 4

content:
  include_summary: true
  include_key_points: true
  include_timeline: true
  include_action_items: true
  include_transcript: true
```

### 模型选择建议

| 模型 | 显存 | 速度 | 适合场景 |
|------|------|------|----------|
| `tiny` | ~1GB | ⚡⚡⚡ | 快速预览 |
| `base` | ~1GB | ⚡⚡ | **推荐**，日常使用 |
| `small` | ~2GB | ⚡ | 较高精度 |
| `medium` | ~5GB | 🐢 | 高精度需求 |
| `large-v3` | ~10GB | 🐢🐢 | 最佳质量 |

### 计算精度说明

- **int8**: 速度最快，内存占用最小，质量损失极小 ⭐ 推荐
- **float16**: 需要 GPU，速度较快
- **float32**: 标准精度，速度最慢

## 🎬 功能特性

- 🤖 **AI 自动分类**: 识别 7 种视频类型（会议/课程/访谈等）
- 📝 **智能总结**: 提取核心要点、行动项、关键决策
- 🏷️ **任务分发**: 通过 @tags 将待办分发给其他 skill
- 🔗 **多源支持**: 本地文件、Zoom/腾讯会议、在线视频
- 🌐 **多语言**: 自动检测语言，支持 99+ 语言
- 📊 **多种输出**: Markdown/Obsidian/Notion/飞书文档

## 📋 支持的视频类型

| 类型 | 特征 | 输出重点 |
|------|------|----------|
| meeting | 多人参与、任务分配 | 待办事项 + 决议 |
| lecture | 课程/讲座 | 知识点图谱 + 时间戳 |
| interview | 问答形式 | Q&A 整理 + 观点对比 |
| presentation | 演讲/汇报 | 核心论点 + 数据 |
| podcast | 播客/对话 | 金句摘录 + 话题索引 |
| tutorial | 教程/演示 | 步骤清单 + 截图提示 |
| note | 个人录屏 | 格式化文本 |

## 🏷️ 任务分发 (@tags)

自动识别并分发任务：
- `@Codex` - 代码任务 → agent-swarm
- `@article` - 写文章 → content-publisher
- `@reminder` - 定时提醒 → cron
- `@research` - 调研 → web_search
- `@design` - 设计 → image-gen

## 📁 项目结构

```
video-minutes/
├── scripts/
│   ├── generate_minutes.py          # 主入口 ⭐
│   ├── insanely_fast_transcriber.py # 高性能转录器 🚀 NEW
│   ├── video_processor.py           # 视频处理
│   ├── classifier.py                # 视频分类
│   └── dispatcher.py                # 任务分发
├── templates/                       # 7种类型模板
├── requirements.txt                 # Python 依赖
├── SKILL.md                         # 完整文档
└── README.md                        # 本文件
```

## 🔧 故障排除

### 模型下载失败

```bash
# 使用 HuggingFace 镜像
export HF_ENDPOINT=https://hf-mirror.com
python scripts/generate_minutes.py video.mp4
```

### 显存不足

```yaml
# 配置更小模型或 int8 量化
whisper:
  model: base
  compute_type: int8
```

### CUDA 不可用

```yaml
# 强制使用 CPU
whisper:
  device: cpu
  compute_type: int8
```

## 📝 更新日志

### v2.0.0 (2026-03-25)
- 🚀 集成 insanely-fast-whisper (faster-whisper)
- ⚡ 速度提升 2-4 倍
- 💾 内存占用降低 50%
- 🎙️ 新增 VAD 语音活动检测
- ✨ 支持词级时间戳

### v1.2.0 (2026-03-21)
- ✅ 7种视频类型自动分类
- ✅ 任务分发系统
- ✅ 多格式输出 (Markdown/Obsidian/Notion/飞书)

## 📄 License

MIT

## 🔗 相关链接

- [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- [insanely-fast-whisper](https://github.com/Vaibhavs10/insanely-fast-whisper)
- [OpenAI Whisper](https://github.com/openai/whisper)

完整文档见 [SKILL.md](SKILL.md)
