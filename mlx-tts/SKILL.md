---
name: mlx-tts
description: Use when needing to generate speech audio from text files on Apple Silicon Mac using Qwen3-TTS (MLX framework, fast, prompt-based voice design)
---

# MLX TTS (Qwen3-TTS)

High-quality local text-to-speech synthesis for Apple Silicon Macs using Qwen3-TTS via MLX framework. Optimized for Apple Neural Engine, runs entirely on-device.

## Overview

Qwen3-TTS is a 1.7B parameter TTS model optimized for Apple Silicon (M1/M2/M3/M4) using the MLX framework. Features:
- **Fast inference**: Leverages Apple Neural Engine
- **Prompt-based voice design**: Describe the voice you want, no reference audio needed
- **ASR support**: Speech-to-text included
- **Low memory**: 8-bit quantized, runs on 16GB Mac
- **Local only**: No cloud, no API keys, fully private

## When to Use

- Have an Apple Silicon Mac (M1/M2/M3/M4)
- Need high-quality TTS locally
- Want to design voices with text prompts (e.g., "a warm female voice, slightly soft")
- Need ASR (speech-to-text) capability
- Want fast inference with Apple Neural Engine

## When NOT to Use

- Non-Mac system (Intel Mac or Windows/Linux) → Use other TTS solutions
- Need voice cloning from reference audio → Use other tools
- Less than 16GB RAM → May work but slower

## Environment Setup

### One-Command Install

```bash
brew install ffmpeg uv && uv tool install --force "mlx-audio" --prerelease=allow
```

### Verify Installation

```bash
uv tool list | grep mlx
# Should show: mlx-audio v0.4.2
```

### Model Download

Models auto-download on first run (~2GB total) to `~/.cache/huggingface/hub/`:
- `mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-8bit`
- `mlx-community/Qwen3-ASR-0.6B-bf16`

**For China users (accelerated download):**

Option 1 - HuggingFace mirror:
```bash
export HF_ENDPOINT=https://hf-mirror.com
```

Option 2 - ModelScope (faster):
```bash
pip install modelscope

# Download TTS model
modelscope download \
  --model mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-8bit \
  --local_dir ~/.cache/huggingface/hub/Qwen3-TTS

# Download ASR model
modelscope download \
  --model mlx-community/Qwen3-ASR-0.6B-bf16 \
  --local_dir ~/.cache/huggingface/hub/Qwen3-ASR
```

## Usage

### Basic TTS

```bash
mlx_audio.tts.generate \
  --text "你好，这是本地 TTS 测试" \
  --output-path ./output.wav
```

### With Voice Design (Prompt-Based)

```bash
mlx_audio.tts.generate \
  --text "我是明日香" \
  --instruct "a confident teenage girl, flirtatious, seductive edge" \
  --output-path ./asuka.wav
```

### Voice Prompt Examples

| Style | Prompt |
|-------|--------|
| 自信少女 | `"a confident teenage girl, German-Japanese, EVA pilot"` |
| 温柔女声 | `"a warm, gentle female voice, slightly soft"` |
| 磁性男声 | `"a deep, masculine voice with authority"` |
| 儿童声音 | `"a cheerful little child, about 5 years old"` |
| 新闻播报 | `"a professional news anchor, clear and authoritative"` |
| 温柔妈妈 | `"a caring mother, warm and soothing"` |
| 神秘低语 | `"a mysterious whisper, soft and intimate, close to microphone"` |
| 激动演讲 | `"an energetic public speaker, passionate and enthusiastic"` |
| 悲伤叙述 | `"a melancholic storyteller, slow and reflective"` |

### Advanced Voice Design Tips

**Delivery Instructions** (Qwen3-TTS supports these):
- `"speak slowly and clearly"`
- `"whisper gently"`
- `"speak with excitement"`
- `"calm and soothing tone"`
- `"fast-paced, energetic delivery"`

**Combine multiple descriptors**:
```bash
--instruct "a warm female voice, slightly soft, speak slowly with gentle pauses"
```

### Long Text TTS (Auto-Chunking)

For texts longer than ~500 characters, use auto-chunking to avoid memory issues:

