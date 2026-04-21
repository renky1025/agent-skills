"""
布局基类
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from ..models import Slide
from ..config import THEMES


class BaseLayout(ABC):
    """布局基类"""

    def __init__(self, theme: str = "linear"):
        self.theme = THEMES.get(theme, THEMES["linear"])
        self.theme_name = theme

    @property
    @abstractmethod
    def layout_type(self) -> str:
        """布局类型标识"""
        pass

    @abstractmethod
    def render(self, slide: Slide) -> str:
        """渲染为HTML"""
        pass

    def _get_css_vars(self) -> str:
        """获取CSS变量"""
        t = self.theme
        return f"""
        --bg-dark: {t['bg_dark']};
        --bg-card: {t['bg_card']};
        --bg-code: {t['bg_code']};
        --bg-elevated: {t['bg_elevated']};
        --text-primary: {t['text_primary']};
        --text-secondary: {t['text_secondary']};
        --text-muted: {t['text-muted']};
        --accent: {t['accent']};
        --accent-gradient: {t['accent_gradient']};
        --border: {t['border']};
        --border-hover: {t['border_hover']};
        """

    def _escape(self, text: str) -> str:
        """HTML转义"""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;'))

    def _nl2br(self, text: str) -> str:
        """换行转br"""
        return text.replace('\n', '<br>')

    def _wrap_slide(self, content: str, slide: Slide, extra_class: str = "") -> str:
        """包装幻灯片容器"""
        progress = (slide.slide_number / slide.total_slides) * 100 if slide.total_slides > 0 else 0

        return f"""
        <div class="slide {extra_class}" id="slide-{slide.slide_number}">
            <div class="bg-gradient-top"></div>
            <div class="bg-gradient-bottom"></div>
            <div class="bg-grid"></div>
            {content}
            <div class="slide-number">{slide.slide_number} / {slide.total_slides}</div>
            <div class="progress-bar" style="width: {progress}%"></div>
        </div>
        """
