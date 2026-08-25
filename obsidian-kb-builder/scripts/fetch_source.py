#!/usr/bin/env python3
"""fetch_source.py — 把一个 URL 或本地文档规范化为 markdown，并保留图片到本地。

用法:
  python3 fetch_source.py --input <URL|文件路径> --vault <vault> [--subdir articles] [--date YYYY-MM-DD]

行为:
  1. 输入为 URL：经 Jina Reader (https://r.jina.ai/<url>) 取干净 markdown；尊重 http(s)_proxy 环境变量。
  2. 输入为本地文件：.md/.txt 直接读；.html/.htm 去除 script/style 后当 markdown；.pdf/.docx 用 pandoc 转换（需安装）。
  3. 扫描文中的图片 URL（markdown ![](...) 与 HTML <img src>），下载到 raw/assets/，并改写为本地相对路径 ../assets/<file>。
  4. 写出 raw/<subdir>/<date>-<slug>.md，打印结果路径与统计。

网络层统一走 curl（经代理可靠）；本机无 curl 时回退 urllib。
图片下载为 best-effort：失败则保留原 URL 并记录 warning，不中断。
"""
import argparse
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import subprocess
import shutil
import datetime

IMG_MARKDOWN = re.compile(r"!\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")
IMG_HTML = re.compile(r"<img\b[^>]*?src=[\"']([^\"']+)[\"'][^>]*?>", re.I)


def get_proxies():
    # 优先小写 https_proxy/http_proxy（用户显式约定的本地代理，如 127.0.0.1:7890），
    # 仅当小写未设置时回退大写。避免被运行时注入的大写 HTTPS_PROXY（沙箱代理）劫持。
    for k in ("https_proxy", "HTTPS_PROXY", "http_proxy", "HTTP_PROXY"):
        v = os.environ.get(k)
        if v:
            return {"http": v, "https": v}
    return {}


def curl_fetch(url, binary=False, timeout=60, retries=3):
    """经 curl 取数据（字节）。本机无 curl 时回退 urllib。返回 bytes。
    对代理的间歇性 TLS 抖动做有限重试（RETRY/502/SSL 错误通常可恢复）。"""
    proxies = get_proxies()
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            if shutil.which("curl"):
                cmd = ["curl", "-fsSL", "--max-time", str(timeout)]
                if proxies:
                    cmd += ["-x", proxies.get("https") or proxies.get("http")]
                cmd += [url]
                r = subprocess.run(cmd, capture_output=True)
                if r.returncode == 0 and r.stdout:
                    return r.stdout
                last_err = f"curl rc={r.returncode} ({r.stderr[:120].decode('utf-8','replace')})"
            else:
                # 回退：urllib
                opener = urllib.request.build_opener()
                if proxies:
                    opener = urllib.request.build_opener(urllib.request.ProxyHandler(proxies))
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with opener.open(req, timeout=timeout) as resp:
                    return resp.read()
        except Exception as e:  # 含 SSL/超时等瞬断
            last_err = str(e)
        if attempt < retries:
            time.sleep(1.5 * attempt)
    raise RuntimeError(last_err or "fetch failed")


def fetch_text(url, timeout=60, binary=False):
    data = curl_fetch(url, binary=binary, timeout=timeout)
    if binary:
        return data
    return data.decode("utf-8", errors="replace")


def is_url(s):
    return bool(re.match(r"^https?://", s, re.I))


def slugify(s):
    s = re.sub(r"[^A-Za-z0-9\u4e00-\u9fff_-]+", "-", s).strip("-")
    return s[:60] or "page"


def derive_slug_and_title(text, fallback):
    # 取第一行非空作为候选标题
    for line in text.splitlines():
        line = line.strip().lstrip("#").strip()
        if line:
            return slugify(line)
    return fallback


def fetch_url(url):
    # 优先 Jina Reader 拿干净 markdown
    try:
        md = fetch_text("https://r.jina.ai/" + url)
        if md and len(md) > 200:
            return md, url
    except Exception:
        pass
    # 回退：直接抓原始页
    return fetch_text(url), url


