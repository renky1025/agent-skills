---
name: video-dubbing
description: >
  Translate video/audio content into another language with dubbed voice and synchronized subtitles.
  Use this skill whenever the user asks to: translate a video, dub a video into another language,
  generate foreign-language voiceover for a video, add translated subtitles with dubbed audio,
  or any workflow involving ASR → translate → TTS → video composition.
  Also trigger when the user mentions replacing audio track with translated narration,
  or syncing subtitles with generated dubbing.
---

# Video Dubbing & Subtitle Sync

Complete workflow for translating video/audio content into another language with dubbed voice and precisely synchronized subtitles.

## Overview

This skill produces a final video where:
- The original audio is replaced by AI-generated dubbing in the target language
- Hardcoded subtitles appear exactly when the dubbed words are spoken
- The video duration matches the original (or is explicitly controlled)

## Critical Insight

**Never reuse the original subtitle timestamps for translated text.**
Translated text has different length, word count, and speaking rhythm. If you burn subtitles using the original English timestamps while playing Chinese dubbing, the subtitles will appear 3–5 seconds too early (or too late).

The correct approach:
1. Generate the dubbed audio first
2. Run ASR on the **generated dubbing** to obtain its real timestamps
3. Use those real timestamps for the translated subtitles
4. Then burn them into the video

## Workflow

### 1. Extract Original Subtitles

Use `whisper` on the original audio to get the source transcript and baseline timing:

```bash
whisper original_audio.m4a \
  --model turbo \
  --language <source_lang> \
  --output_format all \
  --output_dir .
```

Outputs: `.srt`, `.txt`, `.json`, `.vtt`, `.tsv`

### 2. Translate the Text

Translate the full transcript into the target language. Preserve paragraph/sentence boundaries so the text flows naturally when spoken.

Save as `transcript_<lang>.txt`.

### 3. Generate Dubbed Audio

Generate the full narration in one pass using TTS (e.g., mlx-tts, edge-tts, etc.). Use natural speed (do not slow down or speed up at generation time).

```bash
mlx_audio.tts.generate \
  --model mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-8bit \
  --text "$(cat transcript_zh.txt)" \
  --instruct "a professional narrator, clear and authoritative" \
  --speed 1.0 \
  --output_path dubbing_raw.wav
```

> **Why one pass?** Generating the entire text at once preserves natural prosody, pauses, and intonation across sentence boundaries. Splitting into chunks creates audible seams.

### 4. Adjust Dubbing Duration to Match Video

Measure the raw dubbing duration and the original video duration:

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 dubbing_raw.wav/audio_000.wav
ffprobe -v error -show_entries format=duration -of csv=p=0 original_video.mp4
```

Use `ffmpeg atempo` to stretch or compress the entire dubbing track:

```bash
# Example: raw=87.4s, target=77.5s → atempo = 87.4 / 77.5 = 1.128
ffmpeg -y -i dubbing_raw.wav/audio_000.wav \
  -af "atempo=<ratio>" \
  -ar 24000 \
  dubbing_adjusted.wav
```

> **Why atempo?** It changes speed without altering pitch, so the voice still sounds natural.

### 5. Obtain Real Subtitle Timestamps (The Key Step)

Run ASR on the **adjusted dubbing audio** to get timestamps that match what the listener actually hears:

```bash
whisper dubbing_adjusted.wav \
  --model turbo \
  --language <target_lang> \
  --output_format srt \
  --output_dir .
```

This produces `dubbing_adjusted.srt` with real timestamps.

### 6. Replace ASR Text with Correct Translation

The ASR output may contain recognition errors (e.g., "试用范围" instead of "适用范围"). Replace each subtitle segment's text with your carefully translated text, **keeping the ASR timestamps intact**.

Save the result as `subtitle_<lang>_synced.srt`.

> **Rule:** Timestamps come from the dubbing ASR. Text comes from your human-reviewed translation. Never the other way around.

### 7. Merge Audio and Video

```bash
ffmpeg -y -i original_video.mp4 -i dubbing_adjusted.wav \
  -c:v copy -c:a aac -shortest output_temp.mp4
