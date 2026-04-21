"""
HTML 生成器
"""

import os
import shutil
from typing import List
from ..models import Slide
from ..layout.selector import LayoutSelector
from .style_system import generate_styles


class HTMLGenerator:
    """HTML 幻灯片生成器"""

    def __init__(self, output_dir: str, theme: str = "linear", lang: str = "zh"):
        self.output_dir = output_dir
        self.theme = theme
        self.lang = lang
        self.layout_selector = LayoutSelector(theme)

    def _copy_slide_images(self, slides: List[Slide]):
        """复制幻灯片中使用的图片到输出目录"""
        for slide in slides:
            if slide.content.image_path and os.path.exists(slide.content.image_path):
                img_name = f"slide_{slide.slide_number}_img.png"
                output_img = os.path.join(self.output_dir, img_name)
                try:
                    shutil.copy(slide.content.image_path, output_img)
                except Exception as e:
                    print(f"Warning: Failed to copy image for slide {slide.slide_number}: {e}")

    def generate(self, slides: List[Slide]) -> str:
        """生成完整 HTML 文件"""
        # 生成所有幻灯片 HTML
        slides_html = ""
        for slide in slides:
            layout = self.layout_selector.select_layout(slide)
            slides_html += layout.render(slide)

        # 生成完整文档
        html = f"""<!DOCTYPE html>
<html lang="{self.lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width={1920}">
    <title>Video Slides</title>
    {generate_styles(self.theme, self.lang)}
</head>
<body>
    {slides_html}
</body>
</html>"""

        return html

    def save(self, slides: List[Slide]) -> str:
        """保存 HTML 到文件"""
        # 首先复制图片
        self._copy_slide_images(slides)

        # 生成并保存HTML
        html = self.generate(slides)
        output_path = os.path.join(self.output_dir, "slides.html")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        return output_path
