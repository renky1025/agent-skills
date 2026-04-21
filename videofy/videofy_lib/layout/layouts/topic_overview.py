"""
主题概览布局
"""

from ..base import BaseLayout
from ..registry import register_layout
from ...models import Slide


@register_layout
class TopicOverviewLayout(BaseLayout):
    """主题概览 - 要点卡片网格"""

    @property
    def layout_type(self) -> str:
        return "topic_overview"

    def render(self, slide: Slide) -> str:
        content = slide.content
        title = self._escape(content.title)
        bullets = content.bullets if content.bullets else []

        # 根据要点数量选择布局
        count = len(bullets[:6])

        if count <= 2:
            cards_html = self._render_large_cards(bullets[:2])
        elif count <= 4:
            cards_html = self._render_grid_cards(bullets[:4], 2)
        else:
            cards_html = self._render_grid_cards(bullets[:6], 3)

        inner = f"""
        <div class="top-content">
            <div class="tag">Overview</div>
            <h2>{title}</h2>
        </div>
        <div class="cards-container">
            {cards_html}
        </div>
        """

        return self._wrap_slide(inner, slide)

    def _render_large_cards(self, bullets: list) -> str:
        """大卡片（2个）"""
        html = ""
        for i, bullet in enumerate(bullets, 1):
            text = self._escape(bullet)
            html += f"""
            <div class="feature-card large">
                <div class="feature-number">{i}</div>
                <div class="feature-text">{text}</div>
            </div>
            """
        return f'<div class="cards-2-col">{html}</div>'

    def _render_grid_cards(self, bullets: list, cols: int) -> str:
        """网格卡片"""
        html = ""
        for i, bullet in enumerate(bullets, 1):
            text = self._escape(bullet)
            # 截断长文本
            if len(text) > 80:
                text = text[:80] + "..."
            html += f"""
            <div class="feature-card">
                <div class="feature-number">{i}</div>
                <div class="feature-text">{text}</div>
            </div>
            """
        return f'<div class="cards-{cols}-col">{html}</div>'
