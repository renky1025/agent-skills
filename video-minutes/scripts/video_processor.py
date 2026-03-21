#!/usr/bin/env python3
"""
视频处理器
协调音频提取、转录、分类、生成纪要的全流程
"""

import subprocess
from pathlib import Path
from typing import Dict, Optional
import whisper


class VideoProcessor:
    """视频处理器"""

    def __init__(self, config: dict, verbose: bool = False):
        self.config = config
        self.verbose = verbose
        self.whisper_model = None

    def process(self,
                video_path: Path,
                video_type: Optional[str] = None,
                language: str = "auto",
                model: Optional[str] = None,
                output_format: Optional[str] = None,
                transcript_only: bool = False,
                segment_duration: Optional[int] = None) -> Dict:
        """
        处理视频的完整流程

        Args:
            video_path: 视频文件路径
            video_type: 视频类型 (None 则自动检测)
            language: 输出语言
            model: Whisper 模型
            output_format: 输出格式
            transcript_only: 仅转录
            segment_duration: 分段处理时长

        Returns:
            处理结果字典
        """
        result = {
            "video_path": str(video_path),
            "success": False,
            "output_path": None,
            "transcript": None,
            "action_items": [],
            "error": None
        }

        try:
            # 步骤 1: 提取音频
            if self.verbose:
                print("   🔊 提取音频...")
            audio_path = self._extract_audio(video_path)

            # 步骤 2: 转录 (Whisper)
            if self.verbose:
                print("   📝 语音转文字...")
            transcript = self._transcribe(
                audio_path,
                model=model or self.config["whisper"]["model"],
                language=None if language == "auto" else language
            )
            result["transcript"] = transcript

            if transcript_only:
                # 仅转录模式
                output_path = self._save_transcript(video_path, transcript, output_format)
                result["output_path"] = output_path
                result["success"] = True
                return result

            # 步骤 3: 分类 (如果未指定)
            if video_type is None:
                if self.verbose:
                    print("   🔍 自动分类...")
                from scripts.classifier import VideoClassifier
                classifier = VideoClassifier(self.config)
                classification = classifier.classify(video_path)
                video_type = classification["type"]

            # 步骤 4: 内容分析
            if self.verbose:
                print(f"   🧠 生成 {video_type} 类型纪要...")
            content = self._analyze_content(transcript, video_type, language)

            # 步骤 5: 应用模板
            if self.verbose:
                print("   📄 应用模板...")
            formatted_output = self._apply_template(
                content,
                video_type,
                output_format or self.config["output"]["format"]
            )

            # 步骤 6: 保存输出
            output_path = self._save_output(
                video_path,
                formatted_output,
                video_type,
                output_format or self.config["output"]["format"]
            )
            result["output_path"] = output_path

            # 步骤 7: 提取行动项
            if self.config["content"]["include_action_items"]:
                from scripts.dispatcher import TaskDispatcher
                dispatcher = TaskDispatcher(self.config)
                action_items = dispatcher.parse_action_items(transcript, video_type)
                result["action_items"] = action_items

            result["success"] = True

        except Exception as e:
            result["error"] = str(e)
            if self.verbose:
                import traceback
                traceback.print_exc()

        return result

    def _extract_audio(self, video_path: Path) -> Path:
        """从视频提取音频"""
        audio_path = video_path.with_suffix(".wav")

        cmd = [
            "ffmpeg",
            "-i", str(video_path),
            "-vn",  # 不处理视频
            "-acodec", "pcm_s16le",  # 16bit PCM
            "-ar", "16000",  # 16kHz
            "-ac", "1",  # 单声道
            "-y",  # 覆盖
            str(audio_path)
        ]

        subprocess.run(cmd, check=True, capture_output=not self.verbose)
        return audio_path

    def _transcribe(self, audio_path: Path, model: str, language: Optional[str]) -> Dict:
        """使用 Whisper 转录"""
        # 加载模型 (缓存)
        if self.whisper_model is None:
            self.whisper_model = whisper.load_model(model)

        # 转录
        result = self.whisper_model.transcribe(
            str(audio_path),
            language=language,
            verbose=self.verbose
        )

        return {
            "text": result["text"],
            "segments": result["segments"],
            "language": result.get("language", "unknown")
        }

    def _analyze_content(self, transcript: Dict, video_type: str, language: str) -> Dict:
        """分析内容 (模拟实现，实际应该调用 AI)"""
        text = transcript["text"]
        segments = transcript["segments"]

        # 基础分析
        content = {
            "title": "未命名视频",
            "date": Path().stat().st_mtime if Path().exists() else None,
            "duration": segments[-1]["end"] if segments else 0,
            "summary": self._generate_summary(text),
            "key_points": self._extract_key_points(text),
            "transcript_segments": [
                {
                    "start_time": self._format_time(s["start"]),
                    "end_time": self._format_time(s["end"]),
                    "text": s["text"]
                }
                for s in segments
            ]
        }

        # 类型特定分析
        analyzers = {
            "meeting": self._analyze_meeting,
            "lecture": self._analyze_lecture,
            "interview": self._analyze_interview,
            "presentation": self._analyze_presentation,
            "podcast": self._analyze_podcast,
            "tutorial": self._analyze_tutorial,
            "note": self._analyze_note
        }

        analyzer = analyzers.get(video_type, self._default_analyze)
        specific_content = analyzer(text, segments)
        content.update(specific_content)

        return content

    def _generate_summary(self, text: str) -> str:
        """生成摘要 (模拟)"""
        # 实际应该调用 AI
        sentences = text.split("。")
        if len(sentences) > 1:
            return sentences[0] + "。"
        return text[:100] + "..."

    def _extract_key_points(self, text: str) -> list:
        """提取要点 (模拟)"""
        # 简单实现：找包含关键词的句子
        keywords = ["重要", "关键", "注意", "决定", "结论", "建议"]
        points = []
        for sentence in text.split("。"):
            for kw in keywords:
                if kw in sentence:
                    points.append(sentence.strip())
                    break
        return points[:5]  # 最多5个

    def _format_time(self, seconds: float) -> str:
        """格式化时间"""
        mins, secs = divmod(int(seconds), 60)
        hours, mins = divmod(mins, 60)
        if hours > 0:
            return f"{hours}:{mins:02d}:{secs:02d}"
        return f"{mins}:{secs:02d}"

    def _analyze_meeting(self, text: str, segments: list) -> Dict:
        """分析会议内容"""
        return {
            "meeting_type": "内部会议",
            "participants": ["参会人1", "参会人2"],  # 模拟
            "decisions": [],
            "action_items": [],
            "timeline": []
        }

    def _analyze_lecture(self, text: str, segments: list) -> Dict:
        """分析课程内容"""
        return {
            "speaker": "讲师",
            "topics": ["主题1", "主题2"],
            "chapters": [],
            "key_concepts": []
        }

    def _analyze_interview(self, text: str, segments: list) -> Dict:
        """分析访谈内容"""
        return {
            "interviewee": "受访者",
            "interviewer": "采访者",
            "qa_pairs": [],
            "key_quotes": []
        }

    def _analyze_presentation(self, text: str, segments: list) -> Dict:
        """分析演讲内容"""
        return {
            "speaker": "演讲者",
            "central_thesis": "",
            "main_arguments": [],
            "key_quotes": []
        }

    def _analyze_podcast(self, text: str, segments: list) -> Dict:
        """分析播客内容"""
        return {
            "host": "主播",
            "guest": "嘉宾",
            "topics": [],
            "key_quotes": []
        }

    def _analyze_tutorial(self, text: str, segments: list) -> Dict:
        """分析教程内容"""
        return {
            "instructor": "讲师",
            "difficulty": "中级",
            "tech_stack": [],
            "steps": []
        }

    def _analyze_note(self, text: str, segments: list) -> Dict:
        """分析笔记内容"""
        return {
            "clean_transcript": text,
            "idea_categories": [],
            "todos": []
        }

    def _default_analyze(self, text: str, segments: list) -> Dict:
        """默认分析"""
        return {}

    def _apply_template(self, content: Dict, video_type: str, output_format: str) -> str:
        """应用模板"""
        template_path = Path(__file__).parent.parent / "templates" / f"{video_type}.md"

        if not template_path.exists():
            template_path = Path(__file__).parent.parent / "templates" / "note.md"

        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()

        # 简单的变量替换 (实际应该用模板引擎如 Jinja2)
        result = template
        for key, value in content.items():
            placeholder = f"{{{{{}}}}}"
            result = result.replace(placeholder.format(key), str(value) if value else "")

        return result

    def _save_output(self, video_path: Path, content: str, video_type: str, output_format: str) -> Path:
        """保存输出文件"""
        output_dir = Path(self.config["output"]["directory"]).expanduser()
        output_dir.mkdir(parents=True, exist_ok=True)

        # 生成文件名
        from datetime import datetime
        filename = f"{datetime.now().strftime('%Y-%m-%d')}-{video_type}-{video_path.stem}.md"
        output_path = output_dir / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return output_path

    def _save_transcript(self, video_path: Path, transcript: Dict, output_format: str) -> Path:
        """仅保存字幕"""
        output_dir = Path(self.config["output"]["directory"]).expanduser()
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{video_path.stem}-transcript.txt"
        output_path = output_dir / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transcript["text"])

        return output_path