```

### 8. Burn Subtitles into Video

Use `moviepy` (or ffmpeg with libass if available) to hardcode the synced subtitles:

```bash
python3 -m venv venv
source venv/bin/activate
pip install moviepy
python3 burn_subtitles.py
```

Helper script (`scripts/burn_subtitles.py`):

```python
#!/usr/bin/env python3
import re
from moviepy import VideoFileClip, TextClip, CompositeVideoClip

def parse_srt(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    blocks = re.split(r'\n\s*\n', content.strip())
    subtitles = []
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            time_line = lines[1]
            text = '\n'.join(lines[2:])
            match = re.match(r'(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)', time_line)
            if match:
                h1, m1, s1, ms1, h2, m2, s2, ms2 = map(int, match.groups())
                start = h1 * 3600 + m1 * 60 + s1 + ms1 / 1000.0
                end = h2 * 3600 + m2 * 60 + s2 + ms2 / 1000.0
                subtitles.append((start, end, text.strip()))
    return subtitles

if __name__ == "__main__":
    video = VideoFileClip("output_temp.mp4")
    subs = parse_srt("subtitle_zh_synced.srt")
    clips = [video]
    W, H = video.size
    duration = video.duration

    for start, end, text in subs:
        if start >= duration:
            break
        end = min(end, duration)
        txt_clip = TextClip(
            text=text,
            font="/System/Library/Fonts/PingFang.ttc",
            font_size=48,
            color="white",
            stroke_color="black",
            stroke_width=2,
            method="caption",
            size=(W - 120, None),
            text_align="center",
            horizontal_align="center",
            vertical_align="bottom"
        )
        txt_clip = txt_clip.with_position(("center", H - txt_clip.h - 120))
        txt_clip = txt_clip.with_start(start).with_end(end)
        clips.append(txt_clip)

    final = CompositeVideoClip(clips, size=video.size)
    final = final.with_audio(video.audio)
    final.write_videofile("output_final.mp4", codec="libx264", audio_codec="aac", fps=video.fps, preset="fast")
```

### 9. Verify

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 output_final.mp4
```

Duration should match the original video (or the adjusted dubbing).

## Common Mistakes to Avoid

| Mistake | Why It Fails | Correct Approach |
|---------|-------------|------------------|
| Reuse original timestamps for translated subtitles | Text length and rhythm differ across languages | Re-ASR the dubbed audio for real timestamps |
| Generate TTS sentence-by-sentence and concatenate | Audible seams, unnatural pauses | Generate the entire script in one pass |
| Adjust TTS speed parameter to match duration | Speeds above ~1.3x or below ~0.7x sound robotic | Generate at natural speed, then use `ffmpeg atempo` |
| Burn subtitles with ffmpeg `subtitles=` filter | Requires libass; often missing in default ffmpeg builds | Use moviepy or install ffmpeg with `--enable-libass` |
| Forget to clip subtitles that exceed video duration | moviepy crashes or renders empty frames | Cap `end = min(end, video.duration)` |

## Dependencies

- `ffmpeg` (with standard filters)
- `whisper` (OpenAI Whisper or compatible)
- `mlx-audio` / `edge-tts` / any TTS engine
- `moviepy` (for subtitle burning if ffmpeg lacks libass)
- Python 3 with ` Pillow`

## Output Files

| File | Description |
|------|-------------|
| `output_final.mp4` | Final video with dubbed audio + hardcoded subtitles |
| `subtitle_<lang>_synced.srt` | Synced subtitles matching the dubbed audio |
| `dubbing_adjusted.wav` | Time-stretched/compressed dubbing track |

## Example Trigger Phrases

- "把这段视频翻译成中文并配音"
- "Extract English subtitles, translate to Chinese, generate new dubbing"
- "给这个视频加上日语配音和字幕"
- "Replace the audio with Spanish narration and burn captions"
