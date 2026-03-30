#!/usr/bin/env python3
"""
pdf2md - 基于 OpenDataLoader PDF 的高精度 PDF 转 Markdown 工具
"""

import argparse
import json
import os
import subprocess
import sys
import time
import traceback
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Union


def check_prerequisites() -> Dict[str, bool]:
    """检查环境依赖"""
    checks = {}

    # 检查 Java
    try:
        result = subprocess.run(["java", "-version"], capture_output=True, text=True)
        checks["java"] = result.returncode == 0
        if checks["java"]:
            # 解析版本
            version_line = result.stderr.split('\n')[0] if result.stderr else result.stdout.split('\n')[0]
            print(f"✓ Java: {version_line}")
        else:
            print("✗ Java: 未安装 (需要 Java 11+)")
    except Exception as e:
        checks["java"] = False
        print(f"✗ Java: 检查失败 - {e}")

    # 检查 Python
    checks["python"] = sys.version_info >= (3, 10)
    print(f"✓ Python: {sys.version} {'(符合要求)' if checks['python'] else '(需要 3.10+)'}")

    # 检查 OpenDataLoader
    try:
        import opendataloader_pdf
        checks["opendataloader"] = True
        print(f"✓ OpenDataLoader PDF: 已安装")
    except ImportError:
        checks["opendataloader"] = False
        print("✗ OpenDataLoader PDF: 未安装")

    return checks


def install_opendataloader(hybrid: bool = False) -> bool:
    """安装 OpenDataLoader"""
    print("\n📦 正在安装 OpenDataLoader PDF...")

    try:
        if hybrid:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-U",
                "opendataloader-pdf[hybrid]"
            ], check=True)
        else:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-U",
                "opendataloader-pdf"
            ], check=True)

        print("✓ 安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 安装失败: {e}")
        return False


def start_hybrid_backend(port: int = 5002, ocr: bool = False,
                         ocr_lang: str = "en", formula: bool = False,
                         charts: bool = False) -> Optional[subprocess.Popen]:
    """启动混合模式后端"""
    print(f"\n🚀 启动 Hybrid 后端 (端口 {port})...")

    cmd = ["opendataloader-pdf-hybrid", "--port", str(port)]

    if ocr:
        cmd.extend(["--force-ocr", "--ocr-lang", ocr_lang])
        print(f"   OCR: 启用 (语言: {ocr_lang})")

    if formula:
        cmd.append("--enrich-formula")
        print("   公式提取: 启用")

    if charts:
        cmd.append("--enrich-picture-description")
        print("   图表描述: 启用")

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # 等待服务启动
        print("   等待服务就绪...", end="")
        for i in range(30):  # 最多等待30秒
            time.sleep(1)
            try:
                urllib.request.urlopen(
                    f"http://localhost:{port}/health",
                    timeout=2
                )
                print(" ✓")
                return process
            except:
                print(".", end="", flush=True)
                continue

        print(" ✗")
        process.terminate()
        return None

    except FileNotFoundError:
        print("✗ 未找到 opendataloader-pdf-hybrid 命令")
        print("   请运行: pip install 'opendataloader-pdf[hybrid]'")
        return None
    except Exception as e:
        print(f"✗ 启动失败: {e}")
        return None


def estimate_pages(file_size_bytes: int) -> int:
    """估算PDF页数"""
    return max(1, int(file_size_bytes / 150000))


def analyze_input(input_path: str) -> Dict:
    """分析输入路径"""
    path = Path(input_path).expanduser().resolve()

    if not path.exists():
        raise ValueError(f"路径不存在: {input_path}")

    if path.is_file() and path.suffix.lower() == '.pdf':
        file_size = path.stat().st_size
        pages = estimate_pages(file_size)

        return {
            "type": "single",
            "path": str(path),
            "name": path.stem,
            "size": file_size,
            "pages": pages,
            "size_mb": round(file_size / 1024 / 1024, 2)
        }
    elif path.is_dir():
        pdfs = list(path.glob("**/*.pdf"))
        return {
            "type": "batch",
            "path": str(path),
            "count": len(pdfs),
            "files": [str(p) for p in pdfs],
            "recommend_mode": "hybrid" if len(pdfs) > 10 else "fast"
        }
    else:
        raise ValueError(f"无效的PDF路径: {input_path}")


