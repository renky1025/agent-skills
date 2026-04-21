"""
主题详情布局
"""

from ..base import BaseLayout
from ..registry import register_layout
from ...models import Slide


@register_layout
class TopicDetailLayout(BaseLayout):
    """主题详情 - 列表式详细内容"""

    @property
    def layout_type(self) -> str:
        return "topic_detail"

    def render(self, slide: Slide) -> str:
        content = slide.content
        title = self._escape(content.title)
        body = content.body_text if content.body_text else []
        bullets = content.bullets if content.bullets else []

        # 组合内容
        items = body + bullets

        # 渲染列表
        items_html = ""
        for item in items[:6]:
            text = self._escape(item)
            items_html += f"<li>{text}</li>"

        inner = f"""
        <div class="top-content">
            <div class="tag">Details</div>
            <h2>{title}</h2>
        </div>
        <div class="content-area">
            <ul class="bullet-list large">
                {items_html}
            </ul>
        </div>
        """

        return self._wrap_slide(inner, slide)
