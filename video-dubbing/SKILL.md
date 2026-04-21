---
name: video-dubbing
description: Use when translating video audio to another language while preserving timing and rhythm, creating dubbed videos with AI-generated voice using translate-polisher and mlx-tts
---

# Video Dubbing

## Overview

Complete video dubbing pipeline integrating **translate-polisher** (高质量四步精翻) and **mlx-tts** (Apple Silicon 本地 TTS).

**Workflow:**
```
Input Video → Demucs (分离人声) → Whisper (转录) →
translate-polisher (精翻) → mlx-tts (合成) → FFmpeg (合并) → Output Video
```

## Integration Skills

- **translate-polisher**: 四步精翻工作流（分析→初译→审校→终稿），产出出版级翻译
- **mlx-tts**: Qwen3-TTS 本地语音合成，支持 prompt-based 声音设计，无需云端

## Requirements

```bash
# Core tools
pip install openai-whisper demucs
brew install ffmpeg uv

# MLX TTS (macOS Apple Silicon)
uv tool install --force "mlx-audio" --prerelease=allow

# For translation
pip install anthropic  # translate-polisher 使用 Claude API 实现精翻

# 可选：安装带字幕支持的 FFmpeg
brew install ffmpeg --with-libass  # 如果需要硬字幕烧录
```

## Quick Reference

| Step | Tool | Output |
|------|------|--------|
| 1. Extract | `ffmpeg` | `audio.wav` |
| 2. Separate | `demucs` | `vocals.wav`, `no_vocals.wav` |
| 3. Transcribe | `whisper` | `segments.json` |
| 4. Translate | `translate-polisher` | `segments_translated.json` |
| 5. TTS | `mlx-tts` | `dubbed_audio.wav` |
| 6. Merge | `ffmpeg` | `output.mp4` |

## Usage

### 分步执行（推荐）

```bash
# Step 1: 提取音频
python video_dubbing.py input.mp4 --step extract

# Step 2: 分离人声
python video_dubbing.py input.mp4 --step separate

# Step 3: 转录字幕
python video_dubbing.py input.mp4 --step transcribe

# Step 4: 准备翻译文件
python video_dubbing.py input.mp4 --step translate
# 输出提示：请使用 translate-polisher 翻译 to_translate.md

# Step 4b: 使用 translate-polisher 翻译（在 Claude Code 中执行）
/translate --from en --to zh --audience technical --style conversational input_dubbed/to_translate.md
# 将翻译结果保存为 input_dubbed/translated.md

# Step 5: 合成语音
python video_dubbing.py input.mp4 --step synthesize

# Step 6: 合并视频
python video_dubbing.py input.mp4 --step merge
```

### 快捷执行

如果已经完成了翻译步骤（translated.md 已存在）：

```bash
# 一键执行（会自动跳过已完成的步骤）
python video_dubbing.py input.mp4 --target-lang zh

# 自定义声音风格
python video_dubbing.py input.mp4 --voice-prompt "a confident teenage girl, warm and energetic"

# 遮盖原英文字幕区域
python video_dubbing.py input.mp4 --mask-subtitles 100,500,520,80
```

## 关键功能

### 1. 音色一致（解决声音突变问题）

**问题**：mlx-tts 每次调用会重新生成声音特征，导致音色不一致。

**解决方案**：
- 首先生成第一个片段作为**参考音色**
- 后续片段使用 `--ref_audio` 和 `--ref_text` 参数引用参考音色
- 确保整个视频使用同一个人的声音

```python
# 流程
片段1 → 生成参考音频 → 片段2(使用ref) → 片段3(使用ref) → ...
```

### 2. 翻译步骤（使用 translate-polisher）

**不再硬编码 API 调用**，而是生成翻译文件让用户使用 translate-polisher skill 处理：