**Option 1: Manual script**
```bash
# Split text into sentences and generate separately
python3 << 'EOF'
import subprocess
import re

text = """Your long text here... Multiple sentences."""

# Split by sentence boundaries
sentences = re.split(r'(?<=[。！？.!?])\s+', text)
chunks = []
current_chunk = ""

for sent in sentences:
    if len(current_chunk) + len(sent) < 300:  # Max 300 chars per chunk
        current_chunk += sent
    else:
        if current_chunk:
            chunks.append(current_chunk)
        current_chunk = sent
if current_chunk:
    chunks.append(current_chunk)

# Generate each chunk
for i, chunk in enumerate(chunks):
    subprocess.run([
        "mlx_audio.tts.generate",
        "--text", chunk,
        "--instruct", "a warm, gentle female voice",
        "--output-path", f"./chunk_{i:03d}.wav"
    ])
print(f"Generated {len(chunks)} chunks. Use ffmpeg to concatenate.")
EOF
```

**Option 2: Concatenate with ffmpeg**
```bash
# After generating chunks, merge them
ffmpeg -i "concat:$(echo chunk_*.wav | tr ' ' '|')" -acodec copy final_output.wav

# Or with crossfade (smooth transition)
ffmpeg -f concat -safe 0 -i <(for f in chunk_*.wav; do echo "file '$PWD/$f'"; done) -c copy output.wav
```

### ASR (Speech to Text)

```bash
mlx_audio.stt.generate \
  --audio ./input.wav \
  --output-path ./transcript.txt \
  --language zh
```

Long audio (auto-chunking):
```bash
mlx_audio.stt.generate \
  --audio /path/to/long_audio.m4a \
  --output-path ./transcript.txt \
  --format txt \
  --language zh \
  --chunk-duration 30
```

### Batch Processing

**Batch TTS from file list:**
```bash
# Create text file with lines to synthesize
cat > texts.txt << 'EOF'
第一行要转换的文字
第二行要转换的文字
第三行要转换的文字
EOF

# Process each line
while IFS= read -r line; do
  safe_name=$(echo "$line" | tr -cd '[:alnum:]\n' | cut -c1-20)
  mlx_audio.tts.generate \
    --text "$line" \
    --instruct "a professional news anchor" \
    --output-path "./output/${safe_name}.wav"
done < texts.txt
```

**Batch ASR:**
```bash
# Batch convert all audio files in directory
for f in *.wav; do
  mlx_audio.stt.generate \
    --audio "$f" \
    --output-path "${f%.wav}.txt" \
    --language zh
done
```

### Audio Post-Processing (with ffmpeg)

While mlx-audio doesn't have built-in effects like Voicebox, you can use ffmpeg:

**Pitch Shift (音色调整):**
```bash
# Raise pitch by 2 semitones (更尖声)
ffmpeg -i input.wav -af "asetrate=48000*1.12,aresample=48000" output_high.wav

# Lower pitch by 2 semitones (更低沉)
ffmpeg -i input.wav -af "asetrate=48000*0.89,aresample=48000" output_low.wav
```

**Add Reverb (混响):**
```bash
ffmpeg -i input.wav -af "aecho=0.8:0.9:1000:0.3" output_reverb.wav
```

**Speed Control (语速):**
```bash
# Speed up 1.2x (更快)
ffmpeg -i input.wav -af "atempo=1.2" output_fast.wav

# Slow down 0.8x (更慢)
ffmpeg -i input.wav -af "atempo=0.8" output_slow.wav
```

**Volume Normalize (音量标准化):**
```bash
ffmpeg -i input.wav -af "loudnorm" output_normalized.wav
```

**Convert Format (格式转换):**
```bash
# WAV to MP3
ffmpeg -i input.wav -b:a 192k output.mp3

# WAV to AAC (for Apple devices)
ffmpeg -i input.wav -c:a aac -b:a 192k output.m4a

# WAV to FLAC (lossless compression)
ffmpeg -i input.wav output.flac
```

## Create Helper Script

Create `~/bin/tts.sh` for quick TTS:
```bash
#!/bin/bash
TEXT="${1:-"Hello, Human!"}"
INSTRUCT="${2:-"a confident teenage girl with a flirtatious, seductive edge"}"
OUTPUT_DIR=./voice_output

mkdir -p "$OUTPUT_DIR"

mlx_audio.tts.generate \
  --text "$TEXT" \
  --instruct "$INSTRUCT" \
  --output-path "$OUTPUT_DIR/output.wav" \
  --audio-format wav

echo "Generated: $OUTPUT_DIR/output.wav"
```

Make executable and use:
```bash
chmod +x ~/bin/tts.sh

# Usage
tts.sh "要转换的文字"
tts.sh "要转换的文字" "a warm, gentle female voice"
```

