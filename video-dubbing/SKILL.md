---
name: video-dubbing
description: >
  Translate video/audio content into another language with dubbed voice and synchronized subtitles.
  Use this skill whenever the user asks to: translate a video, dub a video, generate foreign-language voiceover for a video,
  add translated subtitles with dubbed audio, or any workflow involving ASR → translate → TTS → video composition.
---

# Video Dubbing & Subtitle Sync

Complete workflow: **ASR → translate → TTS → merge audio → burn subtitles**

## Pipeline

```
视频 → 抽音轨(16kHz) → ASR(whisper) → AI翻译 → TTS(dub_segments) → 合并音轨 → 烧录硬字幕
```

## Workflow

### 0. Prerequisite Check

Ensure whisper + moviepy + mlx-audio are installed:

```bash
pip install openai-whisper moviepy 2>/dev/null
# mlx_audio for TTS:
pip install mlx-audio 2>/dev/null  # Apple Silicon
```

### 1. Extract Audio & Transcribe (ASR)

Extract 16kHz mono audio, then run whisper for **accurate per-segment timestamps**:

```bash
ffmpeg -y -i input.mp4 -ar 16000 -ac 1 -c:a pcm_s16le audio16k.wav

whisper audio16k.wav \
  --model large-v3-turbo \
  --language <source_lang> \
  --output_format srt \
  --output_dir .
```

Output: `audio16k.srt` with native timestamps matching the video.

> Use `large-v3-turbo` for best accuracy. If you want even better Chinese recognition, install Qwen3-ASR (`pip install qwen-asr`) and use `scripts/qwen3_asr.py` instead.

### 2. Translate Subtitles (AI does this)

Read the SRT, translate each segment's text into the target language. **Output one line per SRT segment**, preserving order exactly.

- Count SRT segments first (e.g. 27 segments → 27 translated lines)
- Save as `translated.txt` in the working directory
- Verify line count matches SRT segment count before proceeding

### 3. Generate Dubbed Audio

```bash
python3 scripts/dub_segments.py audio16k.srt translated.txt dubbing.wav subtitle_synced.srt --lang <target_lang>
```

What it does:
- Generates TTS per segment with **voice consistency** (first segment = voice reference)
- **Preserves original timestamps** — subtitles stay synced with video
- Smart speed adjustment: only adjusts segments that overflow their slot (atempo 0.88–1.20)
- Bridges adjacent gaps <1s for natural flow

### 4. Merge Dubbed Audio into Video

```bash
ffmpeg -y \
  -i input.mp4 \
  -i dubbing.wav \
  -map 0:v:0 -map 1:a:0 \
  -c:v copy -c:a aac -b:a 192k \
  -shortest \
  output_temp.mp4
```

Verify audio replaced:
```bash
ffprobe -v error -show_entries stream=codec_type -of csv=p=0 output_temp.mp4
# Should show: video, audio
```

### 5. Burn Hard Subtitles into Video

```bash
python3 scripts/burn_subtitles.py output_temp.mp4 subtitle_synced.srt output_final.mp4
```

This renders translated subtitles permanently into the video frame (hardcoded).

### 6. Cleanup (Optional)

```bash
rm -f audio16k.wav audio16k.srt translated.txt dubbing.wav subtitle_synced.srt output_temp.mp4
```

## Output Files

| File | Description |
|------|-------------|
| `output_final.mp4` | Final video with dubbed audio + hardcoded subtitles |
| `subtitle_synced.srt` | Synced subtitles (original timestamps + translated text) |
| `dubbing.wav` | Per-segment aligned dubbing track |

## Key Design Decisions

| Principle | Why |
|-----------|-----|
| **Preserve original ASR timestamps** | They match the video's visual cues natively. Re-ASR on dubbing drifts. |
| **Per-segment speed adjustment** (0.88–1.20x) | Global atempo on the whole dubbing sounds robotic. Per-segment is natural. |
| **Hard subtitles (burned in)** | Soft subtitles don't work on all platforms. Burn them so they always show. |
| **16kHz mono for ASR** | Whisper expects this. Higher sample rate wastes compute without improving accuracy. |
| **Voice consistency via first segment reference** | mlx-tts supports `--ref_audio`. First segment sets the voice for all others. |
| **No Demucs by default** | For typical narration/speech videos, background music removal is unnecessary overhead. |
| **large-v3-turbo model** | Best accuracy/speed tradeoff. Significantly better than `base` for proper nouns and fast speech. |

## Dependencies

| Component | Install | Purpose |
|-----------|---------|---------|
| `ffmpeg` | `brew install ffmpeg` | Audio extraction, merging |
| `openai-whisper` | `pip install openai-whisper` | Speech-to-text (ASR) |
| `moviepy` | `pip install moviepy` | Burn subtitles into video |
| `mlx-audio` | `pip install mlx-audio` | TTS on Apple Silicon |
| `qwen-asr` | `pip install qwen-asr` (optional) | Better Chinese ASR |

## Common Mistakes to Avoid

| Mistake | Why It Fails | Correct Approach |
|---------|-------------|------------------|
| ffmpeg without `-map` | Picks original audio (video source's audio stream), dubbing ignored | Always use `-map 0:v:0 -map 1:a:0` |
| Global atempo on entire dubbing | All speech slows uniformly (EN→ZH ~0.8x), sounds robotic | Per-segment alignment (dub_segments.py) |
| Re-ASR on dubbed audio for timestamps | Timestamps drift from visual cues | Reuse original Step 1 timestamps |
| Translation line count ≠ SRT segments | `dub_segments.py` requires strict 1:1 mapping | Count SRT segments first, match exactly |
| Use whisper `base`/`tiny` model | Proper nouns wrong, fast speech missed | Use `large-v3-turbo` or `turbo` |
| Burn subtitles without checking FFmpeg libass | `subtitles=` filter silently fails | Use `scripts/burn_subtitles.py` (moviepy) |
| Translate segments out of order | Subtitles play at wrong times | Keep segment order: 1 translated line per SRT segment |
| Skip verification | Audio may not have been replaced | Run ffprobe to check both audio + video streams exist |
