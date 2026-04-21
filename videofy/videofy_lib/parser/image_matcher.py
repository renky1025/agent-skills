"""
图片匹配器 - 将 Markdown 中的图片引用与本地图片文件匹配
"""

import os
import re
from typing import Dict, List, Optional, Tuple


class ImageMatcher:
    """图片匹配器"""

    def __init__(self, images_dir: Optional[str] = None):
        self.images_dir = images_dir
        self.image_cache: Dict[str, str] = {}
        self._build_cache()

    def _build_cache(self):
        """构建图片缓存"""
        if not self.images_dir or not os.path.exists(self.images_dir):
            return

        for root, _, files in os.walk(self.images_dir):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                    full_path = os.path.join(root, file)
                    # 用多种方式索引
                    self.image_cache[file.lower()] = full_path
                    self.image_cache[file] = full_path
                    # 去掉扩展名
                    name_no_ext = os.path.splitext(file)[0].lower()
                    self.image_cache[name_no_ext] = full_path

    def find_image(self, reference: str) -> Optional[str]:
        """
        根据引用找到图片文件
        reference 可以是：
        - 完整文件名: "image.png"
        - 相对路径: "./images/image.png"
        - 仅名称: "image"
        """
        if not reference:
            return None

        # 提取文件名
        basename = os.path.basename(reference).lower()

        # 直接查找
        if basename in self.image_cache:
            return self.image_cache[basename]

        # 去掉扩展名查找
        name_no_ext = os.path.splitext(basename)[0]
        if name_no_ext in self.image_cache:
            return self.image_cache[name_no_ext]

        # 模糊匹配
        for key, path in self.image_cache.items():
            if name_no_ext in key or key in name_no_ext:
                return path

        return None

    def extract_images_from_markdown(self, text: str) -> List[Tuple[str, str]]:
        """
        从 Markdown 文本中提取所有图片引用
        返回: [(alt_text, image_path)]
        """
        images = []
        pattern = r'!\[([^\]]*)\]\s*\(([^)]+)\)'

        for match in re.finditer(pattern, text):
            alt_text = match.group(1)
            img_ref = match.group(2)
            img_path = self.find_image(img_ref)
            if img_path:
                images.append((alt_text, img_path))

        return images

    def match_section_images(self, section_title: str, content: str) -> List[str]:
        """
        为章节匹配相关图片
        策略：
        1. 提取内容中的图片引用
        2. 根据章节标题匹配相关图片
        """
        matched = []

        # 1. 提取内容中的图片
        content_images = self.extract_images_from_markdown(content)
        matched.extend([path for _, path in content_images])

        # 2. 根据标题关键词匹配
        title_keywords = section_title.lower().replace('_', ' ').replace('-', ' ').split()

        for key, path in self.image_cache.items():
            key_lower = key.lower()
            # 检查标题关键词是否匹配图片名
            for keyword in title_keywords:
                if len(keyword) > 2 and keyword in key_lower:
                    if path not in matched:
                        matched.append(path)
                    break

        return matched

    def get_best_image_for_content(self, content: str, section_title: str = "") -> Optional[str]:
        """获取最适合内容的图片"""
        images = self.extract_images_from_markdown(content)

        if images:
            # 优先使用 Markdown 中引用的第一张图片
            return images[0][1]

        # 尝试按章节标题匹配
        if section_title:
            matched = self.match_section_images(section_title, content)
            if matched:
                return matched[0]

        return None