## Advanced Helper Script

Create `~/bin/tts-advanced.sh` with more features:
```bash
#!/bin/bash
# TTS with auto-chunking for long texts

TEXT="${1:-"Hello"}"
VOICE="${2:-"a warm, gentle female voice"}"
OUTPUT="${3:-"./output.wav"}"
MAX_CHARS=300

# Check if text needs chunking
if [ ${#TEXT} -le $MAX_CHARS ]; then
  # Short text - direct generation
  mlx_audio.tts.generate \
    --text "$TEXT" \
    --instruct "$VOICE" \
    --output-path "$OUTPUT"
  echo "Generated: $OUTPUT"
else
  # Long text - need chunking
  echo "Text too long (${#TEXT} chars), auto-chunking..."
  
  # Create temp directory
  TMPDIR=$(mktemp -d)
  
  # Split by sentences (simplified)
  echo "$TEXT" | fold -w $MAX_CHARS -s | split -l 1 - "$TMPDIR/chunk_"
  
  # Generate each chunk
  i=0
  for chunk in "$TMPDIR"/chunk_*; do
    CHUNK_TEXT=$(cat "$chunk")
    [ -z "$CHUNK_TEXT" ] && continue
    
    mlx_audio.tts.generate \
      --text "$CHUNK_TEXT" \
      --instruct "$VOICE" \
      --output-path "$TMPDIR/part_$(printf "%03d" $i).wav"
    
    i=$((i+1))
  done
  
  # Concatenate with ffmpeg
  ffmpeg -f concat -safe 0 -i \
    <(for f in "$TMPDIR"/part_*.wav; do echo "file '$f'"; done) \
    -c copy "$OUTPUT"
  
  # Cleanup
  rm -rf "$TMPDIR"
  echo "Generated: $OUTPUT"
fi
```

## Voicebox vs MLX-TTS Comparison

| Feature | Voicebox | MLX-TTS (Qwen3-TTS) |
|---------|----------|---------------------|
| **Platform** | macOS/Windows/Linux | Apple Silicon only |
| **GUI** | ✅ Desktop app | ❌ CLI only |
| **Multi-engine** | 5 engines (Qwen3, Lux, Chatterbox, TADA) | Qwen3-TTS only |
| **Voice cloning** | ✅ From reference audio | ❌ Prompt-based only |
| **Effects** | Built-in (reverb, pitch, delay) | ffmpeg post-processing |
| **Timeline editor** | ✅ Stories editor | ❌ |
| **Batch processing** | ✅ | Script-based |
| **API** | REST API | ❌ |
| **Setup** | Download DMG/MSI | One-command install |
| **Speed** | Fast | Fast (MLX optimized) |
| **Memory** | Configurable | ~8GB |
| **Privacy** | Local | Local |

**When to use Voicebox:**
- Need GUI and visual timeline
- Need voice cloning from audio
- Need built-in effects
- Multi-platform support

**When to use MLX-TTS:**
- Apple Silicon Mac only
- Prefer CLI and scripting
- Quick setup (`brew install`)
- Lightweight solution

## Quick Reference

| Task | Command |
|------|---------|
| Basic TTS | `mlx_audio.tts.generate --text "Hello" --output out.wav` |
| With voice design | Add `--instruct "voice description"` |
| ASR | `mlx_audio.stt.generate --audio in.wav --output out.txt` |
| Long audio ASR | Add `--chunk-duration 30` |
| Batch TTS | See "Batch Processing" section |
| Pitch shift | Use ffmpeg: `-af "asetrate=48000*1.12,aresample=48000"` |
| Change format | Use ffmpeg: `-i input.wav -b:a 192k output.mp3` |

## Output Formats

### TTS Output
- **Default**: WAV (48kHz, 16-bit)
- **Options**: `--audio-format wav|mp3|flac`

**Note**: mlx-audio outputs WAV by default. Convert to other formats with ffmpeg:
```bash
# High-quality MP3
ffmpeg -i input.wav -b:a 256k output.mp3

# AAC for Apple devices
ffmpeg -i input.wav -c:a aac -b:a 256k output.m4a

# FLAC for lossless
ffmpeg -i input.wav output.flac

# OGG Vorbis
ffmpeg -i input.wav -c:a libvorbis -q:a 6 output.ogg
```

### ASR Output Formats
- `--format txt`: Plain text (default)
- `--format json`: JSON with timestamps
- `--format srt`: Subtitle format

