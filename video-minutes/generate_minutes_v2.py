#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频纪要生成工具 v2.0
自动提取视频语音、深度分析、生成结构化纪要文档
"""

import os
import sys
import json
import argparse
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any

# 导入分析模块
sys.path.insert(0, str(Path(__file__).parent))
from video_analyzer import VideoAnalyzer


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


def prepare_segments(transcription):
    """准备标准化的段落数据"""
    sentences = []
    for seg in transcription['segments']:
        text = seg['text'].strip()
        start = seg['start']
        if text:
            sentences.append({
                'text': text,
                'timestamp': start,
                'timestamp_str': format_timestamp(start)
            })
    return sentences


def generate_deep_analysis_markdown(video_path, video_duration, transcription, deep_analysis, include_full_transcript=True):
    """生成深度分析的 Markdown 文档"""
    
    video_name = Path(video_path).name
    processed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 生成内容概述
    content_type_names = {
        'tutorial': '教学教程',
        'lecture': '知识讲解',
        'review': '评测分析',
        'story': '案例故事',
        'news': '资讯报道'
    }
    
    content_type = content_type_names.get(deep_analysis['content_type'], '内容分享')
    theme = deep_analysis['main_theme']
    
    md_content = f"""# 视频深度纪要：{video_name}

## 基本信息

| 项目 | 内容 |
|------|------|
| **视频文件** | `{video_name}` |
| **视频时长** | {video_duration} |
| **处理时间** | {processed_time} |
| **字幕语言** | {transcription.get('language', 'auto-detect')} |
| **内容类型** | {content_type} |

---

## 内容概述

### 主题与关键词

**核心主题**: {theme['description']}

**关键词**: {', '.join(theme['keywords'][:5])}

**开场白**: 
> {theme['opening_hint'][:150]}...

### 视频主旨

"""
    
    # 添加主旨描述
    if deep_analysis['core_arguments']:
        main_arg = deep_analysis['core_arguments'][0]['argument']
        md_content += f"本视频围绕**{theme['keywords'][0] if theme['keywords'] else '核心主题'}**展开深度讲解，"
        md_content += f"主要阐述「{main_arg[:80]}」等重要观点。"
    else:
        md_content += f"本视频系统性地讲解了**{theme['keywords'][0] if theme['keywords'] else '相关主题'}**的内容，"
        md_content += "提供了全面的知识体系和实用方法。"
    
    md_content += """

---

## 核心论点与论据

"""
    
    # 添加核心论点
    for i, arg in enumerate(deep_analysis['core_arguments'], 1):
        md_content += f"### 论点 {i}: {arg['argument'][:60]}{'...' if len(arg['argument']) > 60 else ''}\n\n"
        md_content += f"**时间**: [{arg['timestamp']}]({video_path}#t={arg['timestamp']})  "
        md_content += f"**论据强度**: {'★' * min(arg['strength'], 5)}\n\n"
        
        if arg['evidence']:
            md_content += "**支持论据**:\n"
            for ev in arg['evidence']:
                md_content += f"- [{ev['timestamp']}] {ev['text'][:80]}{'...' if len(ev['text']) > 80 else ''}\n"
        
        md_content += "\n"
    
    md_content += """---

## 内容结构分析

"""
    
    # 添加章节分析
    md_content += "### 章节划分\n\n"
    md_content += "| 章节 | 时间范围 | 核心内容 |\n"
    md_content += "|------|----------|----------|\n"
    
    for chapter in deep_analysis['chapters']:
        title = chapter['title'] if chapter['title'] else f"段落 {chapter['index']}"
        time_range = chapter['time_range']
        summary = chapter['summary'][:60] + '...' if len(chapter['summary']) > 60 else chapter['summary']
        md_content += f"| {title} | {time_range} | {summary} |\n"
    
    md_content += "\n### 各章节要点\n\n"
    
    for chapter in deep_analysis['chapters']:
        title = chapter['title'] if chapter['title'] else f"段落 {chapter['index']}"
        md_content += f"#### {chapter['index']}. {title}\n\n"
        
        if chapter['key_points']:
            for point in chapter['key_points']:
                md_content += f"- **[{point['timestamp']}]** {point['text']}\n"
        else:
            md_content += f"*{chapter['summary'][:100]}...*\n"
        
        md_content += "\n"
    
    md_content += """---

## 实用价值提炼

"""
    
    # 添加实用要点
    if deep_analysis['practical_value']:
        md_content += "### 方法与技巧\n\n"
        
        methods = [item for item in deep_analysis['practical_value'] if item['type'] == 'method']
        advice = [item for item in deep_analysis['practical_value'] if item['type'] == 'advice']
        
        if methods:
            md_content += "**操作步骤**: \n\n"
            for i, method in enumerate(methods[:5], 1):
                md_content += f"{i}. [{method['timestamp']}] {method['content'][:100]}\n"
            md_content += "\n"
        
        if advice:
            md_content += "**重要建议**: \n\n"
            for i, adv in enumerate(advice[:5], 1):
                md_content += f"{i}. [{adv['timestamp']}] {adv['content'][:100]}\n"
            md_content += "\n"
    else:
        md_content += "本视频以理论讲解为主，未检测到明确的操作步骤或方法指导。\n\n"
    
    md_content += """---

