#!/usr/bin/env python3
"""
Qwen3-ASR CLI — whisper-compatible drop-in for the video-dubbing skill.

Replaces both whisper invocations from SKILL.md:

  # Step 1 (original subtitles)
  whisper original_audio.m4a --model turbo --language en --output_format all --output_dir .
  # becomes:
  qwen3_asr original_audio.m4a --model 0.6B --language en --output_format all --output_dir .

  # Step 5 (dubbing timestamps)
  whisper dubbing_adjusted.wav --model turbo --language zh --output_format srt --output_dir .
  # becomes:
  qwen3_asr dubbing_adjusted.wav --model 0.6B --language zh --output_format srt --output_dir .

Prerequisites:
  pip install qwen-asr

Works on CUDA, MPS (Apple Silicon), and CPU.
"""

import argparse
import json
import os
import sys
from pathlib import Path

# ── language code → Qwen3 language name ──────────────────────────────
LANG_MAP: dict[str, str] = {
    "zh": "Chinese",      "en": "English",       "ja": "Japanese",
    "ko": "Korean",       "fr": "French",        "de": "German",
    "es": "Spanish",      "pt": "Portuguese",    "it": "Italian",
    "ru": "Russian",      "ar": "Arabic",        "th": "Thai",
    "vi": "Vietnamese",   "tr": "Turkish",       "hi": "Hindi",
    "ms": "Malay",        "nl": "Dutch",         "sv": "Swedish",
    "da": "Danish",       "fi": "Finnish",       "pl": "Polish",
    "cs": "Czech",        "fil": "Filipino",     "fa": "Persian",
    "el": "Greek",        "hu": "Hungarian",     "mk": "Macedonian",
    "ro": "Romanian",     "yue": "Cantonese",
}

# ── model name aliases ───────────────────────────────────────────────
# Key: CLI argument.  Value: (label, HuggingFace id)
MODEL_MAP: dict[str, tuple[str, str]] = {
    "0.6B":  ("0.6B",  "Qwen/Qwen3-ASR-0.6B"),
    "1.7B":  ("1.7B",  "Qwen/Qwen3-ASR-1.7B"),
    # whisper-compatible aliases → smallest/fastest Qwen3
    "turbo":  ("0.6B",  "Qwen/Qwen3-ASR-0.6B"),
    "tiny":   ("0.6B",  "Qwen/Qwen3-ASR-0.6B"),
    "base":   ("0.6B",  "Qwen/Qwen3-ASR-0.6B"),
    "small":  ("0.6B",  "Qwen/Qwen3-ASR-0.6B"),
    "medium": ("1.7B",  "Qwen/Qwen3-ASR-1.7B"),
    "large":  ("1.7B",  "Qwen/Qwen3-ASR-1.7B"),
}

FORCED_ALIGNER_ID = "Qwen/Qwen3-ForcedAligner-0.6B"


# ── helpers ──────────────────────────────────────────────────────────

def _get_device() -> tuple[str, "torch.dtype"]:  # noqa: F821
    import torch
    if torch.cuda.is_available():
        return "cuda:0", torch.bfloat16
    if torch.backends.mps.is_available():
        return "mps", torch.float32
    return "cpu", torch.float32


def _parse_dtype(raw: str | None) -> "torch.dtype | None":  # noqa: F821
    if raw is None:
        return None
    import torch
    mapping = {
        "float16": torch.float16,
        "bfloat16": torch.bfloat16,
        "float32": torch.float32,
    }
    if raw not in mapping:
        print(f"Unknown dtype '{raw}', using auto-detect", file=sys.stderr)
        return None
    return mapping[raw]


def _fmt_srt(s: float) -> str:
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = int(s % 60)
    ms = int((s % 1) * 1000)
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"


def _fmt_vtt(s: float) -> str:
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = int(s % 60)
    ms = int((s % 1) * 1000)
    return f"{h:02d}:{m:02d}:{sec:02d}.{ms:03d}"


