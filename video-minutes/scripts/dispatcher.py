#!/usr/bin/env python3
"""
任务分发器
将提取的行动项分发给对应的 skill
"""

import re
from datetime import datetime
from typing import Dict, List


class TaskDispatcher:
    """任务分发器"""

    # Tag 到 skill 的映射
    TAG_MAPPING = {
        "@user": {
            "skill": "notification",
            "description": "通知用户"
        },
        "@assistant": {
            "skill": "builtin",
            "description": "AI 直接执行"
        },
        "@Codex": {
            "skill": "agent-swarm",
            "description": "代码编写任务"
        },
        "@Claude": {
            "skill": "agent-swarm",
            "description": "前端/设计任务"
        },
        "@article": {
            "skill": "content-publisher",
            "description": "文章发布任务"
        },
        "@reminder": {
            "skill": "cron",
            "description": "定时提醒任务"
        },
        "@research": {
            "skill": "web_search",
            "description": "信息调研任务"
        },
        "@design": {
            "skill": "image-gen",
            "description": "设计生成任务"
        },
        "@meeting": {
            "skill": "calendar",
            "description": "会议安排任务"
        },
        "@review": {
            "skill": "notification",
            "description": "审核通知"
        }
    }

    def __init__(self, config: dict):
        self.config = config
        self.confirm_before_dispatch = config.get("dispatch", {}).get("confirm_before_dispatch", True)
        self.auto_dispatch_tags = config.get("dispatch", {}).get("auto_dispatch_tags", ["@reminder"])

    def extract_tags(self, text: str) -> List[str]:
        """从文本中提取 @tags"""
        tag_pattern = r'@\w+'
        tags = re.findall(tag_pattern, text)
        return list(set(tags))  # 去重

    def parse_action_items(self, transcript: str, video_type: str) -> List[Dict]:
        """
        从转录文本中解析行动项
        实际实现应该调用 AI 模型
        """
        # 模拟实现
        action_items = []

        # 基于视频类型的提取规则
        if video_type == "meeting":
            # 会议类型提取 TODO
            action_items = self._extract_meeting_actions(transcript)
        elif video_type == "lecture":
            # 课程类型提取学习任务
            action_items = self._extract_lecture_actions(transcript)

        return action_items

    def _extract_meeting_actions(self, transcript: str) -> List[Dict]:
        """提取会议行动项"""
        actions = []

        # 简单的模式匹配 (实际应该用 AI)
        patterns = [
            r'([^，。]+)负责([^，。]+)',
            r'@(\w+)[:\s]*([^，。]+)',
            r'(下周|明天|本周|月底前)[^，。]*完成([^，。]+)'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, transcript)
            for match in matches:
                if isinstance(match, tuple):
                    task = " ".join(match)
                else:
                    task = match

                # 检测标签
                tags = self.extract_tags(task)
                if not tags:
                    # 默认标签
                    if "代码" in task or "开发" in task:
                        tags = ["@Codex"]
                    elif "文章" in task or "博客" in task:
                        tags = ["@article"]
                    elif "提醒" in task:
                        tags = ["@reminder"]
                    else:
                        tags = ["@user"]

                actions.append({
                    "task": task,
                    "tags": tags,
                    "timestamp": None,
                    "context": transcript[:200]  # 上下文
                })

        return actions

    def _extract_lecture_actions(self, transcript: str) -> List[Dict]:
        """提取课程学习任务"""
        actions = []

        # 提取学习要点
        key_points = re.findall(r'(重点|关键|注意|记住)[^，。]+', transcript)
        for point in key_points:
            actions.append({
                "task": f"复习: {point}",
                "tags": ["@assistant"],
                "timestamp": None,
                "context": transcript[:200]
            })

        return actions

    def dispatch(self, action_item: Dict) -> Dict:
        """分发单个任务"""
        tags = action_item.get("tags", [])

        results = []
        for tag in tags:
            if tag in self.TAG_MAPPING:
                mapping = self.TAG_MAPPING[tag]
                result = self._dispatch_to_skill(action_item, tag, mapping)
                results.append(result)
            else:
                results.append({
                    "tag": tag,
                    "success": False,
                    "message": f"未知标签: {tag}"
                })

        return {
            "action_item": action_item,
            "results": results
        }

    def dispatch_batch(self, action_items: List[Dict]) -> List[Dict]:
        """批量分发任务"""
        results = []
        for item in action_items:
            result = self.dispatch(item)
            results.extend(result["results"])
        return results

    def _dispatch_to_skill(self, action_item: Dict, tag: str, mapping: Dict) -> Dict:
        """分发到具体 skill"""
        skill = mapping["skill"]
        task = action_item.get("task", "")

        # 模拟分发 (实际实现应该调用 skill 的 API)
        dispatch_methods = {
            "agent-swarm": self._dispatch_to_agent_swarm,
            "cron": self._dispatch_to_cron,
            "content-publisher": self._dispatch_to_publisher,
            "notification": self._dispatch_notification,
        }

        method = dispatch_methods.get(skill, self._default_dispatch)
        return method(action_item, tag)

    def _dispatch_to_agent_swarm(self, action_item: Dict, tag: str) -> Dict:
        """分发到 agent-swarm"""
        # 模拟实现
        return {
            "tag": tag,
            "skill": "agent-swarm",
            "success": True,
            "message": "任务已发送至 agent-swarm",
            "link": f"#task-{hash(action_item['task']) % 10000}"
        }

    def _dispatch_to_cron(self, action_item: Dict, tag: str) -> Dict:
        """分发到 cron"""
        # 检测是否有 cron 表达式
        task = action_item.get("task", "")
        cron_match = re.search(r'(\d{1,2})\s+(\d{1,2})\s+\*\s+\*\s+(\*|\d)', task)

        if cron_match:
            # 有 cron 表达式
            return {
                "tag": tag,
                "skill": "cron",
                "success": True,
                "message": "定时任务已创建",
                "cron": " ".join(cron_match.groups())
            }
        else:
            # 普通提醒
            return {
                "tag": tag,
                "skill": "cron",
                "success": True,
                "message": "提醒任务已添加",
                "time": "待用户确认"
            }

    def _dispatch_to_publisher(self, action_item: Dict, tag: str) -> Dict:
        """分发到内容发布器"""
        return {
            "tag": tag,
            "skill": "content-publisher",
            "success": True,
            "message": "文章草稿已创建",
            "link": f"~/Drafts/article-{datetime.now().strftime('%Y%m%d')}.md"
        }

    def _dispatch_notification(self, action_item: Dict, tag: str) -> Dict:
        """发送通知"""
        return {
            "tag": tag,
            "skill": "notification",
            "success": True,
            "message": f"通知已发送: {action_item.get('task', '')}",
        }

    def _default_dispatch(self, action_item: Dict, tag: str) -> Dict:
        """默认分发"""
        return {
            "tag": tag,
            "success": False,
            "message": f"未实现的分发目标: {tag}"
        }

    def should_auto_dispatch(self, action_item: Dict) -> bool:
        """判断是否应该自动分发"""
        tags = action_item.get("tags", [])
        return any(tag in self.auto_dispatch_tags for tag in tags)