```bash
# Step 1-3 完成后，脚本会生成 to_translate.md 文件
python video_dubbing.py input.mp4 --step translate

# 输出：
# 待翻译文件已保存: input_dubbed/to_translate.md
# 请执行以下命令进行翻译：
#   /translate --from en --to zh --audience technical --style conversational input_dubbed/to_translate.md

# Step 4: 使用 translate-polisher 翻译
/translate --from en --to zh --audience technical --style conversational input_dubbed/to_translate.md

# 翻译完成后，保存译文到 input_dubbed/translated.md
# 然后继续执行后续步骤

# Step 5-6: 合成语音并合并
python video_dubbing.py input.mp4 --step synthesize
python video_dubbing.py input.mp4 --step merge
```

**translate-polisher 参数说明**：
- `--from en`: 源语言（英文）
- `--to zh`: 目标语言（中文）
- `--audience technical`: 目标读者为技术人员
- `--style conversational`: 翻译风格为口语化

更多参数参考 @translate-polisher skill。

### 3. 剥离原字幕（遮盖原英文字幕）

**问题**：原视频可能包含硬字幕（烧录在视频中的字幕），与新中文字幕重叠。

**解决方案**：
使用 `--mask-subtitles` 参数指定原字幕区域，用黑色块遮盖：

```bash
python video_dubbing.py input.mp4 --mask-subtitles 100,500,520,80
# 格式: x,y,w,h (x坐标,y坐标,宽度,高度)
```

**如何确定字幕区域**：
```bash
# 使用 ffplay 查看视频，确定字幕位置
ffplay -vf "drawgrid=w=100:h=100" input.mp4
```

### 4. 字幕与语音同步

**问题**：TTS 生成的语音时长可能与原字幕时长不一致，导致不同步。

**解决方案**：
- 记录每个片段的**实际 TTS 时长**
- 根据实际时长**重新计算字幕时间**
- 输出同步后的字幕文件 `subtitles_zh_synced.srt`

```python
# 同步逻辑
if TTS时长 > 原时长:
    使用 TTS时长  # 避免字幕提前消失
else:
    使用原时长 × 0.8  # 保留一点静音缓冲
```

## Voice Prompts (mlx-tts)

| 风格 | Prompt |
|------|--------|
| 专业女声 | `a warm, professional female voice, clear and natural` |
| 自信少女 | `a confident teenage girl, energetic and expressive` |
| 温柔女声 | `a warm, gentle female voice, slightly soft` |
| 磁性男声 | `a deep, masculine voice with authority` |
| 新闻播报 | `a professional news anchor, clear and authoritative` |
| 教学讲解 | `a patient educator, clear and encouraging` |
| 激动演讲 | `an energetic public speaker, passionate and enthusiastic` |

更多声音设计参考 mlx-tts skill。
|------|--------|
| 专业女声 | `a warm, professional female voice, clear and natural` |
| 自信少女 | `a confident teenage girl, energetic and expressive` |
| 温柔女声 | `a warm, gentle female voice, slightly soft` |
| 磁性男声 | `a deep, masculine voice with authority` |
| 新闻播报 | `a professional news anchor, clear and authoritative` |
| 教学讲解 | `a patient educator, clear and encouraging` |
| 激动演讲 | `an energetic public speaker, passionate and enthusiastic` |

更多声音设计参考 mlx-tts skill。

## Translation Styles (translate-polisher)

在 `/translate` 命令中使用 `--style` 参数指定：

| 风格 | 说明 |
|------|------|
| `auto` | 根据原文自动匹配风格 |
| `formal` | 专业严谨 |
| `technical` | 精确简洁，术语密集 |
| `conversational` | 口语化，亲切随和 |
| `storytelling` | 叙事流畅，生动 |

## Translation Audiences (translate-polisher)

在 `/translate` 命令中使用 `--audience` 参数指定：

| 读者 | 说明 |
|------|------|
| `general` | 普通读者 |
| `technical` | 开发者/工程师 |
| `academic` | 研究者/学者 |
| `business` | 商务人士 |

