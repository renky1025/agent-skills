#!/usr/bin/env python3
"""
视频类型分类器
基于音频特征和内容采样自动分类视频类型
"""

import re
from pathlib import Path
from typing import Dict


class VideoClassifier:
    """视频类型分类器"""

    VIDEO_TYPES = {
        "meeting": {
            "keywords": ["会议", "讨论", "周会", "例会", "review", "sync", "standup", "站会"],
            "indicators": ["multiple_speakers", "task_assignment", "decision_making"],
            "duration_range": (300, 7200),  # 5分钟到2小时
        },
        "lecture": {
            "keywords": ["课程", "讲座", "教学", "tutorial", "lecture", "lesson", "class"],
            "indicators": ["structured_content", "knowledge_dense", "one_or_two_speakers"],
            "duration_range": (900, 10800),  # 15分钟到3小时
        },
        "interview": {
            "keywords": ["面试", "访谈", "采访", "interview", "q&a", "问答"],
            "indicators": ["qa_format", "two_speakers", "question_answer_pattern"],
            "duration_range": (600, 5400),  # 10分钟到1.5小时
        },
        "presentation": {
            "keywords": ["演讲", "汇报", "presentation", "talk", "keynote", "slide"],
            "indicators": ["monologue", "structured_slides", "data_visualization"],
            "duration_range": (300, 3600),  # 5分钟到1小时
        },
        "podcast": {
            "keywords": ["播客", "podcast", "对话", "conversation", "chat"],
            "indicators": ["casual_conversation", "multiple_topics", "informal"],
            "duration_range": (1800, 14400),  # 30分钟到4小时
        },
        "tutorial": {
            "keywords": ["教程", "演示", "操作", "howto", "tutorial", "demo", "guide"],
            "indicators": ["step_by_step", "screen_recording", "instructional"],
            "duration_range": (60, 3600),  # 1分钟到1小时
        },
        "note": {
            "keywords": ["备忘", "记录", "想法", "note", "memo", "idea"],
            "indicators": ["single_speaker", "self_talk", "fragmented"],
            "duration_range": (30, 600),  # 30秒到10分钟
        }
    }

    def __init__(self, config: dict):
        self.config = config
        self.confidence_threshold = config.get("classification", {}).get("confidence_threshold", 0.7)

    def classify(self, video_path: Path) -> Dict:
        """
        分类视频
        Returns: {"type": str, "confidence": float, "reasoning": str}
        """
        # 1. 从文件名提取线索
        filename_clues = self._analyze_filename(video_path.name)

        # 2. 从路径提取线索
        path_clues = self._analyze_path(video_path)

        # 3. 获取视频元数据 (时长、分辨率等)
        metadata = self._get_video_metadata(video_path)

        # 4. 综合评分
        scores = self._calculate_scores(filename_clues, path_clues, metadata)

        # 5. 选择最佳类型
        best_type = max(scores, key=scores.get)
        confidence = scores[best_type]

        # 6. 生成推理说明
        reasoning = self._generate_reasoning(best_type, filename_clues, path_clues, metadata)

        return {
            "type": best_type,
            "confidence": confidence,
            "reasoning": reasoning,
            "scores": scores
        }

    def _analyze_filename(self, filename: str) -> Dict:
        """分析文件名获取线索"""
        clues = {"keywords": [], "patterns": []}

        filename_lower = filename.lower()

        for vtype, info in self.VIDEO_TYPES.items():
            for keyword in info["keywords"]:
                if keyword.lower() in filename_lower:
                    clues["keywords"].append((vtype, keyword))

        # 日期模式 (可能是会议)
        if re.search(r'\d{4}[-_]\d{2}[-_]\d{2}', filename):
            clues["patterns"].append("date_pattern")

        # 会议模式
        if re.search(r'(meeting|会议|周会|例会|review)', filename_lower):
            clues["patterns"].append("meeting_indicator")

        return clues

    def _analyze_path(self, video_path: Path) -> Dict:
        """分析路径获取线索"""
        clues = {"folder_hints": []}

        path_str = str(video_path).lower()

        folder_mappings = {
            "meeting": ["meeting", "会议", "zoom", "腾讯会议"],
            "lecture": ["lecture", "课程", "教学", "lesson", "course"],
            "tutorial": ["tutorial", "教程", "demo", "演示"],
        }

        for vtype, folders in folder_mappings.items():
            for folder in folders:
                if folder in path_str:
                    clues["folder_hints"].append(vtype)

        return clues

    def _get_video_metadata(self, video_path: Path) -> Dict:
        """获取视频元数据"""
        # 简化实现，实际应该调用 ffprobe
        # 这里返回模拟数据
        return {
            "duration": 1800,  # 30分钟
            "width": 1920,
            "height": 1080,
            "has_audio": True
        }

    def _calculate_scores(self, filename_clues: Dict, path_clues: Dict, metadata: Dict) -> Dict:
        """计算各类型的匹配分数"""
        scores = {vtype: 0.0 for vtype in self.VIDEO_TYPES}

        # 文件名关键词匹配
        for vtype, keyword in filename_clues["keywords"]:
            scores[vtype] += 0.3

        # 路径提示匹配
        for vtype in path_clues["folder_hints"]:
            scores[vtype] += 0.2

        # 时长匹配
        duration = metadata.get("duration", 0)
        for vtype, info in self.VIDEO_TYPES.items():
            min_d, max_d = info["duration_range"]
            if min_d <= duration <= max_d:
                scores[vtype] += 0.2
            else:
                # 在范围外，根据距离扣分
                if duration < min_d:
                    scores[vtype] -= 0.1 * (min_d - duration) / min_d
                else:
                    scores[vtype] -= 0.1 * (duration - max_d) / max_d

        # 归一化
        max_score = max(scores.values()) if scores else 1
        if max_score > 0:
            scores = {k: min(v / max_score, 1.0) for k, v in scores.items()}

        return scores

    def _generate_reasoning(self, best_type: str, filename_clues: Dict, path_clues: Dict, metadata: Dict) -> str:
        """生成分类推理说明"""
        reasons = []

        if filename_clues["keywords"]:
            keywords = [k for _, k in filename_clues["keywords"]]
            reasons.append(f"文件名包含关键词: {', '.join(keywords)}")

        if path_clues["folder_hints"]:
            reasons.append(f"路径位于 {', '.join(path_clues['folder_hints'])} 相关目录")

        duration = metadata.get("duration", 0)
        minutes = duration // 60
        reasons.append(f"视频时长 {minutes} 分钟，符合 {best_type} 类型特征")

        return "; ".join(reasons)
