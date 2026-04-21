"""
FFmpeg 视频合成模块
"""

import os
import subprocess
import tempfile
import random
from typing import List, Optional
from ..models import Slide
from ..utils.file import find_music


def get_random_transition(duration: float, is_first: bool = False) -> str:
    """获取随机过渡效果"""
    if is_first:
        return f"fade=t=out:st={duration-0.5}:d=0.5"

    transitions = [
        f"fade=t=in:st=0:d=0.4,fade=t=out:st={duration-0.5}:d=0.5",
        f"fade=t=in:st=0:d=0.3,fade=t=out:st={duration-0.4}:d=0.4",
    ]

    return random.choice(transitions)


def create_video(image_paths: List[str], slides: List[Slide],
                 output_path: str, music_dir: Optional[str] = None) -> bool:
    """
    创建视频，支持背景音乐
    """
    if not image_paths:
        print("❌ No images")
        return False

    temp_dir = tempfile.mkdtemp()

    try:
        print("🎬 Creating video...")

        # 计算总时长
        total_duration = sum(s.duration for s in slides)

        # 创建视频片段
        segment_files = []
        for i, (img_path, slide) in enumerate(zip(image_paths, slides)):
            segment_path = os.path.join(temp_dir, f"seg_{i:04d}.mp4")
            duration = slide.duration

            base_vf = (f"fps=30,scale=1920:1080:force_original_aspect_ratio=decrease,"
                       f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,format=yuv420p")

            transition = get_random_transition(duration, is_first=(i == 0))
            vf = f"{base_vf},{transition}"

            cmd = [
                'ffmpeg', '-y', '-loop', '1', '-i', img_path,
                '-vf', vf,
                '-c:v', 'libx264', '-preset', 'fast',
                '-t', str(duration),
                '-pix_fmt', 'yuv420p',
                segment_path
            ]

            subprocess.run(cmd, capture_output=True)
            if os.path.exists(segment_path):
                segment_files.append(segment_path)

        if not segment_files:
            print("❌ Failed to create segments")
            return False

        # 合并片段
        concat_list = os.path.join(temp_dir, "concat.txt")
        with open(concat_list, 'w') as f:
            for seg in segment_files:
                f.write(f"file '{seg}'\n")

        temp_video = os.path.join(temp_dir, "temp.mp4")
        cmd = [
            'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
            '-i', concat_list,
            '-c:v', 'libx264', '-preset', 'medium',
            '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart',
            temp_video
        ]
        subprocess.run(cmd, capture_output=True)

        # 添加背景音乐
        final_video = _add_background_music(
            temp_video, output_path, music_dir, total_duration
        )

        print(f"✅ Video: {output_path}")
        print(f"📊 Duration: {total_duration:.1f}s | Slides: {len(slides)}")

        return final_video

    finally:
        import shutil
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def _add_background_music(video_path: str, output_path: str,
                          music_dir: Optional[str], video_duration: float) -> bool:
    """添加背景音乐（支持循环/截断）"""

    # 如果没有指定音乐目录，尝试使用默认路径
    default_music = "/Users/kyren/Downloads/【08】剪辑配乐精选—节奏类180首"
    if not music_dir or not os.path.exists(music_dir):
        if os.path.exists(default_music):
            music_dir = default_music
        else:
            # 无音乐，直接复制
            import shutil
            shutil.copy(video_path, output_path)
            return True

    music_files = find_music(music_dir)

    if not music_files:
        import shutil
        shutil.copy(video_path, output_path)
        return True

    # 随机选择音乐
    music_file = random.choice(music_files)
    print(f"🎵 {os.path.basename(music_file)}")

    # 获取音频时长
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', music_file],
            capture_output=True, text=True
        )
        audio_duration = float(result.stdout.strip())
    except:
        audio_duration = 0

    print(f"   Video: {video_duration:.1f}s | Audio: {audio_duration:.1f}s")

    # 构建音频滤镜
    if audio_duration < video_duration:
        loop_count = int(video_duration / audio_duration) + 2
        audio_filter = f"[1:a]volume=0.3,aloop=loop={loop_count}:size={int(audio_duration*48000)}[a]"
        print(f"   Audio will loop ({loop_count}x)")
    else:
        audio_filter = f"[1:a]volume=0.3,atrim=duration={video_duration}[a]"
        print(f"   Audio will be trimmed")

    cmd = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-i', music_file,
        '-filter_complex', audio_filter,
        '-map', '0:v', '-map', '[a]',
        '-c:v', 'copy', '-c:a', 'aac',
        '-shortest', output_path
    ]

    subprocess.run(cmd, capture_output=True)
    return os.path.exists(output_path)
