"""
目录页布局
"""

from ..base import BaseLayout
from ..registry import register_layout
from ...models import Slide


@register_layout
class AgendaLayout(BaseLayout):
    """目录页 - 网格布局展示主题"""

    @property
    def layout_type(self) -> str:
        return "agenda"

    def render(self, slide: Slide) -> str:
        bullets = slide.content.bullets if slide.content.bullets else []

        items_html = ""
        for i, item in enumerate(bullets[:8], 1):
            text = self._escape(item)
            items_html += f"""
            <div class="agenda-item">
                <div class="agenda-number">{i}</div>
                <div class="agenda-text">{text}</div>
            </div>
            """

        inner = f"""
        <div class="top-content">
            <div class="tag">目录</div>
            <h2>内容概览</h2>
        </div>
        <div class="agenda-grid">
            {items_html}
        </div>
        """

        return self._wrap_slide(inner, slide)
