#!/usr/bin/env python3
"""
videofy v6.0 - Markdown to PowerPoint Generator
重构版：模块化设计，目录驱动，灵活布局

使用方法：
    python videofy.py <文件夹路径> [选项]

选项：
    --theme, -t     主题名称（linear/vercel/claude/indigo/emerald，默认：linear）
    --max-slides, -n 最大页面数（默认：15）
    --output, -o    输出文件路径
"""

import sys
import os

# 添加库路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from videofy_lib.cli import main

if __name__ == '__main__':
    main()
