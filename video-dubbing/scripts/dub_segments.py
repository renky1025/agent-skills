#!/usr/bin/env python3
"""
Per-segment TTS dubbing with original-timestamp alignment.

Strategy:
  1. Generate TTS for segment 0 → use as voice reference for segments 1..N
  2. For each segment: compare TTS duration to original time slot
     - Too long (> slot): gentle speed up (atempo ≤ 1.20)
     - Too short (< slot): mild stretch (atempo ≥ 0.88)
  3. Bridge adjacent gaps < threshold: next segment starts right after previous
  4. Concatenate at aligned start times via ffmpeg adelay+amix
  5. Output synced SRT = original timestamps + translated text

Usage:
  python3 dub_segments.py original.srt translated.txt out_dub.wav out_synced.srt [--lang zh] [--keep-temp]
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path


TTS_MODEL = "mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-8bit"
TTS_INSTRUCT = "a professional male narrator, clear and natural, conversational pace"
MAX_ATEMPO = 1.20
MIN_ATEMPO = 0.88
GAP_BRIDGE_S = 1.0
TTS_TIMEOUT = 120  # seconds per segment


def parse_srt(filepath: str) -> list[dict]:
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    blocks = re.split(r"\n\s*\n", content.strip())
    segments = []
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        idx = int(lines[0])
        m = re.match(
            r"(\d+):(\d+):(\d+)[.,](\d+)\s*-->\s*(\d+):(\d+):(\d+)[.,](\d+)",
            lines[1],
        )
        if not m:
            continue
        h1, m1, s1, ms1, h2, m2, s2, ms2 = map(int, m.groups())
        start = h1 * 3600 + m1 * 60 + s1 + ms1 / 1000.0
        end = h2 * 3600 + m2 * 60 + s2 + ms2 / 1000.0
        text = "\n".join(lines[2:]).strip()
        segments.append({"index": idx, "start": start, "end": end, "text": text})
    return segments


def read_translations(filepath: str) -> list[str]:
    with open(filepath, encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip()]


def _run_tts(text: str, *, ref_audio: str | None = None, ref_text: str | None = None,
             lang: str = "zh") -> str | None:
    tmpdir = tempfile.mkdtemp()
    try:
        cmd = [
            "mlx_audio.tts.generate",
            "--model", TTS_MODEL,
            "--text", text,
            "--instruct", TTS_INSTRUCT,
            "--speed", "1.0",
            "--lang_code", lang,
            "--file_prefix", "tts",
        ]
        if ref_audio and os.path.exists(ref_audio):
            cmd.extend(["--ref_audio", ref_audio])
            if ref_text:
                cmd.extend(["--ref_text", ref_text[:100]])
        subprocess.run(cmd, check=True, capture_output=True, cwd=tmpdir, timeout=TTS_TIMEOUT)
        generated = list(Path(tmpdir).rglob("*.wav"))
        if generated:
            out = os.path.join(tempfile.mkdtemp(), "tts_out.wav")
            shutil.move(str(generated[0]), out)
            return out
        return None
    except subprocess.TimeoutExpired:
        print(f"  TTS timed out after {TTS_TIMEOUT}s", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  TTS failed: {e}", file=sys.stderr)
        return None
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def get_duration(filepath: str) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", filepath],
        capture_output=True, text=True,
    )
    return float(result.stdout.strip())


def adjust_speed(input_wav: str, output_wav: str, ratio: float) -> None:
    if 0.99 <= ratio <= 1.01:
        shutil.copy(input_wav, output_wav)
        return
    filters = []
    r = ratio
    while r < 0.5:
        filters.append("atempo=0.5")
        r /= 0.5
    while r > 2.0:
        filters.append("atempo=2.0")
        r /= 2.0
    filters.append(f"atempo={r:.4f}")
    subprocess.run(
        ["ffmpeg", "-y", "-i", input_wav, "-af", ",".join(filters),
         "-ar", "24000", output_wav],
        capture_output=True, check=True,
    )


def create_silence(duration_s: float, output_wav: str) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=24000:cl=mono",
         "-t", str(duration_s), "-acodec", "pcm_s16le", output_wav],
        capture_output=True, check=True,
    )


def _fmt_srt(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_synced_srt(segments: list[dict], translations: list[str],
                     output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        for i, (seg, trans) in enumerate(zip(segments, translations), 1):
            f.write(f"{i}\n")
            f.write(f"{_fmt_srt(seg['start'])} --> {_fmt_srt(seg['end'])}\n")
            f.write(f"{trans}\n\n")


def concat_segments(audio_files: list[str], start_times: list[float],
                    output_wav: str, total_duration: float) -> None:
    inputs = []
    filter_parts = []
    for i, (af, st) in enumerate(zip(audio_files, start_times)):
        inputs.extend(["-i", af])
        delay_ms = int(st * 1000)
        filter_parts.append(f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}]")
    mix_label = "".join(f"[a{i}]" for i in range(len(audio_files)))
    filter_parts.append(f"{mix_label}amix=inputs={len(audio_files)}:duration=longest[aout]")
    cmd = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", ";".join(filter_parts),
        "-map", "[aout]", "-t", str(total_duration),
        "-ar", "24000", "-ac", "1", output_wav,
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def main():
    parser = argparse.ArgumentParser(
        description="Per-segment TTS dubbing with original-timestamp alignment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              dub_segments.py audio.srt translated.txt dubbing.wav synced.srt
              dub_segments.py audio.srt translated.txt dubbing.wav synced.srt --lang zh --keep-temp
        """),
    )
    parser.add_argument("original_srt", help="Original SRT with timestamps (from ASR)")
    parser.add_argument("translated_txt", help="Translated text, one line per segment")
    parser.add_argument("out_dubbing", help="Output dubbing WAV")
    parser.add_argument("out_srt", help="Output synced SRT (original timestamps + translated text)")
    parser.add_argument("--lang", default="zh", help="TTS language code (default: zh)")
    parser.add_argument("--keep-temp", action="store_true", help="Keep temp segment files")
    parser.add_argument("--max-atempo", type=float, default=MAX_ATEMPO)
    parser.add_argument("--min-atempo", type=float, default=MIN_ATEMPO)
    parser.add_argument("--gap-bridge", type=float, default=GAP_BRIDGE_S)
    args = parser.parse_args()

    segments = parse_srt(args.original_srt)
    translations = read_translations(args.translated_txt)

    if len(translations) != len(segments):
        print(f"Error: {len(segments)} SRT segments but {len(translations)} "
              f"translation lines. Must match 1:1.", file=sys.stderr)
        sys.exit(1)

    workdir = tempfile.mkdtemp(prefix="dub_segments_")
    print(f"Segments: {len(segments)}  |  atempo: [{args.min_atempo}, {args.max_atempo}]  "
          f"gap-bridge: {args.gap_bridge}s", file=sys.stderr)

    # ── Phase 1: generate TTS with voice consistency ──
    ref_audio_path = None
    ref_text = None
    raw_files: list[str | None] = [None] * len(segments)
    tts_ok = 0

    for i, (seg, trans) in enumerate(zip(segments, translations)):
        slot_dur = seg["end"] - seg["start"]
        if slot_dur <= 0 or not trans.strip():
            continue
        print(f"  [{i+1}/{len(segments)}] TTS ({slot_dur:.1f}s slot): {trans[:40]}...",
              file=sys.stderr)

        # Retry TTS once on failure
        wav = None
        for attempt in range(2):
            wav = _run_tts(trans, ref_audio=ref_audio_path, ref_text=ref_text, lang=args.lang)
            if wav is not None:
                break
            if attempt == 0:
                print(f"    retrying...", file=sys.stderr)

        if wav is None:
            print(f"    TTS failed after retry, using silence ({slot_dur:.1f}s)", file=sys.stderr)
            wav = os.path.join(workdir, f"seg_{i:04d}_sil.wav")
            create_silence(slot_dur, wav)
        elif ref_audio_path is None:
            ref_audio_path = wav
            ref_text = trans[:100]
            print(f"    -> voice reference set", file=sys.stderr)
            tts_ok += 1
        else:
            tts_ok += 1

        raw_files[i] = wav

    print(f"TTS done: {tts_ok}/{len(segments)} segments OK", file=sys.stderr)

    # ── Phase 2: adjust speed + smart gap bridging ──
    audio_files = []
    start_times = []
    prev_end_time = 0.0
    stats = {"natural": 0, "sped_up": 0, "slowed": 0, "bridged": 0}

    for i, (seg, trans) in enumerate(zip(segments, translations)):
        slot_dur = seg["end"] - seg["start"]
        if slot_dur <= 0 or not trans.strip() or raw_files[i] is None:
            continue

        adj_wav = os.path.join(workdir, f"seg_{i:04d}_adj.wav")
        orig_start = seg["start"]
        gap_to_prev = orig_start - prev_end_time

        if i > 0 and 0 < gap_to_prev < args.gap_bridge:
            use_start = prev_end_time
            stats["bridged"] += 1
        else:
            use_start = orig_start

        raw_dur = get_duration(raw_files[i])
        atempo = raw_dur / slot_dur
        atempo = max(args.min_atempo, min(args.max_atempo, atempo))

        if 0.99 <= atempo <= 1.01:
            shutil.copy(raw_files[i], adj_wav)
            adj_dur = raw_dur
            stats["natural"] += 1
            action = "natural"
        elif atempo > 1.01:
            adjust_speed(raw_files[i], adj_wav, atempo)
            adj_dur = get_duration(adj_wav)
            stats["sped_up"] += 1
            action = f"sped {atempo:.2f}x"
        else:
            adjust_speed(raw_files[i], adj_wav, atempo)
            adj_dur = get_duration(adj_wav)
            stats["slowed"] += 1
            action = f"slowed {atempo:.2f}x"

        audio_files.append(adj_wav)
        start_times.append(use_start)
        prev_end_time = use_start + adj_dur

    # ── Phase 3: concatenate ──
    max_end = max((seg["end"] for seg in segments), default=0)
    total_dur = max_end + 2.0

    print(f"\nMerging {len(audio_files)} segments → {args.out_dubbing} "
          f"(total: {total_dur:.1f}s)", file=sys.stderr)
    print(f"Stats: {stats['natural']} natural, {stats['sped_up']} sped up, "
          f"{stats['slowed']} slowed, {stats['bridged']} bridged", file=sys.stderr)

    if audio_files:
        concat_segments(audio_files, start_times, args.out_dubbing, total_dur)
    else:
        print("No audio segments generated, creating silence", file=sys.stderr)
        create_silence(total_dur, args.out_dubbing)

    write_synced_srt(segments, translations, args.out_srt)

    if not args.keep_temp:
        shutil.rmtree(workdir, ignore_errors=True)
        for w in raw_files:
            if w and os.path.exists(w):
                parent = os.path.dirname(w)
                if os.path.exists(parent):
                    shutil.rmtree(parent, ignore_errors=True)

    print(f"Done → {args.out_dubbing} + {args.out_srt}", file=sys.stderr)


if __name__ == "__main__":
    main()