def download_image(url, assets_dir, page_base_url, warnings):
    """下载图片到 assets_dir，返回本地相对路径（相对 raw 子目录：../assets/xxx）。"""
    try:
        if url.startswith("//"):
            url = "https:" + url
        if url.startswith("/") and page_base_url:
            url = urllib.parse.urljoin(page_base_url, url)
        if not re.match(r"^https?://", url, re.I) or url.startswith("data:"):
            return None
        base = os.path.basename(urllib.parse.urlparse(url).path) or "img"
        base = re.sub(r"[^A-Za-z0-9._-]", "_", base)
        if len(base) > 60:
            base = base[:60]
        if "." not in base:
            base += ".png"
        name, ext = os.path.splitext(base)
        out = os.path.join(assets_dir, base)
        i = 1
        while os.path.exists(out):
            out = os.path.join(assets_dir, f"{name}_{i}{ext}")
            i += 1
        data = curl_fetch(url, binary=True)
        if not data:
            return None
        with open(out, "wb") as f:
            f.write(data)
        return "../assets/" + os.path.basename(out)
    except Exception as e:  # best-effort
        warnings.append(f"{url}: {e}")
        return None


def local_to_markdown(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".md", ".markdown", ".txt"):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read(), None
    if ext in (".html", ".htm"):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()
        html = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.I | re.S)
        html = re.sub(r"<style\b[^>]*>.*?</style>", "", html, flags=re.I | re.S)
        # 极简：去掉标签，保留文本与图片
        text = re.sub(r"<(?!img\b)[^>]+>", "", html)
        return text, None
    if ext in (".pdf", ".docx"):
        if not shutil.which("pandoc"):
            raise SystemExit("ERROR: 需要 pandoc 转换 PDF/DOCX。请安装 pandoc（brew install pandoc）后重试。")
        out = subprocess.check_output(["pandoc", path, "-t", "markdown"], timeout=120)
        return out.decode("utf-8", errors="replace"), None
    raise SystemExit(f"ERROR: 不支持的文件类型：{ext}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="URL 或本地文件路径")
    ap.add_argument("--vault", required=True, help="vault 根目录")
    ap.add_argument("--subdir", default="articles", help="raw 下的子目录（默认 articles）")
    ap.add_argument("--date", default=datetime.date.today().isoformat(), help="日期前缀 YYYY-MM-DD")
    args = ap.parse_args()

    vault = os.path.abspath(args.vault)
    warnings = []

    raw_subdir = os.path.join(vault, "raw", args.subdir)
    assets_dir = os.path.join(vault, "raw", "assets")
    os.makedirs(raw_subdir, exist_ok=True)
    os.makedirs(assets_dir, exist_ok=True)

    if is_url(args.input):
        text, page_base = fetch_url(args.input)
        src_label = args.input
    else:
        if not os.path.exists(args.input):
            raise SystemExit(f"ERROR: 文件不存在：{args.input}")
        text, _ = local_to_markdown(os.path.abspath(args.input))
        page_base = None
        src_label = os.path.basename(args.input)

    # 图片本地化
    img_count = 0
    for pat in (IMG_MARKDOWN, IMG_HTML):
        def repl(m, pat=pat):
            nonlocal img_count
            url = m.group(1)
            local = download_image(url, assets_dir, page_base, warnings)
            if local:
                img_count += 1
                return m.group(0).replace(url, local)
            return m.group(0)

        text = pat.sub(repl, text)

    # slug / 写出
    slug = derive_slug_and_title(text, slugify(src_label))
    out_name = f"{args.date}-{slug}.md"
    out_path = os.path.join(raw_subdir, out_name)
    i = 1
    while os.path.exists(out_path):
        out_path = os.path.join(raw_subdir, f"{args.date}-{slug}-{i}.md")
        i += 1
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

    print("input:", src_label)
    print("output:", out_path)
    print("images_localized:", img_count)
    print("warnings:", len(warnings))
    for w in warnings[:10]:
        print("  !", w)
    print("next: AI 读取该文件，按 .wiki-schema.md 写入 wiki/ 并在页面间加 [[链接]]。")


if __name__ == "__main__":
    main()