## 关键洞察总结

"""
    
    # 生成关键洞察
    all_key_points = []
    for chapter in deep_analysis['chapters']:
        all_key_points.extend(chapter['key_points'])
    
    if all_key_points:
        # 按重要性排序
        all_key_points.sort(key=lambda x: x.get('score', 0), reverse=True)
        md_content += "### 最重要的5个要点\n\n"
        for i, point in enumerate(all_key_points[:5], 1):
            md_content += f"**{i}.** {point['text']}\n"
            md_content += f"   > 时间: [{point['timestamp']}]({video_path}#t={point['timestamp']})\n\n"
    
    md_content += """---

## 内容评价

"""
    
    # 生成内容评价
    md_content += "### 内容质量\n\n"
    
    arg_count = len(deep_analysis['core_arguments'])
    chapter_count = len(deep_analysis['chapters'])
    practical_count = len(deep_analysis['practical_value'])
    
    md_content += f"- **逻辑性**: 视频包含{arg_count}个明确论点，结构{'清晰' if arg_count >= 3 else '一般'}\n"
    md_content += f"- **层次感**: 内容分为{chapter_count}个章节，层层递进\n"
    md_content += f"- **实用性**: 提取到{practical_count}个实用要点，{'实操性强' if practical_count >= 5 else '以理论为主'}\n"
    md_content += f"- **信息密度**: 共{len(transcription['segments'])}个字幕片段，内容充实\n"
    
    md_content += "\n### 适用人群\n\n"
    
    if deep_analysis['content_type'] == 'tutorial':
        md_content += "- 适合想要系统学习该主题的初学者\n"
        md_content += "- 适合需要实操指导的实践者\n"
    elif deep_analysis['content_type'] == 'lecture':
        md_content += "- 适合对该领域有一定了解的进阶学习者\n"
        md_content += "- 适合希望深入理解理论的专业人士\n"
    elif deep_analysis['content_type'] == 'story':
        md_content += "- 适合通过案例学习的观众\n"
        md_content += "- 适合希望获得启发和借鉴的人群\n"
    else:
        md_content += "- 适合对该主题感兴趣的普通观众\n"
        md_content += "- 适合希望快速了解核心要点的人群\n"
    
    md_content += """

---

## 完整字幕

<details>
<summary>点击展开完整字幕（共 """ + str(len(transcription['segments'])) + """ 条）</summary>

"""
    
    if include_full_transcript:
        for seg in transcription['segments']:
            timestamp = format_timestamp(seg['start'])
            md_content += f"**[{timestamp}]** {seg['text'].strip()}\n\n"
    
    md_content += """
</details>

---

## 备注

- 本纪要由 AI 深度分析生成，基于语音识别和内容理解
- 章节划分和要点提取基于算法分析，可能存在误差
- 建议结合视频观看以获得最佳理解
- 如需引用内容，请核对原视频确认准确性

---

*Generated by Video Minutes Skill v2.0 - Deep Analysis Mode*
"""
    
    return md_content


def main():
    parser = argparse.ArgumentParser(
        description='生成视频深度纪要 - 提取语音、深度分析、生成结构化文档'
    )
    parser.add_argument('video', help='视频文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径（默认为视频名.md）')
    parser.add_argument('--model', default='base', 
                        choices=['tiny', 'base', 'small', 'medium', 'large'],
                        help='Whisper 模型（默认: base）')
    parser.add_argument('--language', help='语言代码（如 zh, en, ja）')
    parser.add_argument('--no-transcript', action='store_true',
                        help='不包含完整字幕')
    parser.add_argument('--simple', action='store_true',
                        help='使用简单模式（仅基础分析）')
    
    args = parser.parse_args()
    
    video_path = Path(args.video)
    
    # Check video file
    if not video_path.exists():
        print(f"[ERROR] Video file not found: {video_path}")
        sys.exit(1)
    
    # Check dependencies
    print("=" * 50)
    print("Video Minutes Generator v2.0")
    print("Deep Analysis Mode")
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
        
        # Prepare segments
        sentences = prepare_segments(transcription)
        
        if args.simple:
            print("\n[INFO] Using simple analysis mode...")
            from generate_minutes import analyze_content, generate_markdown
            analysis = analyze_content(transcription['segments'], transcription['text'])
            md_content = generate_markdown(
                video_path,
                video_duration or "Unknown",
                transcription,
                analysis,
                include_full_transcript=not args.no_transcript
            )
        else:
            # Deep analysis
            print("\n[STEP 3] Performing deep content analysis...")
            analyzer = VideoAnalyzer()
            deep_analysis = analyzer.analyze_structure(
                sentences,
                transcription['text']
            )
            
            print("[STEP 4] Generating structured minutes...")
            md_content = generate_deep_analysis_markdown(
                video_path,
                video_duration or "Unknown",
                transcription,
                deep_analysis,
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
        print(f"\nDocument includes:")
        print(f"  - Content overview and theme analysis")
        print(f"  - Core arguments with evidence")
        print(f"  - Chapter structure breakdown")
        print(f"  - Practical value extraction")
        print(f"  - Complete transcript")


if __name__ == '__main__':
    main()
