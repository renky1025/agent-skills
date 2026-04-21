#!/usr/bin/env python3
"""
Video Dubbing Pipeline - 优化版

解决三个问题：
1. 音色一致：使用参考音频保持同一人声
2. 剥离原字幕：检测并遮盖原字幕区域
3. 同步字幕：根据实际 TTS 时长动态调整字幕时间

集成 translate-polisher 和 mlx-tts 的完整流程：
视频 → 人声分离 → 字幕提取 → translate-polisher 精翻 → mlx-tts 合成 → 合并
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import time


@dataclass
class Segment:
    """字幕片段"""
    start: float
    end: float
    text: str
    translated_text: str = ""
    audio_file: str = ""
    actual_duration: float = 0.0  # TTS 实际时长


class VideoDubber:
    """视频配音器 - 集成 translate-polisher 和 mlx-tts"""

    def __init__(
        self,
        input_video: str,
        target_lang: str = "zh",
        output_path: str = None,
        voice_prompt: str = "a warm, professional female voice, clear and natural",
        keep_temp: bool = False,
        skip_if_exists: bool = True,
        translate_style: str = "auto",
        translate_audience: str = "general",
        subtitle_area: str = None,  # 原字幕区域 "x,y,w,h"
    ):
        self.input_video = Path(input_video).resolve()
        self.target_lang = target_lang
        self.voice_prompt = voice_prompt
        self.keep_temp = keep_temp
        self.skip_if_exists = skip_if_exists
        self.translate_style = translate_style
        self.translate_audience = translate_audience
        self.subtitle_area = subtitle_area  # 原字幕位置

        # 设置输出目录
        if output_path:
            self.output_dir = Path(output_path).parent
            self.output_file = Path(output_path)
        else:
            self.output_dir = self.input_video.parent / f"{self.input_video.stem}_dubbed"
            self.output_file = self.output_dir / f"{self.input_video.stem}_{target_lang}.mp4"

        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 临时文件路径
        self.audio_path = self.output_dir / "audio.wav"
        self.vocals_path = self.output_dir / "vocals.wav"
        self.no_vocals_path = self.output_dir / "no_vocals.wav"
        self.segments_path = self.output_dir / "segments.json"
        self.translated_segments_path = self.output_dir / "segments_translated.json"
        self.dubbed_audio_path = self.output_dir / "dubbed_audio.wav"
        self.reference_voice_path = self.output_dir / "reference_voice.wav"

        # 翻译工作目录
        self.translate_work_dir = self.output_dir / "translate_work"

    def run(self, step: str = None):
        """执行完整流程或指定步骤"""
        steps = [
            ("extract", self.extract_audio),
            ("separate", self.separate_vocals),
            ("transcribe", self.transcribe),
            ("translate", self.translate_with_polisher),
            ("synthesize", self.synthesize_with_mlxtts_consistent),
            ("merge", self.merge_video_with_subtitles),
        ]

        if step:
            for name, func in steps:
                if name == step:
                    func()
                    return
            print(f"未知步骤: {step}")
            sys.exit(1)
        else:
            for name, func in steps:
                print(f"\n{'='*60}")
                print(f"步骤: {name}")
                print('='*60)
                func()

        print(f"\n✅ 完成！输出文件: {self.output_file}")

    def extract_audio(self):
        """Step 1: 从视频提取音频"""
        if self.skip_if_exists and self.audio_path.exists():
            print(f"跳过: {self.audio_path} 已存在")
            return

        print(f"提取音频: {self.input_video}")
        cmd = [
            "ffmpeg", "-y",
            "-i", str(self.input_video),
            "-vn", "-acodec", "pcm_s16le",
            "-ar", "44100", "-ac", "2",
            str(self.audio_path)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"音频已保存: {self.audio_path}")

    def separate_vocals(self):
        """Step 2: 使用 Demucs 分离人声和背景音乐"""
        if self.skip_if_exists and self.vocals_path.exists():
            print(f"跳过: 人声分离文件已存在")
            return

        print("分离人声和背景音 (使用 Demucs)...")

        cmd = [
            "python3", "-m", "demucs",
            "--two-stems=vocals",
            "-o", str(self.output_dir),
            str(self.audio_path)
        ]
        subprocess.run(cmd, check=True)

        # Demucs 输出到子目录，移动文件
        demucs_output = self.output_dir / "htdemucs" / "audio"
        if (demucs_output / "vocals.wav").exists():
            (demucs_output / "vocals.wav").replace(self.vocals_path)
            (demucs_output / "no_vocals.wav").replace(self.no_vocals_path)
            # 清理空目录
            import shutil
            shutil.rmtree(self.output_dir / "htdemucs")

        print(f"人声: {self.vocals_path}")
        print(f"背景音: {self.no_vocals_path}")

    def transcribe(self):
        """Step 3: 使用 Whisper 转录音频为字幕"""
        if self.skip_if_exists and self.segments_path.exists():
            print(f"跳过: 字幕文件已存在")
            return

        print("转录音频 (使用 Whisper)...")

        import whisper

        model = whisper.load_model("base")
        result = model.transcribe(
            str(self.vocals_path),
            language="en" if self.target_lang != "en" else "zh",
            task="transcribe",
            verbose=True,
        )

        # 保存 segment 信息
        segments_data = []
        for seg in result["segments"]:
            segments_data.append({
                "id": seg["id"],
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"].strip(),
                "translated": "",
                "actual_duration": 0.0,
            })

        with open(self.segments_path, "w", encoding="utf-8") as f:
            json.dump(segments_data, f, ensure_ascii=False, indent=2)

        print(f"转录完成: {len(segments_data)} 个片段")
        print(f"保存至: {self.segments_path}")

    def translate_with_polisher(self):
        """Step 4: 准备翻译文件供 translate-polisher 处理"""
        if self.skip_if_exists and self.translated_segments_path.exists():
            print(f"跳过: 翻译文件已存在")
            return

        print("准备翻译文件...")
        print("=" * 60)
        print("请使用 translate-polisher skill 翻译以下内容：")
        print("=" * 60)

        # 加载原始字幕
        with open(self.segments_path, "r", encoding="utf-8") as f:
            segments = json.load(f)

        # 创建待翻译的 markdown 文件
        source_file = self.output_dir / "to_translate.md"

        # 构建翻译内容（带时间戳便于理解上下文）
        content_lines = ["# 视频字幕翻译\n"]
        content_lines.append("## 上下文")
        content_lines.append("这是一个 Blender 3D 建模软件教程视频的字幕。")
        content_lines.append("目标读者：技术爱好者、3D 建模初学者\n")
        content_lines.append("---\n")

        for i, seg in enumerate(segments):
            content_lines.append(f"### 片段 {i+1}")
            content_lines.append(f"**时间**: {seg['start']:.1f}s - {seg['end']:.1f}s")
            content_lines.append(f"**原文**: {seg['text']}")
            content_lines.append(f"**翻译**: \n")  # 留空给用户填写
            content_lines.append("")

        content = "\n".join(content_lines)

        # 保存待翻译文件
        with open(source_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"\n待翻译文件已保存: {source_file}")
        print("\n请执行以下命令进行翻译：")
        print(f"  /translate --from en --to zh --audience technical --style conversational {source_file}")
        print("\n翻译完成后，请将译文按以下格式保存到：")
        translated_file = self.output_dir / "translated.md"
        print(f"  {translated_file}")
        print("\n格式要求：")
        print("  - 每个片段的翻译放在 '**翻译**: ' 后面")
        print("  - 保持片段顺序一致")
        print("  - 只输出译文，不输出其他内容")

        # 检查是否已经有翻译文件
        if translated_file.exists():
            print(f"\n检测到翻译文件已存在: {translated_file}")
            self._parse_translated_markdown(translated_file, segments)
        else:
            # 尝试找到 translate-polisher 默认输出
            default_output = self.output_dir / "translation.md"
            if default_output.exists():
                print(f"\n检测到 translate-polisher 输出文件: {default_output}")
                self._parse_translated_markdown(default_output, segments)
            else:
                print("\n等待翻译...")
                print("请完成翻译后重新运行本步骤或完整流程。")
                sys.exit(0)

    def _parse_translated_markdown(self, translated_file: Path, segments):
        """解析翻译后的 markdown 文件"""
        print(f"\n解析翻译文件: {translated_file}")

        with open(translated_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 提取翻译内容 - 尝试多种格式
        translations = []

        # 方法1: 查找 **翻译**: 或 翻译: 后面的内容
        import re
        pattern = r'(?:\*\*翻译\*\*|翻译)\s*[:：]\s*(.+?)(?=\n\n|\n### |\Z)'
        matches = re.findall(pattern, content, re.DOTALL)
        if matches:
            translations = [m.strip() for m in matches if m.strip()]

        # 方法2: 如果没有找到，尝试提取所有非特殊行
        if not translations:
            lines = content.split("\n")
            for line in lines:
                line = line.strip()
                # 排除标题、元数据行、原文行
                if line and not line.startswith("#") and not line.startswith("*"):
                    if "原文:" not in line and "时间:" not in line and "片段" not in line:
                        if "上下文" not in line and "目标读者" not in line:
                            translations.append(line)

        # 更新 segments
        for i, seg in enumerate(segments):
            if i < len(translations):
                seg["translated"] = translations[i]
            else:
                seg["translated"] = seg["text"]  # 保留原文

        # 保存
        with open(self.translated_segments_path, "w", encoding="utf-8") as f:
            json.dump(segments, f, ensure_ascii=False, indent=2)

        print(f"翻译完成！已保存 {len(segments)} 个片段")

        # 显示翻译结果
        print("\n翻译结果预览:")
        for i, seg in enumerate(segments[:3]):
            print(f"  [{i+1}] {seg['translated'][:50]}...")
        if len(segments) > 3:
            print(f"  ... 共 {len(segments)} 个片段")

    def synthesize_with_mlxtts_consistent(self):
        """Step 5: 使用 mlx-tts 合成语音 - 保持音色一致"""
        if self.skip_if_exists and self.dubbed_audio_path.exists():
            print(f"跳过: 配音文件已存在")
            return

        print("合成语音 (使用 mlx-tts，保持音色一致)...")
        print(f"声音风格: {self.voice_prompt}")

        # 加载翻译后的字幕
        with open(self.translated_segments_path, "r", encoding="utf-8") as f:
            segments = json.load(f)

        # 创建临时目录
        temp_dir = self.output_dir / "tts_segments"
        temp_dir.mkdir(exist_ok=True)

        try:
            segment_files = []

            # 问题1解决方案：使用参考音频保持音色一致
            # 先生成第一个片段作为参考
            if len(segments) > 0:
                print("\n生成参考音色...")
                ref_text = segments[0].get("translated", segments[0]["text"])
                ref_output = temp_dir / "reference.wav"

                self._generate_single_tts(
                    text=ref_text[:100],  # 使用片段的前100字符生成参考
                    output_path=ref_output,
                    use_reference=False
                )

                if ref_output.exists():
                    self.reference_voice_path = ref_output
                    print(f"参考音色已生成: {ref_output}")

            # 使用参考音色生成所有片段
            for i, seg in enumerate(segments):
                text = seg.get("translated", seg["text"])
                if not text:
                    continue

                duration = seg["end"] - seg["start"]
                output_wav = temp_dir / f"segment_{i:04d}.wav"

                print(f"  [{i+1}/{len(segments)}] {text[:40]}... ({duration:.2f}s)")

                # 使用参考音频保持音色一致
                self._generate_single_tts(
                    text=text,
                    output_path=output_wav,
                    use_reference=True,
                    ref_audio=self.reference_voice_path if i > 0 else None,
                    ref_text=segments[0].get("translated", "") if i > 0 else None
                )

                if output_wav.exists():
                    # 获取实际时长
                    actual_duration = self._get_audio_duration(output_wav)
                    segments[i]["actual_duration"] = actual_duration
                    segment_files.append((output_wav, seg["start"], seg["end"], actual_duration))

            # 保存更新后的 segments（包含实际时长）
            with open(self.translated_segments_path, "w", encoding="utf-8") as f:
                json.dump(segments, f, ensure_ascii=False, indent=2)

            # 合并所有片段（按时间对齐）
            if segment_files:
                self._merge_audio_segments_with_timing(segment_files)
                print(f"配音完成: {self.dubbed_audio_path}")
            else:
                print("警告: 没有生成任何音频片段")

        finally:
            if not self.keep_temp:
                import shutil
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)

    def _generate_single_tts(self, text: str, output_path: Path,
                             use_reference: bool = False,
                             ref_audio: Path = None,
                             ref_text: str = None):
        """生成单个 TTS 音频"""
        try:
            # 检查文本长度
            max_chars = 200
            if len(text) > max_chars:
                self._generate_long_text_with_ref(text, output_path, max_chars,
                                                   ref_audio, ref_text)
            else:
                # mlx_audio.tts.generate 会创建目录结构
                # 使用临时目录，然后移动文件
                temp_output_dir = tempfile.mkdtemp()
                file_prefix = "tts_output"

                cmd = [
                    "mlx_audio.tts.generate",
                    "--model", "mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-8bit",
                    "--text", text,
                    "--instruct", self.voice_prompt,
                    "--file_prefix", file_prefix,
                    "--lang_code", "zh"
                ]

                # 使用参考音频保持音色一致
                if use_reference and ref_audio and ref_audio.exists():
                    cmd.extend(["--ref_audio", str(ref_audio)])
                    if ref_text:
                        cmd.extend(["--ref_text", ref_text[:100]])

                # 切换到临时目录执行
                import os
                original_dir = os.getcwd()
                os.chdir(temp_output_dir)
                subprocess.run(cmd, check=True, capture_output=True)
                os.chdir(original_dir)

                # 查找生成的音频文件并移动
                generated_files = list(Path(temp_output_dir).rglob("*.wav"))
                if generated_files:
                    generated_files[0].replace(output_path)

                # 清理临时目录
                import shutil
                shutil.rmtree(temp_output_dir, ignore_errors=True)

        except Exception as e:
            print(f"    TTS 生成失败: {e}")
            self._create_silence(2.0, output_path)  # 创建2秒静音

    def _generate_long_text_with_ref(self, text: str, output_path: Path,
                                      max_chars: int,
                                      ref_audio: Path = None,
                                      ref_text: str = None):
        """处理长文本，使用参考音频保持一致性"""
        sentences = re.split(r'(?<=[。！？.!?])\s+', text)
        chunks = []
        current_chunk = ""

        for sent in sentences:
            if len(current_chunk) + len(sent) < max_chars:
                current_chunk += sent
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sent
        if current_chunk:
            chunks.append(current_chunk)

        chunk_files = []
        temp_dir = tempfile.mkdtemp()

        try:
            for i, chunk in enumerate(chunks):
                chunk_temp_dir = tempfile.mkdtemp()
                file_prefix = f"chunk_{i:03d}"

                cmd = [
                    "mlx_audio.tts.generate",
                    "--model", "mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-8bit",
                    "--text", chunk,
                    "--instruct", self.voice_prompt,
                    "--file_prefix", file_prefix,
                    "--lang_code", "zh"
                ]

                # 使用参考音频
                if ref_audio and ref_audio.exists():
                    cmd.extend(["--ref_audio", str(ref_audio)])
                    if ref_text:
                        cmd.extend(["--ref_text", ref_text[:100]])

                # 在临时目录执行
                import os
                original_dir = os.getcwd()
                os.chdir(chunk_temp_dir)
                subprocess.run(cmd, check=True, capture_output=True)
                os.chdir(original_dir)

                # 查找生成的音频文件
                generated_files = list(Path(chunk_temp_dir).rglob("*.wav"))
                if generated_files:
                    chunk_files.append(generated_files[0])

                # 清理临时目录
                import shutil
                shutil.rmtree(chunk_temp_dir, ignore_errors=True)

            self._concatenate_wav_files(chunk_files, output_path)

        finally:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)

    def _get_audio_duration(self, audio_path: Path) -> float:
        """获取音频时长"""
        try:
            cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(audio_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return float(result.stdout.strip())
        except:
            return 0.0

    def _concatenate_wav_files(self, files: List[Path], output: Path):
        """合并 WAV 文件"""
        concat_file = output.parent / "concat_list.txt"
        with open(concat_file, "w") as f:
            for wav_file in files:
                f.write(f"file '{wav_file}'\n")

        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c", "copy",
            str(output)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        concat_file.unlink()

    def _merge_audio_segments_with_timing(self, segment_audios: List[Tuple[Path, float, float, float]]):
        """合并音频片段，按时间对齐"""
        # 获取视频时长
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(self.input_video)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        total_duration = float(result.stdout.strip())

        # 创建 filter_complex
        filter_parts = []
        inputs = []

        for i, (audio_path, start, end, actual_duration) in enumerate(segment_audios):
            inputs.extend(["-i", str(audio_path)])
            delay_ms = int(start * 1000)
            filter_parts.append(f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}]")

        mix_inputs = "".join([f"[a{i}]" for i in range(len(segment_audios))])
        filter_parts.append(f"{mix_inputs}amix=inputs={len(segment_audios)}:duration=longest[aout]")

        filter_complex = ";".join(filter_parts)

        cmd = [
            "ffmpeg", "-y",
            *inputs,
            "-filter_complex", filter_complex,
            "-map", "[aout]",
            "-t", str(total_duration),
            str(self.dubbed_audio_path)
        ]
        subprocess.run(cmd, check=True, capture_output=True)

    def _create_silence(self, duration: float, output_path: Path):
        """创建静音音频"""
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"anullsrc=r=44100:cl=stereo",
            "-t", str(duration),
            "-acodec", "pcm_s16le",
            str(output_path)
        ]
        subprocess.run(cmd, check=True, capture_output=True)

    def merge_video_with_subtitles(self):
        """Step 6: 合并视频、配音和中文字幕（同步）"""
        print("合并视频、配音和同步字幕...")

        # 加载翻译后的字幕（包含实际时长）
        with open(self.translated_segments_path, "r", encoding="utf-8") as f:
            segments = json.load(f)

        # 问题3解决方案：根据实际 TTS 时长重新计算字幕时间
        print("同步字幕时间...")
        synced_segments = self._sync_subtitle_timing(segments)

        # 生成同步后的 SRT 字幕
        srt_path = self.output_dir / "subtitles_zh_synced.srt"
        self._generate_synced_srt(synced_segments, srt_path)

        # 混合背景音和新人声
        final_audio = self.output_dir / "final_audio.wav"

        if self.no_vocals_path.exists():
            print("混合原始背景音...")
            cmd = [
                "ffmpeg", "-y",
                "-i", str(self.no_vocals_path),
                "-i", str(self.dubbed_audio_path),
                "-filter_complex",
                "[0:a]volume=0.2[bg];[bg][1:a]amix=inputs=2:duration=longest:weights=1 2",
                str(final_audio)
            ]
        else:
            final_audio = self.dubbed_audio_path
            cmd = ["cp", str(final_audio), str(final_audio)]

        subprocess.run(cmd, check=True, capture_output=True)

        # 问题2解决方案：遮盖原字幕区域
        video_with_masked_subtitles = self.output_dir / "video_masked.mp4"
        if self.subtitle_area:
            print(f"遮盖原字幕区域: {self.subtitle_area}")
            self._mask_subtitle_area(video_with_masked_subtitles)
            input_for_merge = video_with_masked_subtitles
        else:
            input_for_merge = self.input_video

        # 合并视频和音频
        print("生成最终视频...")
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_for_merge),
            "-i", str(final_audio),
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(self.output_file)
        ]
        subprocess.run(cmd, check=True, capture_output=True)

        print(f"✅ 视频生成成功: {self.output_file}")
        print(f"📄 同步字幕: {srt_path}")

        # 复制字幕到视频目录方便播放器自动加载
        auto_load_srt = self.input_video.parent / f"{self.input_video.stem}_zh.srt"
        import shutil
        shutil.copy(srt_path, auto_load_srt)
        print(f"📄 自动加载字幕: {auto_load_srt}")

        # 清理
        if not self.keep_temp:
            for f in [self.audio_path, self.vocals_path, self.no_vocals_path,
                      final_audio, video_with_masked_subtitles if self.subtitle_area else None]:
                if f and f.exists():
                    f.unlink()

    def _sync_subtitle_timing(self, segments: List[Dict]) -> List[Dict]:
        """根据实际 TTS 时长同步字幕时间"""
        synced = []
        current_time = 0.0

        for seg in segments:
            actual_duration = seg.get("actual_duration", seg["end"] - seg["start"])
            original_duration = seg["end"] - seg["start"]

            # 如果 TTS 比原时长长，使用 TTS 时长
            # 如果 TTS 比原时长短，使用原时长（留一点静音）
            use_duration = max(actual_duration, original_duration * 0.8)

            synced_seg = {
                "start": current_time,
                "end": current_time + use_duration,
                "text": seg.get("translated", seg["text"]),
                "original_start": seg["start"],
                "original_end": seg["end"]
            }
            synced.append(synced_seg)
            current_time += use_duration

        return synced

    def _generate_synced_srt(self, segments: List[Dict], output_path: Path):
        """生成同步后的 SRT 字幕"""
        with open(output_path, "w", encoding="utf-8") as f:
            for i, seg in enumerate(segments, 1):
                start = self._format_time(seg["start"])
                end = self._format_time(seg["end"])

                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{seg['text']}\n\n")

    def _format_time(self, seconds: float) -> str:
        """格式化为 SRT 时间格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def _mask_subtitle_area(self, output_path: Path):
        """遮盖原字幕区域"""
        if not self.subtitle_area:
            return

        # 解析区域参数 x,y,w,h
        try:
            x, y, w, h = map(int, self.subtitle_area.split(","))
        except:
            print(f"  警告: 无效的字幕区域格式 {self.subtitle_area}")
            return

        # 使用 ffmpeg drawbox 遮盖字幕区域
        cmd = [
            "ffmpeg", "-y",
            "-i", str(self.input_video),
            "-vf", f"drawbox=x={x}:y={y}:w={w}:h={h}:color=black:t=fill",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-an",
            str(output_path)
        ]
        subprocess.run(cmd, check=True, capture_output=True)


