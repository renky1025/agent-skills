#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频纪要生成工具
自动提取视频语音、转录、总结，生成结构化纪要文档
"""

import os
import sys
import json
import argparse
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime, timedelta


def check_ffmpeg():
    """检查 ffmpeg 是否已安装"""
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            check=True
        )
        version_line = result.stdout.split('\n')[0]
        print(f"[OK] FFmpeg installed: {version_line}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[ERROR] FFmpeg not installed")
        print("  请安装 FFmpeg: winget install Gyan.FFmpeg")
        return False


def check_whisper():
    """检查 whisper 是否已安装"""
    try:
        import whisper
        print("[OK] Whisper installed")
        return True
    except ImportError:
        print("[ERROR] Whisper not installed")
        print("  请安装: pip install openai-whisper")
        return False


def get_video_duration(video_path):
    """获取视频时长"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', str(video_path)],
            capture_output=True,
            text=True,
            check=True
        )
        duration = float(result.stdout.strip())
        return timedelta(seconds=int(duration))
    except:
        return None


def extract_audio(video_path, output_audio_path):
    """从视频中提取音频"""
    print(f"\n[STEP 1] Extracting audio...")
    print(f"   Video: {video_path}")
    
    try:
        subprocess.run([
            'ffmpeg', '-y', '-i', str(video_path),
            '-vn', '-acodec', 'pcm_s16le',
            '-ar', '16000', '-ac', '1',
            str(output_audio_path)
        ], check=True, capture_output=True)
        
        print(f"[OK] Audio extracted: {output_audio_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Audio extraction failed: {e}")
        return False


def transcribe_audio(audio_path, model_name='base', language=None):
    """使用 Whisper 转录音频"""
    print(f"\n[STEP 2] Transcribing audio...")
    print(f"   Model: {model_name}")
    if language:
        print(f"   Language: {language}")
    
    try:
        import whisper
        
        # 加载模型
        model = whisper.load_model(model_name)
        
        # 转录
        result = model.transcribe(
            str(audio_path),
            language=language,
            verbose=False
        )
        
        print(f"[OK] Transcription completed")
        print(f"   Segments: {len(result['segments'])}")
        
        return result
    except Exception as e:
        print(f"[ERROR] Transcription failed: {e}")
        return None


def format_timestamp(seconds):
    """格式化时间戳"""
    td = timedelta(seconds=int(seconds))
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def analyze_content(segments, full_text):
    """分析内容，提取关键信息"""
    print(f"\n[STEP 3] Analyzing content...")
    
    # 简单的关键词提取和分段
    # 在实际应用中，这里可以调用 LLM API 进行更智能的分析
    
    # 按句子分割
    sentences = []
    for seg in segments:
        text = seg['text'].strip()
        start = seg['start']
        if text:
            sentences.append({
                'text': text,
                'timestamp': start,
                'timestamp_str': format_timestamp(start)
            })
    
    # 提取关键句（基于简单启发式规则）
    key_points = []
    important_keywords = [
        '重要', '关键', '核心', '总结', '结论', '决定', '决议',
        '必须', '需要', '应该', '建议', '注意', '提醒',
        '首先', '其次', '最后', '第一', '第二', '第三',
        '总之', '综上所述', '因此', '所以', '结果',
        '问题', '挑战', '困难', '解决方案', '方法',
        '目标', '计划', '安排', '任务', '下一步'
    ]
    
    for sent in sentences:
        score = 0
        for keyword in important_keywords:
            if keyword in sent['text']:
                score += 1
        
        # 如果句子较长且包含关键词，认为是关键句
        if len(sent['text']) > 20 and score > 0:
            key_points.append({
                'text': sent['text'],
                'timestamp': sent['timestamp_str'],
                'score': score
            })
    
    # 按重要性排序并取前 N 个
    key_points.sort(key=lambda x: x['score'], reverse=True)
    
    # 去重（避免相似的句子）
    unique_points = []
    for point in key_points[:15]:  # 最多取 15 个要点
        is_duplicate = False
        for existing in unique_points:
            # 简单相似度检查
            if len(set(point['text']) & set(existing['text'])) > len(point['text']) * 0.7:
                is_duplicate = True
                break
        if not is_duplicate:
            unique_points.append(point)
    
    # 按时间排序
    unique_points.sort(key=lambda x: x['timestamp'])
    
    print(f"[OK] Extracted {len(unique_points)} key points")
    
    return {
        'key_points': unique_points[:10],  # 最多保留 10 个要点
        'sentences': sentences
    }


