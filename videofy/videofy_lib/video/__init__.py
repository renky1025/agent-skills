"""
videofy 视频模块
"""

from .capture import capture_slides
from .ffmpeg import create_video

__all__ = ['capture_slides', 'create_video']
