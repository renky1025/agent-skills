#!/usr/bin/env python3
"""
Video Minutes - 智能视频纪要生成器
主入口脚本
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

# 添加 skill 目录到路径
SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR))

from scripts.config_manager import ConfigManager
from scripts.video_processor import VideoProcessor
from scripts.classifier import VideoClassifier
from scripts.dispatcher import TaskDispatcher


def check_first_time_setup() -> tuple[bool, Optional[dict]]:
    """检查是否需要首次设置"""
    config_manager = ConfigManager()
    config, source = config_manager.load_config()

    if config is None:
        return True, None

    return False, config


def run_setup_wizard():
    """运行首次设置向导"""
    print("🎬 Video Minutes 首次设置")
    print("=" * 50)
    print("\n未检测到配置文件，请先完成设置。\n")
    print("提示: 在实际使用中，这里会调用 AskUserQuestion 与用户交互。")
    print("由于这是命令行脚本，请手动创建配置文件:\n")
    print(f"  mkdir -p ~/.opencode/skills/video-minutes")
    print(f"  nano ~/.opencode/skills/video-minutes/config.yaml\n")
    print("或者运行交互式配置:")
    print(f"  python {SKILL_DIR}/scripts/config_wizard.py\n")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="智能视频纪要生成器 - 自动提取视频语音、生成字幕、智能分类总结"
    )
    parser.add_argument("video_path", help="视频文件路径或目录")
    parser.add_argument(
        "-o", "--output",
        help="输出文件路径 (默认自动生成)"
    )
    parser.add_argument(
        "--type",
        choices=["meeting", "lecture", "interview", "presentation", "podcast", "tutorial", "note", "auto"],
        default="auto",
        help="视频类型 (默认自动检测)"
    )
    parser.add_argument(
        "--language",
        choices=["auto", "zh", "en", "ja"],
        default="auto",
        help="输出语言"
    )
    parser.add_argument(
        "--model",
        choices=["tiny", "base", "small", "medium", "large"],
        default=None,
        help="Whisper 模型 (覆盖配置)"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "obsidian", "notion", "lark"],
        default=None,
        help="输出格式 (覆盖配置)"
    )
    parser.add_argument(
        "--transcript-only",
        action="store_true",
        help="仅提取字幕不生成纪要"
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="批量处理目录中的所有视频"
    )
    parser.add_argument(
        "--no-dispatch",
        action="store_true",
        help="禁用任务分发"
    )
    parser.add_argument(
        "--skip-confirm",
        action="store_true",
        help="跳过确认步骤 (自动分发)"
    )
    parser.add_argument(
        "--segment-duration",
        type=int,
        default=None,
        help="长视频分段处理 (秒)"
    )
    parser.add_argument(
        "--config",
        help="指定配置文件路径"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="详细输出"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.2.0"
    )

    args = parser.parse_args()

    # 检查首次设置
    needs_setup, config = check_first_time_setup()
    if needs_setup:
        run_setup_wizard()

    # 处理视频路径
    video_path = Path(args.video_path).expanduser().resolve()

    if not video_path.exists():
        print(f"❌ 错误: 路径不存在: {video_path}")
        sys.exit(1)

    # 初始化处理器
    processor = VideoProcessor(
        config=config,
        verbose=args.verbose
    )

    # 批量处理
    if args.batch or video_path.is_dir():
        video_files = list(video_path.glob("**/*.mp4")) + \
                     list(video_path.glob("**/*.mov")) + \
                     list(video_path.glob("**/*.mkv")) + \
                     list(video_path.glob("**/*.avi"))
        print(f"📁 发现 {len(video_files)} 个视频文件")

        for i, vf in enumerate(video_files, 1):
            print(f"\n[{i}/{len(video_files)}] 处理: {vf.name}")
            try:
                result = processor.process(
                    video_path=vf,
                    video_type=args.type if args.type != "auto" else None,
                    language=args.language,
                    model=args.model,
                    output_format=args.format,
                    transcript_only=args.transcript_only,
                    segment_duration=args.segment_duration
                )
                print(f"✅ 完成: {result.get('output_path', 'N/A')}")
            except Exception as e:
                print(f"❌ 失败: {e}")

    else:
        # 单个文件处理
        print(f"🎬 处理视频: {video_path.name}")

        # 步骤 1: 分类 (如果是 auto)
        if args.type == "auto":
            print("🔍 正在分析视频类型...")
            classifier = VideoClassifier(config)
            classification = classifier.classify(video_path)
            video_type = classification["type"]
            confidence = classification["confidence"]
            print(f"   检测到类型: {video_type} (置信度: {confidence:.2%})")
        else:
            video_type = args.type
            print(f"   使用指定类型: {video_type}")

        # 步骤 2: 处理
        print("📝 正在生成纪要...")
        result = processor.process(
            video_path=video_path,
            video_type=video_type,
            language=args.language,
            model=args.model,
            output_format=args.format,
            transcript_only=args.transcript_only,
            segment_duration=args.segment_duration
        )

        output_path = result.get("output_path")
        print(f"\n✅ 纪要已生成: {output_path}")

        # 步骤 3: 任务分发
        if not args.no_dispatch and result.get("action_items"):
            action_items = result["action_items"]
            print(f"\n📋 检测到 {len(action_items)} 个行动项:")

            for item in action_items:
                tags = item.get("tags", [])
                print(f"   - {item['task']} {tags}")

            if not args.skip_confirm:
                print("\n提示: 在实际使用中，这里会等待用户确认")
                print("      添加 --skip-confirm 可自动分发")
                response = input("\n是否分发这些任务? [y/N]: ")
                if response.lower() != 'y':
                    print("⏭️  跳过任务分发")
                    return

            print("\n🚀 正在分发任务...")
            dispatcher = TaskDispatcher(config)
            dispatch_results = dispatcher.dispatch_batch(action_items)

            for result in dispatch_results:
                status = "✅" if result["success"] else "❌"
                print(f"   {status} {result['tag']}: {result['message']}")

    print("\n🎉 全部完成!")


if __name__ == "__main__":
    main()
