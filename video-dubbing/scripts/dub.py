#!/usr/bin/env python3
"""
Video Dubbing Pipeline — end-to-end orchestrator.

Chains: extract audio → ASR(whisper) → translate prompt → TTS(dub_segments) → merge → burn subtitles

Usage:
  # Full pipeline: extract ASR from English video, dub to Chinese
  python3 scripts/dub.py input.mp4 --source-lang en --target-lang zh

  # Skip ASR if SRT already exists
  python3 scripts/dub.py input.mp4 --source-lang en --target-lang zh --srt existing.srt

  # Use Qwen3-ASR for better Chinese recognition
  python3 scripts/dub.py input.mp4 --source-lang zh --target-lang en --asr qwen3

  # Skip subtitle burning
  python3 scripts/dub.py input.mp4 --source-lang en --target-lang zh --no-burn
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path


def run(cmd, desc=None, check=True, capture_output=False):
    if desc:
        print(f"\n{'='*60}")
        print(f"  {desc}")
        print('='*60)
    print(f"  $ {' '.join(cmd[:6])}{' ...' if len(cmd) > 6 else ''}")
    kwargs = dict(check=check)
    if capture_output:
        kwargs["capture_output"] = capture_output
    result = subprocess.run(cmd, **kwargs)
    if capture_output:
        return result.stdout.decode() if isinstance(result.stdout, bytes) else result.stdout
    return result


def check_deps():
    missing = []
    for cmd in ["ffmpeg", "ffprobe"]:
        if not subprocess.run(["which", cmd], capture_output=True).returncode == 0:
            missing.append(cmd)
    if missing:
        print(f"Missing: {', '.join(missing)}. Install with: brew install ffmpeg")
        sys.exit(1)

    try:
        import whisper
    except ImportError:
        print("Installing openai-whisper...")
        subprocess.run([sys.executable, "-m", "pip", "install", "openai-whisper"], check=True)

    # verify mlx_audio
    if subprocess.run(["which", "mlx_audio.tts.generate"], capture_output=True).returncode != 0:
        print("Installing mlx-audio...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "mlx-audio"],
            check=True, capture_output=True,
        )

    # verify moviepy
    try:
        import moviepy
    except ImportError:
        print("Installing moviepy...")
        subprocess.run([sys.executable, "-m", "pip", "install", "moviepy"], check=True)


def step_extract(input_video, output_dir):
    audio_path = output_dir / "audio16k.wav"
    run([
        "ffmpeg", "-y",
        "-i", str(input_video),
        "-ar", "16000", "-ac", "1",
        "-c:a", "pcm_s16le",
        str(audio_path),
    ], desc="Step 1/5: Extract 16kHz mono audio")
    return audio_path


def step_asr(audio_path, output_dir, source_lang, asr_engine):
    srt_path = output_dir / "audio16k.srt"

    if asr_engine == "qwen3":
        qwen_script = Path(__file__).parent / "qwen3_asr.py"
        if not qwen_script.exists():
            print("qwen3_asr.py not found. Falling back to whisper.")
            asr_engine = "whisper"

    if asr_engine == "qwen3":
        run([
            sys.executable, str(Path(__file__).parent / "qwen3_asr.py"),
            str(audio_path),
            "--model", "0.6B",
            "--language", source_lang,
            "--output_format", "srt",
            "--output_dir", str(output_dir),
        ], desc=f"Step 2/5: ASR via Qwen3-ASR ({source_lang})")
    else:
        run([
            sys.executable, "-m", "whisper",
            str(audio_path),
            "--model", "large-v3-turbo",
            "--language", source_lang,
            "--output_format", "srt",
            "--output_dir", str(output_dir),
        ], desc=f"Step 2/5: ASR via Whisper (large-v3-turbo, {source_lang})")

        srt_path = output_dir / f"{audio_path.stem}.srt"
        if not srt_path.exists():
            srt_path = output_dir / "audio16k.srt"

    if not srt_path.exists():
        print(f"ASR failed: no SRT generated at {srt_path}", file=sys.stderr)
        sys.exit(1)

    # Count segments for the AI translation step
    with open(srt_path) as f:
        content = f.read()
    seg_count = content.count("\n\n") + 1
    print(f"\n  → {seg_count} segments detected in SRT")
    return srt_path


def step_translate(srt_path, output_dir, target_lang):
    """Output the translation prompt for the AI. In SKILL.md workflow, the AI
    (Claude) reads this, translates, and writes translated.txt."""
    print(f"\n{'='*60}")
    print(f"  Step 3/5: Translate Subtitles")
    print(f"{'='*60}")

    with open(srt_path) as f:
        content = f.read()

    # Extract text lines (skip index and timestamp lines)
    blocks = content.strip().split("\n\n")
    lines = []
    for block in blocks:
        parts = block.strip().split("\n")
        if len(parts) >= 3:
            text = "\n".join(parts[2:]).strip()
            lines.append(text)

    out_path = output_dir / "to_translate.txt"
    with open(out_path, "w") as f:
        for line in lines:
            f.write(line + "\n")

    print(f"\n  Source SRT: {srt_path.name} ({len(lines)} segments)")
    print(f"  Text saved to: {out_path.name}")
    print(f"\n  → Translate the text above, write one line per segment to:")
    print(f"    {output_dir / 'translated.txt'}")
    print(f"\n  Expected lines: {len(lines)}")

    return out_path


def step_dub(srt_path, translated_path, output_dir, target_lang):
    dub_script = Path(__file__).parent / "dub_segments.py"
    dubbing_wav = output_dir / "dubbing.wav"
    synced_srt = output_dir / "subtitle_synced.srt"

    run([
        sys.executable, str(dub_script),
        str(srt_path),
        str(translated_path),
        str(dubbing_wav),
        str(synced_srt),
        "--lang", target_lang,
    ], desc="Step 4/5: Generate Dubbed Audio (per-segment)")
    return dubbing_wav, synced_srt


def step_merge(input_video, dubbing_wav, output_dir):
    temp_video = output_dir / "output_temp.mp4"
    run([
        "ffmpeg", "-y",
        "-i", str(input_video),
        "-i", str(dubbing_wav),
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(temp_video),
    ], desc="Step 5/5: Merge Dubbed Audio into Video")

    # Verify both streams
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type",
         "-of", "csv=p=0", str(temp_video)],
        capture_output=True, text=True,
    )
    streams = [s.strip() for s in result.stdout.strip().split("\n") if s.strip()]
    print(f"  Streams in output: {streams}")
    if "video" not in streams:
        print("  WARNING: Video stream missing!", file=sys.stderr)
    if "audio" not in streams:
        print("  WARNING: Audio stream missing!", file=sys.stderr)

    return temp_video


def step_burn(temp_video, synced_srt, output_dir, output_name, font_size):
    burn_script = Path(__file__).parent / "burn_subtitles.py"
    final_video = output_dir / output_name

    run([
        sys.executable, str(burn_script),
        str(temp_video),
        str(synced_srt),
        str(final_video),
        "--font-size", str(font_size),
    ], desc="Final: Burn Hard Subtitles into Video")
    return final_video


def main():
    parser = argparse.ArgumentParser(
        description="Video Dubbing Pipeline — end-to-end",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              # English video → Chinese dubbing
              dub.py intro_video.mp4 --source-lang en --target-lang zh

              # Chinese video → English, using Qwen3-ASR
              dub.py lecture.mp4 --source-lang zh --target-lang en --asr qwen3

              # Skip ASR (using existing SRT)
              dub.py lecture.mp4 --source-lang zh --target-lang en --srt existing.srt
        """),
    )
    parser.add_argument("input", help="Input video file")
    parser.add_argument("--source-lang", default="en", help="Source language code (default: en)")
    parser.add_argument("--target-lang", default="zh", help="Target language code (default: zh)")
    parser.add_argument("--asr", choices=["whisper", "qwen3"], default="whisper",
                        help="ASR engine (default: whisper)")
    parser.add_argument("--srt", help="Existing SRT to skip ASR step")
    parser.add_argument("--output", "-o", help="Output filename (default: input_dubbed.mp4)")
    parser.add_argument("--font-size", type=int, default=28, help="Subtitle font size")
    parser.add_argument("--no-burn", action="store_true",
                        help="Skip subtitle burning (stop after audio merge)")
    parser.add_argument("--keep-temp", action="store_true", help="Keep intermediate files")
    args = parser.parse_args()

    check_deps()
    input_video = Path(args.input).resolve()
    if not input_video.exists():
        print(f"Input not found: {input_video}")
        sys.exit(1)

    output_dir = input_video.parent / f"{input_video.stem}_dubbed"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_name = args.output or f"{input_video.stem}_{args.target_lang}.mp4"

    # Step 1: Extract audio
    audio_path = step_extract(input_video, output_dir)

    # Step 2: ASR (or use existing SRT)
    if args.srt:
        srt_path = Path(args.srt).resolve()
        if not srt_path.exists():
            print(f"SRT not found: {srt_path}")
            sys.exit(1)
        print(f"\nUsing existing SRT: {srt_path}")
    else:
        srt_path = step_asr(audio_path, output_dir, args.source_lang, args.asr)

    # Step 3: Translation — in SKILL.md workflow, the AI does this.
    # Here we output the to_translate.txt and prompt the AI.
    translated_path = output_dir / "translated.txt"
    if not translated_path.exists():
        step_translate(srt_path, output_dir, args.target_lang)
        print(f"\n{'!'*60}")
        print(f"  TRANSLATION REQUIRED")
        print(f"{'!'*60}")
        print(f"  Please translate the text in {output_dir / 'to_translate.txt'}")
        print(f"  Save translations to: {translated_path}")
        print(f"  (one translated line per segment)")
        print(f"\n  Then re-run the same command to continue from here.")
        sys.exit(0)

    # Verify translation count matches SRT
    with open(srt_path) as f:
        srt_segs = f.read().count("\n\n") + 1
    with open(translated_path) as f:
        trans_lines = len([l for l in f if l.strip()])
    if srt_segs != trans_lines:
        print(f"Error: SRT has {srt_segs} segments but translated.txt has {trans_lines} lines",
              file=sys.stderr)
        print(f"Please fix translated.txt to have exactly {srt_segs} lines.", file=sys.stderr)
        sys.exit(1)

    # Step 4: Generate dubbed audio
    dubbing_wav, synced_srt = step_dub(srt_path, translated_path, output_dir, args.target_lang)

    # Step 5: Merge audio
    temp_video = step_merge(input_video, dubbing_wav, output_dir)

    # Final: Burn subtitles
    if args.no_burn:
        final_path = output_dir / output_name
        os.rename(temp_video, final_path)
        print(f"\n{'='*60}")
        print(f"  Done (no subtitles): {final_path}")
    else:
        final_path = step_burn(temp_video, synced_srt, output_dir, output_name, args.font_size)

    print(f"\n{'='*60}")
    print(f"  ✅ Complete!")
    print(f"  Final video: {final_path}")
    print(f"  Subtitles:   {synced_srt}")
    print(f"{'='*60}")

    if not args.keep_temp:
        for f in [audio_path]:
            if f.exists():
                f.unlink()
        for f in [temp_video]:
            if f.exists() and f != final_path:
                f.unlink()


if __name__ == "__main__":
    main()