def generate_summary(full_text, key_points):
    """生成内容摘要"""
    # 使用简单启发式方法生成一句话摘要
    # 取前 100 个字符作为开头
    first_sentence = full_text[:150].split('。')[0] + '。'
    
    if len(first_sentence) < 20:
        first_sentence = full_text[:200] + '...'
    
    return first_sentence


def generate_markdown(video_path, video_duration, transcription, analysis, include_full_transcript=True):
    """生成 Markdown 格式的纪要文档"""
    
    # 基本信息
    video_name = Path(video_path).name
    processed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    md_content = f"""# 视频纪要：{video_name}

## 基本信息

| 项目 | 内容 |
|------|------|
| **视频文件** | `{video_name}` |
| **视频时长** | {video_duration} |
| **处理时间** | {processed_time} |
| **字幕语言** | {transcription.get('language', 'auto-detect')} |

---

## 内容摘要

{generate_summary(transcription['text'], analysis['key_points'])}

---

## 核心要点

"""
    
    # 添加核心要点
    for i, point in enumerate(analysis['key_points'], 1):
        md_content += f"### {i}. {point['text']}\n\n"
        md_content += f"> **时间戳**：[{point['timestamp']}]({video_path}#t={point['timestamp']})\n\n"
        md_content += f"\n"
    
    md_content += """---

## 详细时间线

"""
    
    # 添加时间线（每 30 秒一个节点）
    timeline_points = []
    current_time = 0
    interval = 30  # 30 秒一个节点
    
    for sent in analysis['sentences']:
        if sent['timestamp'] >= current_time:
            timeline_points.append(sent)
            current_time += interval
    
    for point in timeline_points[:20]:  # 最多 20 个时间点
        md_content += f"- **[{point['timestamp_str']}]** {point['text']}\n"
    
    md_content += "\n---\n\n"
    
    # 可选：完整字幕
    if include_full_transcript:
        md_content += """## 原文字幕

<details>
<summary>点击展开完整字幕</summary>

"""
        for seg in transcription['segments']:
            timestamp = format_timestamp(seg['start'])
            md_content += f"**[{timestamp}]** {seg['text'].strip()}\n\n"
        
        md_content += """
</details>

---

"""
    
    md_content += """## 备注

- 本纪要由 AI 自动生成，仅供参考
- 如需修改，请直接编辑本文档
- 时间戳可点击跳转（支持的视频播放器）

---

*Generated by Video Minutes Skill*
"""
    
    return md_content


def main():
    parser = argparse.ArgumentParser(
        description='生成视频纪要 - 提取语音、转录、总结'
    )
    parser.add_argument('video', help='视频文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径（默认为视频名.md）')
    parser.add_argument('--model', default='base', 
                        choices=['tiny', 'base', 'small', 'medium', 'large'],
                        help='Whisper 模型（默认: base）')
    parser.add_argument('--language', help='语言代码（如 zh, en, ja）')
    parser.add_argument('--no-transcript', action='store_true',
                        help='不包含完整字幕')
    
    args = parser.parse_args()
    
    video_path = Path(args.video)
    
    # Check video file
    if not video_path.exists():
        print(f"[ERROR] Video file not found: {video_path}")
        sys.exit(1)
    
    # Check dependencies
    print("=" * 50)
    print("Video Minutes Generator")
    print("=" * 50)
    
    if not check_ffmpeg():
        sys.exit(1)
    
    if not check_whisper():
        sys.exit(1)
    
    # Get video info
    print(f"\n[FILE] Video: {video_path.name}")
    video_duration = get_video_duration(video_path)
    if video_duration:
        print(f"[INFO] Duration: {video_duration}")
    
    # Create temp directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract audio
        audio_path = Path(temp_dir) / "audio.wav"
        if not extract_audio(video_path, audio_path):
            sys.exit(1)
        
        # Transcribe audio
        transcription = transcribe_audio(
            audio_path,
            model_name=args.model,
            language=args.language
        )
        
        if not transcription:
            sys.exit(1)
        
        # Analyze content
        analysis = analyze_content(
            transcription['segments'],
            transcription['text']
        )
        
        # Generate Markdown
        md_content = generate_markdown(
            video_path,
            video_duration or "Unknown",
            transcription,
            analysis,
            include_full_transcript=not args.no_transcript
        )
        
        # Determine output path
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = video_path.with_suffix('.md')
        
        # Write file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"\n" + "=" * 50)
        print(f"[DONE] Video minutes saved: {output_path}")
        print(f"=" * 50)


if __name__ == '__main__':
    main()
