"""几何 scene JSON -> 单文件交互式 HTML（Three.js + CSS2D 中文标签）。

用法:
    python build_html.py <scene.json> <out.html> [--offline]

--offline: 将 Three.js 三件套内联进 HTML（体积约 +630KB），无网环境可打开。
默认走 unpkg CDN。
"""

import json
import os
import sys

TEMPLATE_PATH = __file__.replace("build_html.py", "template_3d.html")
VENDOR_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "vendor")

CDN_SCRIPTS = [
    "https://unpkg.com/three@0.128.0/build/three.min.js",
    "https://unpkg.com/three@0.128.0/examples/js/controls/OrbitControls.js",
    "https://unpkg.com/three@0.128.0/examples/js/renderers/CSS2DRenderer.js",
]
LOCAL_SCRIPTS = ["three.min.js", "OrbitControls.js", "CSS2DRenderer.js"]


def build(scene_path, out_path, offline=False):
    with open(scene_path, "r", encoding="utf-8") as f:
        scene = json.load(f)
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        tpl = f.read()
    data = json.dumps(scene, ensure_ascii=False)
    html = tpl.replace("/*__DATA__*/", data).replace("__TITLE__", scene.get("title", "立体几何解题演示"))

    if offline:
        for cdn, local in zip(CDN_SCRIPTS, LOCAL_SCRIPTS):
            with open(os.path.join(VENDOR_DIR, local), "r", encoding="utf-8") as f:
                js = f.read()
            html = html.replace(
                '<script src="%s"></script>' % cdn,
                "<script>\n%s\n</script>" % js,
            )
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("html written:", out_path, "(offline)" if offline else "")


def main():
    args = [a for a in sys.argv[1:] if a != "--offline"]
    offline = "--offline" in sys.argv
    if len(args) < 2:
        print("usage: python build_html.py <scene.json> <out.html> [--offline]", file=sys.stderr)
        sys.exit(1)
    build(args[0], args[1], offline=offline)


if __name__ == "__main__":
    main()