def post_process_images(output_dir: Path):
    """整理图片文件 - OpenDataLoader 默认输出到 {filename}_images/ 目录"""
    import re

    # 查找所有 OpenDataLoader 生成的图片目录 (*_images/)
    image_dirs = list(output_dir.glob("*_images"))

    if not image_dirs:
        return

    # 使用第一个找到的 images 目录
    source_images_dir = image_dirs[0]
    target_images_dir = output_dir / "images"

    # 移动图片到标准 images/ 目录
    moved = 0
    if source_images_dir.exists():
        target_images_dir.mkdir(exist_ok=True)
        for img in source_images_dir.glob("*"):
            if img.is_file():
                try:
                    target_path = target_images_dir / img.name
                    img.rename(target_path)
                    moved += 1
                except Exception as e:
                    print(f"   警告: 移动图片失败 {img.name}: {e}")

        # 删除空的源目录
        try:
            source_images_dir.rmdir()
        except:
            pass

    if moved > 0:
        print(f"   图片整理: {moved} 个文件 -> images/")

    # 更新 markdown 中的图片引用
    # OpenDataLoader 生成的路径是: {filename}_images/imageFile1.png
    # 需要改为: images/imageFile1.png
    for md_file in output_dir.glob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8')
            # 匹配 {filename}_images/xxx.png 改为 images/xxx.png
            content = re.sub(
                r'!\[([^\]]*)\]\([^)]*_images/([^)]+)\)',
                r'![\1](images/\2)',
                content
            )
            md_file.write_text(content, encoding='utf-8')
        except Exception as e:
            print(f"   警告: 更新图片引用失败: {e}")


def convert_pdf(input_path: Union[str, List[str]], output_dir: str,
                mode: str = "fast", extract_images: bool = True,
                hybrid_port: int = 5002) -> Dict:
    """
    执行PDF转换

    Args:
        input_path: PDF文件路径或路径列表
        output_dir: 输出目录
        mode: 'fast' 或 'hybrid'
        extract_images: 是否提取图片
        hybrid_port: hybrid后端端口
    """
    import opendataloader_pdf

    output_path = Path(output_dir).expanduser().resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    # 准备配置
    formats = ["markdown", "json"]

    kwargs = {
        "input_path": input_path,
        "output_dir": str(output_path),
        "format": ",".join(formats),
        "image_output": "external" if extract_images else "off",
        "image_format": "png",
        "use_struct_tree": True,
    }

    if mode == "hybrid":
        kwargs["hybrid"] = "docling-fast"

    # 执行转换
    start_time = time.time()
    result = opendataloader_pdf.convert(**kwargs)
    elapsed = time.time() - start_time

    # 后处理
    if extract_images:
        post_process_images(output_path)

    return {
        "success": True,
        "output_dir": str(output_path),
        "elapsed_time": round(elapsed, 2),
        "files": [f.name for f in output_path.glob("*")]
    }


def safe_convert(input_path: str, output_dir: str, mode: str = "fast",
                 extract_images: bool = True, hybrid_port: int = 5002,
                 max_retries: int = 2) -> Dict:
    """带重试机制的转换"""

    for attempt in range(max_retries + 1):
        try:
            result = convert_pdf(
                input_path, output_dir, mode=mode,
                extract_images=extract_images, hybrid_port=hybrid_port
            )
            return result

        except Exception as e:
            error_msg = str(e).lower()

            if "memory" in error_msg:
                print(f"⚠️  内存不足，尝试切换到 fast 模式...")
                mode = "fast"
            elif "password" in error_msg or "encrypted" in error_msg:
                return {
                    "success": False,
                    "error": "PDF 已加密，请先解密后再处理"
                }
            elif attempt < max_retries:
                print(f"⚠️  转换失败，{3}秒后重试...")
                time.sleep(3)
                continue
            else:
                return {
                    "success": False,
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }

    return {"success": False, "error": "达到最大重试次数"}


def generate_summary(output_dir: Path, source_info: Dict) -> Dict:
    """生成处理摘要"""
    summary = {
        "source": source_info,
        "output_directory": str(output_dir),
        "files": {}
    }

    # 分类输出文件
    summary["files"]["markdown"] = [f.name for f in output_dir.glob("*.md")]
    summary["files"]["json"] = [f.name for f in output_dir.glob("*.json")]

    images_dir = output_dir / "images"
    if images_dir.exists():
        summary["files"]["images"] = [f.name for f in images_dir.glob("*")]

    # 保存摘要
    summary_file = output_dir / "summary.json"
    summary_file.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )

    return summary


