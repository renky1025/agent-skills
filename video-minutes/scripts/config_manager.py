#!/usr/bin/env python3
"""
配置管理器
处理配置文件的加载、保存和验证
"""

import json
import os
from pathlib import Path
from typing import Optional, Tuple
import yaml


class ConfigManager:
    """配置管理器"""

    DEFAULT_CONFIG = {
        "version": "1.2.0",
        "output": {
            "language": "auto",
            "format": "markdown",
            "directory": "~/Documents/video-minutes",
            "filename_template": "{date}-{type}-{title}"
        },
        "content": {
            "include_summary": True,
            "include_key_points": True,
            "include_timeline": True,
            "include_action_items": True,
            "include_transcript": True,
            "transcript_collapsed": True,
            "speaker_identification": True,
            "max_summary_points": 10
        },
        "whisper": {
            "model": "base",
            "device": "auto",
            "language": None
        },
        "classification": {
            "enabled": True,
            "confidence_threshold": 0.7
        },
        "dispatch": {
            "confirm_before_dispatch": True,
            "auto_dispatch_tags": ["@reminder"]
        },
        "scanning": {
            "enabled": True,
            "interval_minutes": 60,
            "paths": []
        },
        "integrations": {
            "obsidian_vault": None,
            "notion_database_id": None,
            "lark_webhook": None
        }
    }

    def __init__(self):
        self.project_config_path = Path(".opencode/skills/video-minutes/config.yaml")
        self.user_config_path = Path.home() / ".opencode/skills/video-minutes/config.yaml"
        self.legacy_config_path = Path.home() / ".video-minutes-config.json"

    def load_config(self) -> Tuple[Optional[dict], str]:
        """
        加载配置文件
        Returns: (config_dict, source)
        """
        # 优先级 1: 项目级配置
        if self.project_config_path.exists():
            with open(self.project_config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f), "project"

        # 优先级 2: 用户级配置
        if self.user_config_path.exists():
            with open(self.user_config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f), "user"

        # 优先级 3: 旧版 JSON 配置 (迁移)
        if self.legacy_config_path.exists():
            legacy_config = self._load_legacy_config()
            migrated_config = self._migrate_legacy_config(legacy_config)
            self.save_config(migrated_config)
            return migrated_config, "migrated"

        # 未找到配置
        return None, "none"

    def save_config(self, config: dict, location: str = "user"):
        """保存配置文件"""
        if location == "project":
            config_path = self.project_config_path
        else:
            config_path = self.user_config_path

        # 确保目录存在
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, sort_keys=False)

    def _load_legacy_config(self) -> dict:
        """加载旧版 JSON 配置"""
        with open(self.legacy_config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _migrate_legacy_config(self, legacy: dict) -> dict:
        """将旧版配置迁移到新版"""
        config = self.DEFAULT_CONFIG.copy()

        # 映射旧版字段
        if "default_model" in legacy:
            config["whisper"]["model"] = legacy["default_model"]

        if "default_language" in legacy:
            config["output"]["language"] = legacy["default_language"]

        if "include_full_transcript" in legacy:
            config["content"]["include_transcript"] = legacy["include_full_transcript"]

        if "max_summary_points" in legacy:
            config["content"]["max_summary_points"] = legacy["max_summary_points"]

        return config

    def validate_config(self, config: dict) -> Tuple[bool, list]:
        """
        验证配置有效性
        Returns: (is_valid, errors)
        """
        errors = []

        # 检查必填字段
        required_fields = ["version", "output", "whisper"]
        for field in required_fields:
            if field not in config:
                errors.append(f"缺少必填字段: {field}")

        # 检查输出目录
        output_dir = config.get("output", {}).get("directory", "")
        if output_dir:
            expanded_path = Path(output_dir).expanduser()
            if not expanded_path.parent.exists():
                try:
                    expanded_path.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    errors.append(f"无法创建输出目录: {e}")

        # 检查模型名称
        valid_models = ["tiny", "base", "small", "medium", "large"]
        model = config.get("whisper", {}).get("model", "")
        if model not in valid_models:
            errors.append(f"无效模型名称: {model}")

        # 检查输出格式
        valid_formats = ["markdown", "obsidian", "notion", "lark"]
        fmt = config.get("output", {}).get("format", "")
        if fmt not in valid_formats:
            errors.append(f"无效输出格式: {fmt}")

        return len(errors) == 0, errors

    def create_default_config(self) -> dict:
        """创建默认配置"""
        return self.DEFAULT_CONFIG.copy()

    def detect_recording_paths(self) -> list:
        """自动检测录制软件目录"""
        paths = []

        # Zoom
        zoom_path = Path.home() / "Documents/Zoom"
        if zoom_path.exists():
            paths.append(str(zoom_path))

        # 腾讯会议
        tx_path = Path.home() / "Documents/腾讯会议"
        if tx_path.exists():
            paths.append(str(tx_path))

        # 钉钉
        dd_path = Path.home() / "Documents/DingTalk"
        if dd_path.exists():
            paths.append(str(dd_path))

        return paths