## Advanced Use Cases

### Podcast/Audio Book Production

```bash
# Create consistent narrator voice
VOICE="a warm, articulate narrator, clear and engaging"

# Generate chapters
for chapter in {1..10}; do
  mlx_audio.tts.generate \
    --text "Chapter $chapter" \
    --instruct "a professional announcer, clear and authoritative" \
    --output-path "./podcast/chapter_${chapter}_title.wav"
  
  mlx_audio.tts.generate \
    --text "$(cat chapter_${chapter}.txt)" \
    --instruct "$VOICE" \
    --output-path "./podcast/chapter_${chapter}_content.wav"
done

# Merge with ffmpeg
ffmpeg -f concat -safe 0 -i <(for f in ./podcast/*.wav; do echo "file '$PWD/$f'"; done) -c copy audiobook.wav
```

### Multi-Voice Dialogue

```bash
# Character A (confident young woman)
mlx_audio.tts.generate \
  --text "I'll take care of this." \
  --instruct "a confident teenage girl, slightly energetic" \
  --output-path ./voice_a.wav

# Character B (elderly wise man)
mlx_audio.tts.generate \
  --text "Be careful, my child." \
  --instruct "an elderly male voice, wise and gentle, slower pace" \
  --output-path ./voice_b.wav

# Character C (robot/AI)
mlx_audio.tts.generate \
  --text "Processing complete." \
  --instruct "a synthetic robotic voice, monotone, slightly metallic" \
  --output-path ./voice_c.wav

# Add robotic effect with ffmpeg
ffmpeg -i voice_c.wav -af "asetrate=48000*0.95,aresample=48000,aecho=0.6:0.4:300:0.5" voice_c_robot.wav
```

### Voice Templates Library

Create reusable voice templates:

```bash
# Save templates in a file
cat > ~/voice_templates.txt << 'EOF'
narration=a warm, articulate narrator, clear and engaging, moderate pace
news=a professional news anchor, clear and authoritative, precise diction
friendly=a friendly, approachable voice, warm and inviting
teacher=a patient educator, clear and encouraging, moderate pace
storyteller=a mysterious storyteller, dramatic and engaging
calm=a soothing, meditative voice, very slow and gentle
excited=a highly energetic voice, fast-paced and enthusiastic
dramatic=a theatrical voice, expressive and emotional
EOF

# Usage
VOICE=$(grep "^narration=" ~/voice_templates.txt | cut -d'=' -f2)
mlx_audio.tts.generate \
  --text "Your text here" \
  --instruct "$VOICE" \
  --output-path output.wav
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Model download fails/timeout | Use `HF_ENDPOINT=https://hf-mirror.com` or ModelScope |
| Memory不足 (OOM) | Model already 8-bit quantized; close other apps; use chunking for long text |
| Command not found | Restart terminal or run `uv tool update-shell` |
| Audio format not supported | Convert: `ffmpeg -i input.mp3 output.wav` |
| M1/M2 errors | Ensure macOS 14.0+; MLX requires Apple Silicon |
| Model path error | Use absolute path or `realpath` |
| Poor voice quality | Try different `--instruct` prompts; simpler is often better |
| Audio cuts off | Text too long; use auto-chunking for >500 chars |
| Pronunciation issues | Use phonetic spelling or hyphens: "AI" → "A I", "COVID" → "Co-vid" |

### Performance Tips

1. **First run is slow**: Model downloads ~2GB on first use
2. **Keep sentences together**: Don't split mid-sentence
3. **Simple prompts work better**: Avoid overly complex instructions
4. **Use --verbose**: See detailed output for debugging

### Debug Mode

```bash
# Verbose output
mlx_audio.tts.generate --verbose --text "Hello" --output test.wav

# Check model cache
ls -la ~/.cache/huggingface/hub/ | grep mlx

# Check disk space
df -h ~/.cache/huggingface/

# Test with minimal text
mlx_audio.tts.generate --text "Test" --output /tmp/test.wav
```

## References

- [MLX-Audio GitHub](https://github.com/Blaizzy/mlx-audio)
- [Qwen3-TTS Model](https://huggingface.co/mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-8bit)
- [Qwen3-ASR Model](https://huggingface.co/mlx-community/Qwen3-ASR-0.6B-bf16)
- [ModelScope](https://www.modelscope.cn/)
- [HuggingFace Mirror](https://hf-mirror.com/)
