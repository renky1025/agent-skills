"""
主题封面布局
"""

from ..base import BaseLayout
from ..registry import register_layout
from ...models import Slide


@register_layout
class TopicCoverLayout(BaseLayout):
    """主题封面 - 章节起始页"""

    @property
    def layout_type(self) -> str:
        return "topic_cover"

    def render(self, slide: Slide) -> str:
        content = slide.content
        title = self._escape(content.title)
        subtitle = self._escape(content.subtitle) if content.subtitle else ""

        subtitle_html = f'<p class="subtitle large">{subtitle}</p>' if subtitle else ""

        inner = f"""
        <div class="center-content">
            <div class="deco-line" style="margin: 0 auto 40px;"></div>
            <h1>{title}</h1>
            {subtitle_html}
        </div>
        """

        return self._wrap_slide(inner, slide, "topic-cover")
