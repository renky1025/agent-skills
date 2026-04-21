"""
命令行入口
"""

import argparse
import os
import sys

# 确保 videofy_lib 在路径中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from videofy_lib.parser.markdown import MarkdownParser
from videofy_lib.parser import PagePlanner
from videofy_lib.generator.pptx_generator import PPTXGenerator
from videofy_lib.utils.file import ensure_dir, find_images
from videofy_lib.config import THEMES


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown to PowerPoint Presentation'
    )
    parser.add_argument('input_dir', help='Input directory containing .md files')
    parser.add_argument('--theme', '-t', default='linear',
                       choices=list(THEMES.keys()),
                       help='Theme name')
    parser.add_argument('--max-slides', '-n', type=int, default=15,
                       help='Maximum number of slides (default: 15)')
    parser.add_argument('--output', '-o', help='Output file path (.pptx)')

    args = parser.parse_args()

    input_dir = os.path.abspath(args.input_dir)

    if not os.path.exists(input_dir):
        print(f"❌ Directory not found: {input_dir}")
        sys.exit(1)

    # 查找 Markdown 文件
    md_files = []
    for root, _, files in os.walk(input_dir):
        for f in files:
            if f.endswith('.md'):
                md_files.append(os.path.join(root, f))

    if not md_files:
        print(f"❌ No Markdown files found in {input_dir}")
        sys.exit(1)

    md_path = md_files[0]
    print(f"📝 {os.path.basename(md_path)}")

    # 查找图片目录
    images_dir = None
    for check_dir in [input_dir, os.path.dirname(input_dir)]:
        for subdir in ['images', 'assets', 'img']:
            img_path = os.path.join(check_dir, subdir)
            if os.path.exists(img_path):
                images_dir = img_path
                break
        if images_dir:
            break

    if images_dir:
        print(f"🖼️  {os.path.basename(images_dir)}")

    # 确定输出文件路径
    if args.output:
        output_path = os.path.abspath(args.output)
        # 确保目录存在
        ensure_dir(os.path.dirname(output_path))
    else:
        # 默认使用输入目录名
        dir_name = os.path.basename(input_dir)
        output_path = os.path.join(input_dir, f"{dir_name}.pptx")

    # 解析 Markdown
    print("📖 Parsing...")
    parser = MarkdownParser(md_path, images_dir)
    doc = parser.parse()

    # 规划页面
    print(f"📊 Planning (max {args.max_slides} slides)...")
    planner = PagePlanner(max_slides=args.max_slides)
    slides = planner.plan_slides(doc)

    print(f"🎯 {len(slides)} slides generated")
    for item in doc.agenda:
        print(f"   {item.index}. {item.title} ({item.content_pages} pages)")

    # 生成 PPTX
    print(f"🎨 Theme: {THEMES[args.theme]['name']}")
    print("📊 Generating PowerPoint...")

    pptx_gen = PPTXGenerator(theme=args.theme)
    pptx_gen.save(slides, output_path)

    print(f"\n✨ Done!")
    print(f"📊 PowerPoint saved to: {output_path}")


if __name__ == '__main__':
    main()
