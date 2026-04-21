"""
标题页布局
"""

from ..base import BaseLayout
from ..registry import register_layout
from ...models import Slide


@register_layout
class TitleLayout(BaseLayout):
    """标题页 - Hero风格，大标题居中"""

    @property
    def layout_type(self) -> str:
        return "title"

    def render(self, slide: Slide) -> str:
        content = slide.content
        title = self._escape(content.title)
        subtitle = self._escape(content.subtitle) if content.subtitle else ""

        subtitle_html = f'<p class="subtitle">{subtitle}</p>' if subtitle else ""

        inner = f"""
        <div class="center-content">
            <div class="deco-line" style="margin: 0 auto 48px;"></div>
            <h1 class="gradient">{title}</h1>
            {subtitle_html}
        </div>
        """

        return self._wrap_slide(inner, slide)
