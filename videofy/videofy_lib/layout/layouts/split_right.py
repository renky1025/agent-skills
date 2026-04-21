"""
图文混排布局 - 右图左文
"""

from ..base import BaseLayout
from ..registry import register_layout
from ...models import Slide


@register_layout
class SplitRightLayout(BaseLayout):
    """右图左文布局"""

    @property
    def layout_type(self) -> str:
        return "split_right"

    def render(self, slide: Slide) -> str:
        content = slide.content
        title = self._escape(content.title)

        # 图片
        img_html = ""
        if content.image_path:
            img_name = f"slide_{slide.slide_number}_img.png"
            img_html = f'<img src="{img_name}" alt="" />'

        # 文字内容
        text_html = ""
        if content.body_text:
            for text in content.body_text[:2]:
                text_html += f'<p class="body-text">{self._escape(text)}</p>'

        if content.bullets:
            bullets_li = ""
            for bullet in content.bullets[:4]:
                bullets_li += f"<li>{self._escape(bullet)}</li>"
            text_html += f"<ul class='bullet-list'>{bullets_li}</ul>"

        inner = f"""
        <div class="split-layout right-image">
            <div class="split-content">
                <div class="tag">{title}</div>
                {text_html}
            </div>
            <div class="split-image">
                <div class="image-frame">
                    {img_html}
                </div>
            </div>
        </div>
        """

        return self._wrap_slide(inner, slide)
