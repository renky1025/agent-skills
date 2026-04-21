"""
结束页布局
"""

from ..base import BaseLayout
from ..registry import register_layout
from ...models import Slide


@register_layout
class EndLayout(BaseLayout):
    """结束页"""

    @property
    def layout_type(self) -> str:
        return "end"

    def render(self, slide: Slide) -> str:
        title = self._escape(slide.content.title)

        inner = f"""
        <div class="center-content">
            <div class="deco-line" style="margin: 0 auto 48px;"></div>
            <h1 class="gradient">{title}</h1>
            <p style="margin-top: 40px; color: var(--text-secondary); font-size: 24px;">
                Thanks for watching
            </p>
        </div>
        """

        return self._wrap_slide(inner, slide, "end-slide")
