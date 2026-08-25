"""函数 scene JSON -> 单文件交互式 HTML（Canvas2D + 参数滑块）。

用法:
    python build_html.py <scene.json> <out.html>
"""

import json
import sys

TEMPLATE_PATH = __file__.replace("build_html.py", "template_2d.html")


def build(scene_path, out_path):
    with open(scene_path, "r", encoding="utf-8") as f:
        scene = json.load(f)
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        tpl = f.read()
    data = json.dumps(scene, ensure_ascii=False)
    html = tpl.replace("/*__DATA__*/", data)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("html written:", out_path)


def main():
    if len(sys.argv) < 3:
        print("usage: python build_html.py <scene.json> <out.html>", file=sys.stderr)
        sys.exit(1)
    build(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
