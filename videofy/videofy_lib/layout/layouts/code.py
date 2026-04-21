"""
代码页布局
"""

from ..base import BaseLayout
from ..registry import register_layout
from ...models import Slide


@register_layout
class CodeLayout(BaseLayout):
    """代码展示页 - IDE风格"""

    @property
    def layout_type(self) -> str:
        return "code"

    def render(self, slide: Slide) -> str:
        content = slide.content
        title = self._escape(content.title)
        code = self._escape(content.code)
        lang = content.code_lang or "text"

        inner = f"""
        <div class="top-content">
            <div class="tag">Code</div>
            <h2>{title}</h2>
        </div>
        <div class="code-window">
            <div class="code-header">
                <div class="code-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
                <div class="code-lang">{lang}</div>
            </div>
            <div class="code-content">
                <pre><code>{code}</code></pre>
            </div>
        </div>
        """

        return self._wrap_slide(inner, slide)