def main():
    parser = argparse.ArgumentParser(
        description="Video Dubbing Pipeline - 优化版",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 完整流程
  python video_dubbing.py input.mp4 --target-lang zh --output dubbed.mp4

  # 指定声音风格
  python video_dubbing.py input.mp4 --voice-prompt "a warm, gentle female voice"

  # 遮盖原字幕区域 (x,y,w,h)
  python video_dubbing.py input.mp4 --mask-subtitles 100,500,520,80

  # 单步执行
  python video_dubbing.py input.mp4 --step extract
        """
    )
    parser.add_argument("input", help="输入视频文件")
    parser.add_argument("--target-lang", default="zh",
                        choices=["zh", "en", "ja"],
                        help="目标语言代码 (默认: zh)")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--voice-prompt", default="a warm, professional female voice, clear and natural",
                        help="TTS 声音风格描述")
    parser.add_argument("--translate-style", default="auto",
                        choices=["auto", "formal", "technical", "conversational", "storytelling"],
                        help="翻译风格")
    parser.add_argument("--translate-audience", default="general",
                        choices=["general", "technical", "academic", "business"],
                        help="目标读者")
    parser.add_argument("--mask-subtitles", dest="subtitle_area",
                        help="遮盖原字幕区域，格式: x,y,w,h (如: 100,500,520,80)")
    parser.add_argument("--step", choices=["extract", "separate", "transcribe",
                                            "translate", "synthesize", "merge"],
                        help="执行单个步骤")
    parser.add_argument("--keep-temp", action="store_true", help="保留临时文件")
    parser.add_argument("--force", action="store_true", help="强制重新执行")

    args = parser.parse_args()

    dubber = VideoDubber(
        input_video=args.input,
        target_lang=args.target_lang,
        output_path=args.output,
        voice_prompt=args.voice_prompt,
        keep_temp=args.keep_temp,
        skip_if_exists=not args.force,
        translate_style=args.translate_style,
        translate_audience=args.translate_audience,
        subtitle_area=args.subtitle_area,
    )

    dubber.run(args.step)


if __name__ == "__main__":
    main()
