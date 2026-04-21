"""
配置常量：主题、默认路径、布局注册
"""

from typing import Dict, Any

# PPTX 分辨率 (16:9)
PPTX_WIDTH = 1280
PPTX_HEIGHT = 720

# 默认最大页面数
DEFAULT_MAX_SLIDES = 15

# 主题配色方案 - Linear/Vercel 现代风格
THEMES: Dict[str, Dict[str, Any]] = {
    "linear": {
        "name": "Linear",
        "bg_dark": "#0A0A0A",
        "bg_card": "#111111",
        "bg_code": "#0D0D0D",
        "bg_elevated": "#161616",
        "text_primary": "#FFFFFF",
        "text_secondary": "#A0A0A0",
        "text_muted": "#666666",
        "accent": "#5E6AD2",
        "accent_rgb": (94, 106, 210),
        "accent_gradient": "linear-gradient(135deg, #5E6AD2 0%, #8B5CF6 100%)",
        "accent_secondary": "#8B5CF6",
        "border": "#222222",
        "border_hover": "#333333",
        "success": "#22C55E",
        "warning": "#F59E0B",
        "error": "#EF4444",
    },
    "vercel": {
        "name": "Vercel",
        "bg_dark": "#000000",
        "bg_card": "#111111",
        "bg_code": "#0A0A0A",
        "bg_elevated": "#171717",
        "text_primary": "#FFFFFF",
        "text_secondary": "#888888",
        "text_muted": "#555555",
        "accent": "#FFFFFF",
        "accent_rgb": (255, 255, 255),
        "accent_gradient": "linear-gradient(135deg, #FFFFFF 0%, #888888 100%)",
        "accent_secondary": "#333333",
        "border": "#333333",
        "border_hover": "#444444",
        "success": "#0070F3",
        "warning": "#F5A623",
        "error": "#FF0000",
    },
    "claude": {
        "name": "Claude",
        "bg_dark": "#1a1a2e",
        "bg_card": "#252542",
        "bg_code": "#16162a",
        "bg_elevated": "#2a2a50",
        "text_primary": "#ffffff",
        "text_secondary": "#b8b8d1",
        "text_muted": "#6b6b8a",
        "accent": "#FF6B35",
        "accent_rgb": (255, 107, 53),
        "accent_gradient": "linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%)",
        "accent_secondary": "#FF8C42",
        "border": "#3a3a5c",
        "border_hover": "#4a4a6c",
        "success": "#22C55E",
        "warning": "#F59E0B",
        "error": "#EF4444",
    },
    "indigo": {
        "name": "Indigo",
        "bg_dark": "#0F172A",
        "bg_card": "#1E293B",
        "bg_code": "#0f172a",
        "bg_elevated": "#334155",
        "text_primary": "#F8FAFC",
        "text_secondary": "#94A3B8",
        "text_muted": "#64748B",
        "accent": "#6366F1",
        "accent_rgb": (99, 102, 241),
        "accent_gradient": "linear-gradient(135deg, #6366F1 0%, #A855F7 100%)",
        "accent_secondary": "#A855F7",
        "border": "#334155",
        "border_hover": "#475569",
        "success": "#10B981",
        "warning": "#F59E0B",
        "error": "#EF4444",
    },
    "emerald": {
        "name": "Emerald",
        "bg_dark": "#022C22",
        "bg_card": "#064E3B",
        "bg_code": "#011f17",
        "bg_elevated": "#065F46",
        "text_primary": "#ECFDF5",
        "text_secondary": "#6EE7B7",
        "text_muted": "#34D399",
        "accent": "#10B981",
        "accent_rgb": (16, 185, 129),
        "accent_gradient": "linear-gradient(135deg, #10B981 0%, #34D399 100%)",
        "accent_secondary": "#059669",
        "border": "#065F46",
        "border_hover": "#10B981",
        "success": "#22C55E",
        "warning": "#F59E0B",
        "error": "#EF4444",
    },
}

# 布局类型
LAYOUT_TYPES = [
    "title",           # 标题页
    "agenda",          # 目录页
    "topic_cover",     # 主题封面
    "topic_overview",  # 主题概览
    "topic_detail",    # 主题详情
    "split_left",      # 左图右文
    "split_right",     # 右图左文
    "image_top",       # 上图下文
    "image_full",      # 全屏图+文字叠加
    "cards_2x2",       # 2x2卡片
    "cards_3",         # 3列卡片
    "code",            # 代码展示
    "timeline",        # 时间轴
    "comparison",      # 对比布局
    "quote",           # 引用/金句
    "end",             # 结束页
]

# 内容块类型优先级（用于页面分配）
CONTENT_PRIORITY = {
    "heading": 10,      # 标题最重要
    "paragraph": 5,     # 段落
    "bullet_list": 7,   # 列表
    "code_block": 6,    # 代码
    "image": 8,         # 图片
    "table": 4,         # 表格
}