## Implementation

See @video_dubbing.py for full implementation.

**Key parameters:**
- `--target-lang`: 目标语言 (zh, en, ja)
- `--voice-prompt`: mlx-tts 声音风格描述
- `--translate-style`: translate-polisher 翻译风格
- `--translate-audience`: 目标读者类型
- `--keep-temp`: 保留中间文件

## Subtitles

脚本会自动生成中文字幕文件 (`subtitles_zh.srt`)，并提供两种输出模式：

### 硬字幕（推荐）
如果 FFmpeg 支持 libass，字幕会直接烧录到视频中：
```bash
brew install ffmpeg --with-libass  # 安装带字幕支持的 FFmpeg
```

### 软字幕（备用）
如果 FFmpeg 不支持字幕烧录，脚本会：
1. 生成配音视频（无字幕）
2. 单独输出 SRT 字幕文件
3. 字幕文件与视频同名，播放器（VLC、IINA）会自动加载

### 手动添加字幕
如果需要硬字幕但 FFmpeg 不支持，可用以下工具：
- **HandBrake**: 导入视频 + SRT 字幕，导出带字幕视频
- **Final Cut Pro / Premiere**: 导入 SRT 作为字幕轨道
- **ffmpeg + libass**: 重新编译 FFmpeg 带字幕支持

保持原视频节奏的关键：

```python
# Whisper 提取的时间信息
segment = {
    "start": 1.52,
    "end": 4.85,
    "text": "Hello world"
}

# translate-polisher: 只翻译文本，保持时间
# mlx-tts: 生成后使用 ffmpeg atempo 调整语速匹配原时长

# 语速调整示例
if tts_duration < original_duration:
    # TTS 太快，放慢语速
    atempo = tts_duration / original_duration  # 如 0.8
else:
    # TTS 太慢，加快语速
    atempo = tts_duration / original_duration  # 如 1.2

# ffmpeg 应用
ffmpeg -i input.wav -filter:a "atempo={atempo}" output.wav
```

## Common Mistakes

| Issue | Cause | Fix |
|-------|-------|-----|
| 翻译质量差 | 使用简单翻译 API | 使用 translate-polisher 四步精翻 |
| 机器音太重 | TTS 参数不当 | 优化 mlx-tts voice prompt |
| 音频不同步 | 时长不匹配 | ffmpeg atempo 自动调整 |
| 中文太长 | 字数比英文多 | 适当加快语速或精简翻译 |
| mlx-tts 失败 | 文本太长 | 自动分块生成 |
| 翻译失败 | API 限制 | 自动降级到 Google Translate |

## Pro Tips

**优化翻译质量：**
```bash
# 针对技术视频使用专业风格
python video_dubbing.py input.mp4 --translate-style technical --translate-audience technical

# 针对故事类视频使用叙事风格
python video_dubbing.py input.mp4 --translate-style storytelling
```

**定制声音：**
```bash
# 教学视频用耐心声音
--voice-prompt "a patient educator, clear and encouraging, moderate pace"

# 新闻视频用专业声音
--voice-prompt "a professional news anchor, clear and authoritative"

# 青少年内容用活力声音
--voice-prompt "an energetic young adult, enthusiastic and friendly"
```

**背景音乐处理：**
```bash
# 原始背景音降低音量后与新配音混合
ffmpeg -i no_vocals.wav -i dubbed_audio.wav -filter_complex \
    "[0:a]volume=0.3[bg];[bg][1:a]amix=inputs=2:duration=longest" \
    final_audio.wav
```

**批量处理：**
```bash
for video in *.mp4; do
    python video_dubbing.py "$video" --target-lang zh \
        --voice-prompt "a warm, professional female voice"
done
```

## See Also

- @mlx-tts - 详细的声音设计和 TTS 使用指南
- @translate-polisher - 四步精翻工作流详解
- https://github.com/Blaizzy/mlx-audio - MLX TTS 项目