def main():
    parser = argparse.ArgumentParser(
        description="PDF 转 Markdown 工具 - 基于 OpenDataLoader PDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s document.pdf
  %(prog)s document.pdf --mode=hybrid --ocr --ocr-lang=ch_sim
  %(prog)s ./pdfs/ --output=./output/ --mode=hybrid
  %(prog)s --check          # 检查环境
  %(prog)s --install        # 安装依赖
        """
    )

    parser.add_argument("input", nargs="?", help="PDF文件或文件夹路径")
    parser.add_argument("-o", "--output", default="~/Downloads/pdf2md-output",
                       help="输出目录 (默认: ~/Downloads/pdf2md-output)")
    parser.add_argument("-m", "--mode", choices=["fast", "hybrid"],
                       default="fast", help="处理模式 (默认: fast)")
    parser.add_argument("--no-images", action="store_true",
                       help="不提取图片")
    parser.add_argument("--ocr", action="store_true",
                       help="启用OCR (扫描版PDF)")
    parser.add_argument("--ocr-lang", default="en",
                       help="OCR语言 (默认: en)")
    parser.add_argument("--formula", action="store_true",
                       help="提取数学公式为LaTeX (hybrid模式)")
    parser.add_argument("--charts", action="store_true",
                       help="生成图表AI描述 (hybrid模式)")
    parser.add_argument("--port", type=int, default=5002,
                       help="Hybrid后端端口 (默认: 5002)")
    parser.add_argument("--check", action="store_true",
                       help="仅检查环境依赖")
    parser.add_argument("--install", action="store_true",
                       help="安装/更新依赖")

    args = parser.parse_args()

    # 检查模式
    if args.check:
        print("🔍 检查环境依赖...\n")
        checks = check_prerequisites()
        if all(checks.values()):
            print("\n✓ 所有依赖已就绪")
            return 0
        else:
            print("\n✗ 部分依赖缺失")
            return 1

    # 安装模式
    if args.install:
        print("📦 安装依赖...\n")
        hybrid = args.mode == "hybrid" or args.ocr or args.formula or args.charts
        if install_opendataloader(hybrid=hybrid):
            return 0
        else:
            return 1

    # 常规转换模式需要 input
    if not args.input:
        parser.print_help()
        print("\n✗ 错误: 请提供PDF文件或文件夹路径，或使用 --check/--install")
        return 1

    # 常规转换模式
    print("🔍 检查环境...")
    checks = check_prerequisites()

    if not all(checks.values()):
        print("\n⚠️  部分依赖缺失，尝试自动安装...")
        hybrid = args.mode == "hybrid" or args.ocr or args.formula or args.charts
        if not install_opendataloader(hybrid=hybrid):
            print("✗ 安装失败，请手动安装后重试")
            return 1

    # 重新导入
    try:
        import opendataloader_pdf
    except ImportError:
        print("✗ 导入失败，请检查安装")
        return 1

    # 分析输入
    print(f"\n📄 分析输入...")
    try:
        source_info = analyze_input(args.input)
    except ValueError as e:
        print(f"✗ {e}")
        return 1

    if source_info["type"] == "single":
        print(f"   文件: {source_info['name']}.pdf")
        print(f"   大小: {source_info['size_mb']} MB")
        print(f"   预估页数: ~{source_info['pages']} 页")
    else:
        print(f"   批量处理: {source_info['count']} 个PDF文件")

    # 确定输出目录
    output_dir = Path(args.output).expanduser().resolve()
    if source_info["type"] == "single":
        output_dir = output_dir / source_info["name"]
    print(f"   输出目录: {output_dir}")

    # 确定模式
    mode = args.mode
    if source_info["type"] == "single" and source_info.get("pages", 0) > 100:
        if mode == "fast":
            print(f"\n💡 提示: 大文件检测，建议使用 --mode=hybrid 以获得更好质量")

    # 启动Hybrid后端（如需要）
    hybrid_process = None
    if mode == "hybrid" or args.ocr or args.formula or args.charts:
        hybrid_process = start_hybrid_backend(
            port=args.port,
            ocr=args.ocr,
            ocr_lang=args.ocr_lang,
            formula=args.formula,
            charts=args.charts
        )
        if not hybrid_process:
            print("✗ Hybrid 后端启动失败，切换到 fast 模式")
            mode = "fast"

    # 执行转换
    print(f"\n🔄 开始转换 (模式: {mode})...")
    try:
        result = safe_convert(
            input_path=source_info["path"] if source_info["type"] == "single" else source_info["files"],
            output_dir=str(output_dir),
            mode=mode,
            extract_images=not args.no_images,
            hybrid_port=args.port
        )

        if result.get("success"):
            print(f"✓ 转换完成! 耗时: {result.get('elapsed_time', 'N/A')}s")
            print(f"   输出目录: {result['output_dir']}")

            # 生成摘要
            summary = generate_summary(Path(result["output_dir"]), source_info)

            print(f"\n📁 输出文件:")
            for file_type, files in summary["files"].items():
                if files:
                    print(f"   [{file_type.upper()}]")
                    for f in files[:5]:  # 最多显示5个
                        print(f"      - {f}")
                    if len(files) > 5:
                        print(f"      ... 还有 {len(files) - 5} 个文件")

            print(f"\n💡 提示: 查看 summary.json 获取完整信息")
            return 0
        else:
            print(f"✗ 转换失败: {result.get('error', '未知错误')}")
            if "traceback" in result:
                print(f"\n详细错误:\n{result['traceback']}")
            return 1

    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        return 130
    finally:
        if hybrid_process:
            print("\n🛑 停止 Hybrid 后端...")
            hybrid_process.terminate()


if __name__ == "__main__":
    sys.exit(main())