# ── output writers ───────────────────────────────────────────────────

def _write_srt(segments: list[tuple[float, float, str]], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for i, (start, end, text) in enumerate(segments, 1):
            f.write(f"{i}\n{_fmt_srt(start)} --> {_fmt_srt(end)}\n{text}\n\n")


def _write_vtt(segments: list[tuple[float, float, str]], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for i, (start, end, text) in enumerate(segments, 1):
            f.write(f"{i}\n{_fmt_vtt(start)} --> {_fmt_vtt(end)}\n{text}\n\n")


def _write_txt(segments: list[tuple[float, float, str]], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for _, _, text in segments:
            f.write(text + "\n")


def _write_json(segments: list[tuple[float, float, str]], path: str) -> None:
    data = {
        "segments": [
            {"id": i, "start": s, "end": e, "text": t}
            for i, (s, e, t) in enumerate(segments, 1)
        ],
        "text": " ".join(t for _, _, t in segments),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _write_tsv(segments: list[tuple[float, float, str]], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("start\tend\ttext\n")
        for s, e, t in segments:
            f.write(f"{s:.3f}\t{e:.3f}\t{t}\n")


OUTPUT_FORMATS: dict[str, tuple[str, callable]] = {
    "srt":  ("srt",  _write_srt),
    "vtt":  ("vtt",  _write_vtt),
    "txt":  ("txt",  _write_txt),
    "json": ("json", _write_json),
    "tsv":  ("tsv",  _write_tsv),
}


# ── check / install ──────────────────────────────────────────────────

def _check_prerequisites() -> bool:
    try:
        import qwen_asr  # noqa: F401
        return True
    except ImportError:
        print("Error: 'qwen-asr' package is not installed.", file=sys.stderr)
        print(file=sys.stderr)
        print("Install with:", file=sys.stderr)
        print("  pip install qwen-asr", file=sys.stderr)
        print(file=sys.stderr)
        print("For faster vLLM backend (streaming, batch):", file=sys.stderr)
        print("  pip install 'qwen-asr[vllm]'", file=sys.stderr)
        print(file=sys.stderr)
        print("Requires Python ≥ 3.10.  Use a fresh environment:", file=sys.stderr)
        print("  conda create -n qwen3-asr python=3.12 -y", file=sys.stderr)
        print("  conda activate qwen3-asr", file=sys.stderr)
        print("  pip install qwen-asr", file=sys.stderr)
        return False


# ── core ─────────────────────────────────────────────────────────────

def run_asr(
    audio_path: str,
    model_name: str,
    language: str | None,
    output_dir: str,
    output_format: str,
    device: str | None,
    dtype_str: str | None,
) -> None:
    from qwen_asr import Qwen3ASRModel
    import torch

    # resolve model
    if model_name not in MODEL_MAP:
        print(
            f"Unknown model '{model_name}'.  "
            f"Available: {sorted(set(MODEL_MAP.keys()))}",
            file=sys.stderr,
        )
        sys.exit(1)
    label, hf_id = MODEL_MAP[model_name]

    # resolve language
    qwen_lang: str | None = None
    if language and language.lower() != "auto":
        qwen_lang = LANG_MAP.get(language.lower(), language)

    # resolve device / dtype
    _device = device or _get_device()[0]
    _dtype = _parse_dtype(dtype_str)
    if _dtype is None:
        _, _dtype = _get_device()

    # timestamped output needs the forced aligner
    needs_ts = output_format in ("srt", "vtt", "json", "all")
    aligner_id = FORCED_ALIGNER_ID if needs_ts else None
    aligner_kw = dict(dtype=_dtype, device_map=_device) if needs_ts else None

    print(f"Model : {hf_id}  ({label})", file=sys.stderr)
    print(f"Device: {_device}  dtype: {_dtype}", file=sys.stderr)
    print("Loading …", file=sys.stderr)

    model = Qwen3ASRModel.from_pretrained(
        hf_id,
        dtype=_dtype,
        device_map=_device,
        max_new_tokens=4096,
        forced_aligner=aligner_id,
        forced_aligner_kwargs=aligner_kw,
    )

    print(f"Transcribing: {audio_path}", file=sys.stderr)
    if qwen_lang:
        print(f"Language hint: {qwen_lang}", file=sys.stderr)

    results = model.transcribe(
        audio=audio_path,
        language=qwen_lang,
        return_time_stamps=needs_ts,
    )
    r = results[0]

    print(f"Detected language: {r.language}", file=sys.stderr)

    # build segment list
    segments: list[tuple[float, float, str]] = []

    if needs_ts and hasattr(r, "time_stamps") and r.time_stamps:
        for ts in r.time_stamps[0]:
            if hasattr(ts, "start_time"):
                segments.append((float(ts.start_time), float(ts.end_time), str(ts.text)))
            elif isinstance(ts, (tuple, list)) and len(ts) >= 3:
                segments.append((float(ts[0]), float(ts[1]), str(ts[2])))

    if not segments:
        segments = [(0.0, 0.0, r.text)]

    # write output
    os.makedirs(output_dir, exist_ok=True)
    stem = Path(audio_path).stem
    base = os.path.join(output_dir, stem)

    if output_format == "all":
        for _fmt, (ext, writer) in OUTPUT_FORMATS.items():
            writer(segments, f"{base}.{ext}")
            print(f"  → {base}.{ext}", file=sys.stderr)
    else:
        ext, writer = OUTPUT_FORMATS[output_format]
        writer(segments, f"{base}.{ext}")
        print(f"  → {base}.{ext}", file=sys.stderr)

    seg_count = len(segments)
    char_count = sum(len(t) for _, _, t in segments)
    print(f"Done — {seg_count} segments, {char_count} chars", file=sys.stderr)


# ── CLI ──────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Qwen3-ASR CLI — whisper-compatible speech recognition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  qwen3_asr audio.wav
  qwen3_asr audio.wav --model 1.7B --language zh
  qwen3_asr audio.m4a --model turbo --language en -f srt -o ./subs
  qwen3_asr dubbing.wav --model 0.6B --language zh -f all

Model aliases (whisper-compatible):
  turbo / tiny / base / small  →  Qwen3-ASR-0.6B  (fast, 0.6B params)
  medium / large              →  Qwen3-ASR-1.7B  (highest accuracy)

Supported language codes:  zh en ja ko fr de es pt it ru ar th vi tr hi
  ms nl sv da fi pl cs fil fa el hu mk ro yue  (or "auto")
""",
    )
    parser.add_argument("input", help="Audio file (wav, mp3, m4a, flac, …)")
    parser.add_argument(
        "--model", default="0.6B",
        help="Model (0.6B, 1.7B) or whisper alias (turbo, medium, large, …)",
    )
    parser.add_argument(
        "--language", default="auto",
        help="Language code or 'auto' for automatic detection",
    )
    parser.add_argument(
        "--output_format", "-f", default="srt",
        choices=["srt", "vtt", "txt", "json", "tsv", "all"],
        help="Output format (default: srt)",
    )
    parser.add_argument(
        "--output_dir", "-o", default=".",
        help="Output directory (default: .)",
    )
    parser.add_argument(
        "--device", default=None,
        help="Device override: cuda:0, mps, cpu",
    )
    parser.add_argument(
        "--dtype", default=None,
        help="dtype override: float16, bfloat16, float32",
    )

    args = parser.parse_args()

    if not _check_prerequisites():
        sys.exit(1)

    run_asr(
        audio_path=args.input,
        model_name=args.model,
        language=args.language,
        output_dir=args.output_dir,
        output_format=args.output_format,
        device=args.device,
        dtype_str=args.dtype,
    )


if __name__ == "__main__":
    main()
