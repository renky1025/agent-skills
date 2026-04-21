"""
Playwright 截图模块
"""

import os
from typing import List


def capture_slides(html_path: str, output_dir: str, slide_count: int) -> List[str]:
    """
    使用 Playwright 截图所有幻灯片
    返回截图文件路径列表
    """
    try:
        from playwright.sync_api import sync_playwright

        image_paths = []

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={'width': 1920, 'height': 1080})

            # 加载 HTML
            page.goto(f'file://{html_path}', wait_until='networkidle')
            page.wait_for_timeout(1000)

            # 获取所有幻灯片
            slides = page.query_selector_all('.slide')

            for i, slide in enumerate(slides[:slide_count], 1):
                slide.evaluate('el => el.scrollIntoView({ block: "start" })')
                page.wait_for_timeout(200)

                output_path = os.path.join(output_dir, f"slide_{i:03d}.png")
                slide.screenshot(path=output_path)
                image_paths.append(output_path)

            browser.close()

        return image_paths

    except Exception as e:
        print(f"Playwright error: {e}")
        return []
