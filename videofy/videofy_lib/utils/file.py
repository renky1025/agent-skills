"""
文件工具
"""

import os
import glob
import shutil
from typing import List, Optional, Dict


def find_files(directory: str, pattern: str, recursive: bool = False) -> List[str]:
    """查找文件"""
    if recursive:
        search_path = os.path.join(directory, "**", pattern)
    else:
        search_path = os.path.join(directory, pattern)

    files = glob.glob(search_path, recursive=recursive)
    return sorted(files)


def find_images(directory: str) -> Dict[str, str]:
    """查找图片文件，返回 {basename: full_path}"""
    image_files = {}
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp', '*.svg']:
        for img in find_files(directory, ext, recursive=True):
            basename = os.path.basename(img).lower()
            image_files[basename] = img
    return image_files


def find_music(directory: str) -> List[str]:
    """查找音乐文件"""
    music_files = []
    for ext in ['*.mp3', '*.m4a', '*.aac', '*.wav', '*.flac']:
        music_files.extend(find_files(directory, ext))
    return sorted(music_files)


def ensure_dir(path: str) -> str:
    """确保目录存在"""
    os.makedirs(path, exist_ok=True)
    return path


def copy_file(src: str, dst: str) -> bool:
    """复制文件"""
    try:
        shutil.copy2(src, dst)
        return True
    except Exception as e:
        print(f"Copy failed: {e}")
        return False


def get_file_size(path: str) -> int:
    """获取文件大小（字节）"""
    try:
        return os.path.getsize(path)
    except:
        return 0


def is_image_file(path: str) -> bool:
    """检查是否是图片文件"""
    ext = os.path.splitext(path)[1].lower()
    return ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp']
