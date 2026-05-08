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
    print("Done: output_final.mp4")
