# Video Minutes Skill

## 描述
输入任意视频文件，自动提取语音、生成字幕、梳理总结，最终生成结构化的视频纪要 Markdown 文档。

## 工作流程
1. **提取音频**：使用 ffmpeg 从视频中提取音频
2. **语音转文字**：使用 Whisper 将音频转为字幕文本
3. **智能总结**：分析字幕内容，提取核心要点
4. **生成纪要**：输出结构化的 Markdown 文档

## 前置依赖
- ffmpeg (必需)
- Python 3.8+
- openai-whisper

## 安装依赖
```bash
# 安装 ffmpeg (Windows)
winget install Gyan.FFmpeg

# 安装 Python 依赖
pip install openai-whisper
```

## 使用方法

### 基本用法
```bash
# 生成视频纪要
python .opencode/skills/video-minutes/generate_minutes.py <视频文件路径>

# 示例
python .opencode/skills/video-minutes/generate_minutes.py meeting.mp4
```

### 高级选项
```bash
# 指定输出文件名
python .opencode/skills/video-minutes/generate_minutes.py meeting.mp4 -o report.md

# 指定语言 (zh/en/ja 等)
python .opencode/skills/video-minutes/generate_minutes.py meeting.mp4 --language zh

# 使用不同的 Whisper 模型 (tiny/base/small/medium/large)
python .opencode/skills/video-minutes/generate_minutes.py meeting.mp4 --model medium
```

## 输出格式
生成的 Markdown 文档包含：
- **视频基本信息**：文件名、时长、处理时间
- **内容摘要**：一句话总结视频核心内容
- **核心要点**：分点列出关键信息（有理有据，引用原文字幕）
- **详细时间线**：按时间分段的关键内容
- **行动项**：（如检测到）待办事项或决议
- **原文字幕**：完整的转录文本（可选）

## 配置文件
创建 `~/.video-minutes-config.json` 可自定义：
```json
{
  "default_model": "base",
  "default_language": "zh",
  "include_full_transcript": true,
  "max_summary_points": 10
}
```
