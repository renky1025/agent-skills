#!/usr/bin/env python3
"""
Burn hardcoded subtitles into video using moviepy.

Usage:
  python3 burn_subtitles.py input.mp4 subtitles.srt output.mp4
  python3 burn_subtitles.py input.mp4 subtitles.srt output.mp4 --font-size 32
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def check_moviepy():
    try:
        import moviepy
        return True
    except ImportError:
        print("moviepy not installed. Installing...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "moviepy"],
            check=True, capture_output=True,
        )
        return True


def parse_srt(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    blocks = re.split(r"\n\s*\n", content.strip())
    subtitles = []
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) >= 3:
            time_line = lines[1]
            text = "\n".join(lines[2:])
            match = re.match(
                r"(\d+):(\d+):(\d+)[.,](\d+) --> (\d+):(\d+):(\d+)[.,](\d+)", time_line
            )
            if match:
                h1, m1, s1, ms1, h2, m2, s2, ms2 = map(int, match.groups())
                start = h1 * 3600 + m1 * 60 + s1 + ms1 / 1000.0
                end = h2 * 3600 + m2 * 60 + s2 + ms2 / 1000.0
                subtitles.append((start, end, text.strip()))
    return subtitles


def find_chinese_font():
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    for path in candidates:
        if Path(path).exists():
            return path

    # Try fc-list as fallback
    try:
        result = subprocess.run(
            ["fc-list", ":lang=zh", "-f", "%{file}\n"],
            capture_output=True, text=True, timeout=5,
        )
        fonts = [f.strip() for f in result.stdout.split("\n") if f.strip()]
        if fonts:
            return fonts[0]
    except Exception:
        pass

    return None


def burn(input_video, srt_path, output_video, font_path=None, font_size=28):
    from moviepy import VideoFileClip, TextClip, CompositeVideoClip

    video = VideoFileClip(str(input_video))
    subs = parse_srt(str(srt_path))

    if not subs:
        print(f"Error: No valid subtitles found in {srt_path}", file=sys.stderr)
        sys.exit(1)

    font = font_path or find_chinese_font()
    print(f"Font: {font}")
    print(f"Video: {video.size[0]}x{video.size[1]}, {video.duration:.1f}s")
    print(f"Subtitles: {len(subs)} segments")

    clips = [video]
    W, H = video.size
    duration = video.duration
    burned = 0

    for start, end, text in subs:
        if start >= duration:
            break
        end = min(end, duration)
        if end - start < 0.3:
            continue

        txt_clip = TextClip(
            text=text,
            font=font,
            font_size=font_size,
            color="white",
            stroke_color="black",
            stroke_width=2,
            method="caption",
            size=(W - 80, None),
            text_align="center",
        )
        txt_clip = txt_clip.with_position(("center", H - txt_clip.h - 40))
        txt_clip = txt_clip.with_start(start).with_end(end)
        clips.append(txt_clip)
        burned += 1

    print(f"Burning {burned} subtitle segments...")
    final = CompositeVideoClip(clips, size=video.size)
    final = final.with_audio(video.audio)
    final.write_videofile(
        str(output_video),
        codec="libx264",
        audio_codec="aac",
        fps=video.fps,
        preset="fast",
        logger=None,
    )
    print(f"Done: {output_video}")


def main():
    parser = argparse.ArgumentParser(description="Burn subtitles into video")
    parser.add_argument("video", help="Input video file")
    parser.add_argument("srt", help="SRT subtitle file")
    parser.add_argument("output", nargs="?", default="output_final.mp4",
                        help="Output video file (default: output_final.mp4)")
    parser.add_argument("--font", help="Font path override")
    parser.add_argument("--font-size", type=int, default=28, help="Font size (default: 28)")
    args = parser.parse_args()

    check_moviepy()
    burn(args.video, args.srt, args.output, args.font, args.font_size)


if __name__ == "__main__":
    main()
