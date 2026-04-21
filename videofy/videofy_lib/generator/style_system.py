"""
样式系统 - Linear/Vercel风格CSS
"""

from ..config import THEMES, FONTS, VIDEO_WIDTH, VIDEO_HEIGHT


def generate_styles(theme_name: str = "linear", lang: str = "zh") -> str:
    """生成完整CSS样式"""
    theme = THEMES.get(theme_name, THEMES["linear"])
    fonts = FONTS.get(lang, FONTS["zh"])

    return f"""
<style>
    :root {{
        --bg-dark: {theme['bg_dark']};
        --bg-card: {theme['bg_card']};
        --bg-code: {theme['bg_code']};
        --bg-elevated: {theme['bg_elevated']};
        --text-primary: {theme['text_primary']};
        --text-secondary: {theme['text_secondary']};
        --text-muted: {theme['text_muted']};
        --accent: {theme['accent']};
        --accent-gradient: {theme['accent_gradient']};
        --accent-secondary: {theme['accent_secondary']};
        --border: {theme['border']};
        --border-hover: {theme['border_hover']};
    }}

    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}

    body {{
        font-family: {fonts['primary']};
        background: var(--bg-dark);
        color: var(--text-primary);
    }}

    .slide {{
        width: {VIDEO_WIDTH}px;
        height: {VIDEO_HEIGHT}px;
        background: var(--bg-dark);
        display: flex;
        flex-direction: column;
        padding: 80px 100px;
        position: relative;
        overflow: hidden;
    }}

    /* 背景装饰 */
    .bg-gradient-top {{
        position: absolute;
        top: -30%;
        right: -20%;
        width: 1000px;
        height: 1000px;
        background: radial-gradient(circle, var(--accent)15 0%, transparent 70%);
        border-radius: 50%;
        filter: blur(150px);
        pointer-events: none;
        z-index: 0;
    }}

    .bg-gradient-bottom {{
        position: absolute;
        bottom: -40%;
        left: -20%;
        width: 800px;
        height: 800px;
        background: radial-gradient(circle, var(--accent)10 0%, transparent 70%);
        border-radius: 50%;
        filter: blur(120px);
        pointer-events: none;
        z-index: 0;
    }}

    .bg-grid {{
        position: absolute;
        inset: 0;
        background-image:
            linear-gradient(var(--border)08 1px, transparent 1px),
            linear-gradient(90deg, var(--border)08 1px, transparent 1px);
        background-size: 80px 80px;
        pointer-events: none;
        z-index: 0;
    }}

    /* 进度条 */
    .progress-bar {{
        position: absolute;
        bottom: 0;
        left: 0;
        height: 2px;
        background: var(--accent-gradient);
        z-index: 10;
    }}

    .slide-number {{
        position: absolute;
        bottom: 30px;
        right: 100px;
        font-size: 14px;
        color: var(--text-muted);
        font-weight: 500;
        letter-spacing: 0.1em;
        z-index: 10;
    }}

    /* 内容层级 */
    .top-content {{
        z-index: 1;
        margin-bottom: 48px;
    }}

    .center-content {{
        z-index: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        text-align: center;
    }}

    /* 标题系统 */
    h1 {{
        font-size: 72px;
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -0.03em;
        color: var(--text-primary);
        margin-bottom: 24px;
    }}

    h1.gradient {{
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    h2 {{
        font-size: 48px;
        font-weight: 700;
        line-height: 1.2;
        letter-spacing: -0.02em;
        color: var(--text-primary);
        margin-bottom: 32px;
    }}

    /* 副标题 */
    .subtitle {{
        font-size: 28px;
        color: var(--text-secondary);
        line-height: 1.5;
        max-width: 80%;
    }}

    .subtitle.large {{
        font-size: 32px;
        max-width: 70%;
    }}

    /* 标签 */
    .tag {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 10px 20px;
        background: var(--accent)10;
        border: 1px solid var(--accent)30;
        border-radius: 100px;
        font-size: 14px;
        font-weight: 600;
        color: var(--accent);
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 24px;
        backdrop-filter: blur(10px);
    }}

    .tag::before {{
        content: '';
        width: 6px;
        height: 6px;
        background: var(--accent);
        border-radius: 50%;
    }}

    /* 装饰线 */
    .deco-line {{
        width: 60px;
        height: 4px;
        background: var(--accent-gradient);
        border-radius: 2px;
    }}

    /* 章节编号 */
    .chapter-number {{
        font-size: 16px;
        font-weight: 600;
        color: var(--accent);
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-bottom: 24px;
    }}

    /* 目录网格 */
    .agenda-grid {{
        z-index: 1;
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 24px;
        margin-top: 32px;
    }}

    .agenda-item {{
        display: flex;
        align-items: flex-start;
        gap: 20px;
        padding: 28px 32px;
        background: var(--bg-card);
        border-radius: 16px;
        border: 1px solid var(--border);
    }}

    .agenda-number {{
        width: 40px;
        height: 40px;
        background: var(--accent-gradient);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: 700;
        color: white;
        flex-shrink: 0;
    }}

    .agenda-text {{
        font-size: 22px;
        color: var(--text-primary);
        line-height: 1.4;
        padding-top: 4px;
    }}

    /* 卡片系统 */
    .cards-container {{
        z-index: 1;
        flex: 1;
        display: flex;
        align-items: center;
    }}

    .cards-2-col {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 32px;
        width: 100%;
    }}

    .cards-3-col {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 24px;
        width: 100%;
    }}

    .feature-card {{
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 36px;
        display: flex;
        flex-direction: column;
        gap: 16px;
    }}

    .feature-card.large {{
        padding: 48px;
    }}

    .feature-number {{
        font-size: 48px;
        font-weight: 800;
        color: var(--accent);
        line-height: 1;
    }}

    .feature-text {{
        font-size: 22px;
        color: var(--text-secondary);
        line-height: 1.5;
    }}

    .feature-card.large .feature-text {{
        font-size: 26px;
    }}

    /* 列表 */
    .bullet-list {{
        list-style: none;
        padding: 0;
    }}

    .bullet-list li {{
        position: relative;
        padding-left: 36px;
        font-size: 22px;
        line-height: 1.6;
        color: var(--text-secondary);
        margin-bottom: 16px;
    }}

    .bullet-list li::before {{
        content: '';
        position: absolute;
        left: 0;
        top: 10px;
        width: 10px;
        height: 10px;
        background: var(--accent);
        border-radius: 50%;
    }}

    .bullet-list.large li {{
        font-size: 26px;
        padding-left: 44px;
        margin-bottom: 20px;
    }}

    .bullet-list.large li::before {{
        width: 14px;
        height: 14px;
        top: 12px;
    }}

    /* 内容区域 */
    .content-area {{
        z-index: 1;
        flex: 1;
        display: flex;
        align-items: center;
    }}

    .body-text {{
        font-size: 22px;
        line-height: 1.6;
        color: var(--text-secondary);
        margin-bottom: 20px;
    }}

    /* 分屏布局 */
    .split-layout {{
        z-index: 1;
        flex: 1;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 60px;
        align-items: center;
    }}

    .split-image {{
        height: 100%;
        max-height: 700px;
    }}

    .image-frame {{
        width: 100%;
        height: 100%;
        background: var(--bg-card);
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid var(--border);
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .image-frame img {{
        width: 100%;
        height: 100%;
        object-fit: contain;
        max-width: 100%;
        max-height: 100%;
    }}

    .split-content {{
        display: flex;
        flex-direction: column;
    }}

    /* 代码窗口 */
    .code-window {{
        z-index: 1;
        flex: 1;
        background: var(--bg-code);
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid var(--border);
        display: flex;
        flex-direction: column;
    }}

    .code-header {{
        background: var(--bg-card);
        padding: 16px 24px;
        display: flex;
        align-items: center;
        gap: 12px;
        border-bottom: 1px solid var(--border);
    }}

    .code-dots {{
        display: flex;
        gap: 8px;
    }}

    .code-dots span {{
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }}

    .code-dots span:nth-child(1) {{ background: #ff5f57; }}
    .code-dots span:nth-child(2) {{ background: #ffbd2e; }}
    .code-dots span:nth-child(3) {{ background: #27ca40; }}

    .code-lang {{
        font-size: 13px;
        color: var(--text-muted);
        font-weight: 500;
        margin-left: 12px;
        text-transform: uppercase;
    }}

    .code-content {{
        flex: 1;
        padding: 32px;
        overflow: auto;
    }}

    .code-content pre {{
        margin: 0;
        font-family: {fonts['mono']};
        font-size: 17px;
        line-height: 1.6;
        color: var(--text-primary);
    }}

    .code-content code {{
        font-family: inherit;
    }}

    /* 特殊页面 */
    .topic-cover h1 {{
        font-size: 64px;
    }}

    .end-slide h1 {{
        font-size: 80px;
    }}
</style>
"""
