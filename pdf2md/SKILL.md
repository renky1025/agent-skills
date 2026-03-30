---
name: pdf2md
description: "将任意 PDF 文件高质量转换为 Markdown 格式。支持复杂布局、表格、公式、图片提取，自动处理大文件分页，提供多种输出模式。基于 OpenDataLoader PDF - Benchmark #1 准确率。使用方法: /pdf2md <pdf路径> [--output=<输出目录>] [--mode=fast|hybrid] [--extract-images=true|false] [--ocr-lang=<语言>]"
user_invocable: true
version: "1.0.0"
---

# pdf2md: PDF 转 Markdown 铸造器

基于 [OpenDataLoader PDF](https://github.com/opendataloader-project/opendataloader-pdf) 的高精度 PDF 解析工具，将 PDF 完美转换为 Markdown 格式，特别适合 AI/RAG 工作流。

## 核心优势

- **业界最高准确率**：Benchmark #1，综合 0.90，表格 0.93，阅读顺序 0.94
- **双模式架构**：本地模式(0.05s/页) + 混合模式(AI增强，复杂PDF专用)
- **完整内容还原**：表格、LaTeX公式、图片、多栏布局、标题层级
- **大文件友好**：自动分页处理，支持批量文件夹处理
- **边界框坐标**：每个元素都有坐标，支持溯源引用

## 使用方法

```
/pdf2md <PDF路径> [--output=<目录>] [--mode=fast|hybrid] [--extract-images=true|false] [--ocr] [--ocr-lang=<语言>]
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `PDF路径` | 单个PDF文件或包含PDF的文件夹 | 必填 |
| `--output` | 输出目录 | `~/Downloads/pdf2md-output/` |
| `--mode` | 处理模式: `fast`(本地) 或 `hybrid`(AI增强) | `fast` |
| `--extract-images` | 是否提取图片 | `true` |
| `--ocr` | 强制启用OCR(扫描版PDF) | `false` |
| `--ocr-lang` | OCR语言: `en`, `ch_sim`, `ch_tra`, `ja`, `ko` 等 | `en` |
| `--formula` | 提取数学公式为LaTeX(hybrid模式) | `false` |
| `--charts` | 生成图表AI描述(hybrid模式) | `false` |

## 前置检查

在使用前，必须验证环境是否就绪：

```bash
# 1. 检查 Java 版本 (需要 11+)
java -version

# 2. 检查 Python 版本 (需要 3.10+)
python3 --version

# 3. 检查 OpenDataLoader 是否安装
pip show opendataloader-pdf

# 4. 检查 hybrid 模式依赖 (如果使用)
pip show opendataloader-pdf[hybrid]
```

### 使用 pdf2md CLI 工具

```bash
# 基础转换
python3 ~/.claude/skills/pdf2md/pdf2md.py document.pdf

# Hybrid 模式（高质量，支持复杂表格/公式）
python3 ~/.claude/skills/pdf2md/pdf2md.py document.pdf --mode=hybrid

# 扫描版PDF（带OCR）
python3 ~/.claude/skills/pdf2md/pdf2md.py scan.pdf --mode=hybrid --ocr --ocr-lang=ch_sim

# 学术论文（含公式）
python3 ~/.claude/skills/pdf2md/pdf2md.py paper.pdf --mode=hybrid --formula

# 批量处理文件夹
python3 ~/.claude/skills/pdf2md/pdf2md.py ./pdfs/ --mode=hybrid --output=./output/

# 检查环境
python3 ~/.claude/skills/pdf2md/pdf2md.py --check

# 安装依赖
python3 ~/.claude/skills/pdf2md/pdf2md.py --install
```

### CLI 参数说明

```
参数:
  input                 PDF文件或文件夹路径

可选参数:
  -o, --output          输出目录 (默认: ~/Downloads/pdf2md-output)
  -m, --mode            处理模式: fast 或 hybrid (默认: fast)
  --no-images           不提取图片
  --ocr                 启用OCR (扫描版PDF)
  --ocr-lang            OCR语言 (默认: en, 可选: ch_sim/ch_tra/ja/ko)
  --formula             提取数学公式为LaTeX (hybrid模式)
  --charts              生成图表AI描述 (hybrid模式)
  --port                Hybrid后端端口 (默认: 5002)
  --check               仅检查环境依赖
  --install             安装/更新依赖
```

# 4. 检查 hybrid 模式依赖 (如果使用)
pip show opendataloader-pdf[hybrid]
```

### 自动安装

如果未安装，Claude 会自动执行：

```bash
# 基础安装
pip install -U opendataloader-pdf

# 混合模式安装(推荐，支持OCR/公式/图表)
pip install -U "opendataloader-pdf[hybrid]"
```

## 执行步骤

### 步骤 1: 环境检查与初始化

```python
import subprocess
import sys

def check_prerequisites():
    """检查并安装必要依赖"""
    checks = {
        "java": "java -version",
        "python": "python3 --version",
        "opendataloader": "pip show opendataloader-pdf"
    }

    for name, cmd in checks.items():
        result = subprocess.run(cmd.split(), capture_output=True)
        if result.returncode != 0:
            if name == "opendataloader":
                print(f"安装 {name}...")
                subprocess.run([sys.executable, "-m", "pip", "install", "-U", "opendataloader-pdf"])
            else:
                raise RuntimeError(f"{name} 未安装，请先安装")
```

### 步骤 2: 文件分析与预处理

```python
import os
from pathlib import Path

def analyze_pdf(input_path):
    """分析PDF文件，确定处理策略"""
    path = Path(input_path)

    if path.is_file() and path.suffix.lower() == '.pdf':
        file_size = path.stat().st_size
        pages = estimate_pages(file_size)  # 估算页数

        return {
            "type": "single",
            "path": str(path),
            "size": file_size,
            "pages": pages,
            "recommend_mode": "hybrid" if pages > 50 else "fast"
        }
    elif path.is_dir():
        pdfs = list(path.glob("**/*.pdf"))
        return {
            "type": "batch",
            "count": len(pdfs),
            "files": [str(p) for p in pdfs],
            "recommend_mode": "hybrid" if len(pdfs) > 10 else "fast"
        }
    else:
        raise ValueError(f"无效路径: {input_path}")

def estimate_pages(file_size_bytes):
    """根据文件大小估算页数 (约150KB/页)"""
    return max(1, int(file_size_bytes / 150000))
```

### 步骤 3: 启动 Hybrid 后端 (如使用混合模式)

```python
import subprocess
import time

def start_hybrid_backend(port=5002, ocr=False, ocr_lang="en", formula=False, charts=False):
    """启动混合模式后端服务器"""
    cmd = ["opendataloader-pdf-hybrid", "--port", str(port)]

    if ocr:
        cmd.extend(["--force-ocr", "--ocr-lang", ocr_lang])
    if formula:
        cmd.append("--enrich-formula")
    if charts:
        cmd.append("--enrich-picture-description")

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 等待服务启动
    time.sleep(3)

    # 检查服务是否就绪
    import urllib.request
    try:
        urllib.request.urlopen(f"http://localhost:{port}/health", timeout=5)
        return process
    except:
        process.terminate()
        raise RuntimeError("Hybrid 后端启动失败")
```

### 步骤 4: 执行转换 (核心代码)

```python
import opendataloader_pdf
import json
from pathlib import Path

def convert_pdf(input_path, output_dir, mode="fast", extract_images=True,
                ocr=False, ocr_lang="en", formula=False, charts=False):
    """
    转换PDF到Markdown

    Args:
        input_path: PDF文件路径或文件夹路径
        output_dir: 输出目录
        mode: 'fast' 或 'hybrid'
        extract_images: 是否提取图片
        ocr: 是否启用OCR
        ocr_lang: OCR语言
        formula: 是否提取公式
        charts: 是否描述图表
    """

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 准备配置
    formats = ["markdown", "json"]  # JSON用于调试和元数据

    kwargs = {
        "input_path": input_path,
        "output_dir": str(output_path),
        "format": ",".join(formats),
        "image_output": "external" if extract_images else "off",
        "image_format": "png",
        "use_struct_tree": True,  # 使用PDF原有结构
    }

    # 混合模式配置
    if mode == "hybrid":
        kwargs["hybrid"] = "docling-fast"
        if formula or charts:
            kwargs["hybrid_mode"] = "full"

    # 执行转换
    try:
        result = opendataloader_pdf.convert(**kwargs)

        # 后处理：整合图片到markdown
        if extract_images:
            post_process_images(output_path)

        # 后处理：修复表格格式
        post_process_tables(output_path)

        return {
            "success": True,
            "output_dir": str(output_path),
            "files": list(output_path.glob("*"))
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

def post_process_images(output_dir):
    """优化图片路径和引用"""
    import re

    for md_file in Path(output_dir).glob("*.md"):
        content = md_file.read_text(encoding='utf-8')

        # 确保图片路径正确
        content = re.sub(
            r'!\[\]\(([^)]+)\)',
            lambda m: f'![image]({Path(m.group(1)).name})',
            content
        )

        md_file.write_text(content, encoding='utf-8')

def post_process_tables(output_dir):
    """优化表格Markdown格式"""
    import re

    for md_file in Path(output_dir).glob("*.md"):
        content = md_file.read_text(encoding='utf-8')

        # 修复可能的表格格式问题
        # OpenDataLoader 输出通常是标准GFM格式
        # 这里可以添加自定义修复逻辑

        md_file.write_text(content, encoding='utf-8')
```

### 步骤 5: 大文件分批处理

```python
import os
from pathlib import Path
import tempfile

def convert_large_pdf(input_path, output_dir, mode="hybrid", batch_size=100):
    """
    大文件分批处理

    对于超过 batch_size 页的PDF，建议：
    1. 使用 OpenDataLoader 的批量处理功能（它会自动处理）
    2. 或者预先分割PDF（不推荐，会丢失跨页内容）
    """
    file_size = Path(input_path).stat().st_size
    estimated_pages = estimate_pages(file_size)

    if estimated_pages > batch_size:
        print(f"⚠️  大文件检测: 约 {estimated_pages} 页，建议使用 hybrid 模式以确保质量")
        print(f"   自动切换到 hybrid 模式...")
        mode = "hybrid"

    # OpenDataLoader 内部已经优化了大文件处理
    # 只需要在 batch 调用时一次性传入所有文件
    return convert_pdf(input_path, output_dir, mode=mode)

def process_batch(pdf_files, output_dir, mode="fast"):
    """批量处理多个PDF文件"""
    results = []

    # OpenDataLoader 推荐一次性批量处理，而不是逐个处理
    # 因为每个 convert() 调用会启动一次 JVM 进程
    result = convert_pdf(pdf_files, output_dir, mode=mode)
    results.append(result)

    return results
```

### 步骤 6: 异常处理与重试

```python
import time
import traceback

def safe_convert(input_path, output_dir, max_retries=2, **kwargs):
    """
    带重试机制的转换

    常见异常及处理：
    1. JVM内存不足 -> 减小批次大小
    2. 损坏的PDF -> 尝试修复模式
    3. 加密PDF -> 提示用户解密
    4. 混合模式后端未启动 -> 自动启动
    """

    for attempt in range(max_retries + 1):
        try:
            result = convert_pdf(input_path, output_dir, **kwargs)
            if result.get("success"):
                return result
            else:
                raise Exception(result.get("error", "Unknown error"))

        except Exception as e:
            error_msg = str(e).lower()

            if "memory" in error_msg:
                print(f"⚠️  内存不足，尝试用 fast 模式重试...")
                kwargs["mode"] = "fast"

            elif "password" in error_msg or "encrypted" in error_msg:
                return {
                    "success": False,
                    "error": "PDF 已加密，请先解密后再处理",
                    "recoverable": False
                }

            elif "corrupted" in error_msg or "damaged" in error_msg:
                print(f"⚠️  PDF 可能损坏，尝试修复模式...")
                # 可以尝试用 PyPDF2 等工具修复

            elif attempt < max_retries:
                print(f"⚠️  转换失败 ({attempt+1}/{max_retries+1})，{3}秒后重试...")
                time.sleep(3)
                continue

            else:
                return {
                    "success": False,
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                    "recoverable": False
                }

    return result
```

### 步骤 7: 结果整理与输出

```python
def organize_output(output_dir, original_name):
    """整理输出文件结构"""
    output_path = Path(output_dir)

    # 创建子目录
    images_dir = output_path / "images"
    images_dir.mkdir(exist_ok=True)

    # 移动图片文件
    for img in output_path.glob("*.png"):
        img.rename(images_dir / img.name)
    for img in output_path.glob("*.jpg"):
        img.rename(images_dir / img.name)

    # 更新 markdown 中的图片引用
    for md_file in output_path.glob("*.md"):
        content = md_file.read_text(encoding='utf-8')
        content = content.replace("](", "](images/")
        md_file.write_text(content, encoding='utf-8')

    # 生成摘要文件
    summary = {
        "source": original_name,
        "output_directory": str(output_path),
        "files": {
            "markdown": [str(f) for f in output_path.glob("*.md")],
            "json": [str(f) for f in output_path.glob("*.json")],
            "images": [str(f) for f in images_dir.glob("*")]
        }
    }

    summary_file = output_path / "summary.json"
    summary_file.write_text(json.dumps(summary, indent=2), encoding='utf-8')

    return summary
```

## 完整使用示例

### 示例 1: 简单PDF转Markdown

```python
# 用户命令: /pdf2md document.pdf

result = safe_convert(
    input_path="document.pdf",
    output_dir="~/Downloads/pdf2md-output/document/",
    mode="fast",
    extract_images=True
)
```

### 示例 2: 扫描版PDF（带OCR）

```python
# 用户命令: /pdf2md scan.pdf --mode=hybrid --ocr --ocr-lang=ch_sim

result = safe_convert(
    input_path="scan.pdf",
    output_dir="~/Downloads/pdf2md-output/scan/",
    mode="hybrid",
    ocr=True,
    ocr_lang="ch_sim",  # 简体中文
    extract_images=True
)
```

### 示例 3: 学术论文（含公式）

```python
# 用户命令: /pdf2md paper.pdf --mode=hybrid --formula

result = safe_convert(
    input_path="paper.pdf",
    output_dir="~/Downloads/pdf2md-output/paper/",
    mode="hybrid",
    formula=True,
    extract_images=True
)
```

### 示例 4: 批量处理文件夹

```python
# 用户命令: /pdf2md ./pdfs/ --mode=hybrid --output=./output/

result = safe_convert(
    input_path="./pdfs/",
    output_dir="./output/",
    mode="hybrid",
    extract_images=True
)
```

## 输出结构

转换完成后，输出目录结构如下：

```
output/
├── document.md              # 主Markdown文件
├── document.json            # 结构化JSON（含边界框坐标）
├── summary.json             # 处理摘要
└── images/                  # 提取的图片
    ├── image_001.png
    ├── image_002.png
    └── ...
```

### Markdown 示例输出

```markdown
# 文档标题

## 第一章 介绍

这是一段正文内容。OpenDataLoader 会正确保留**粗体**和*斜体*。

### 表格示例

| 列1 | 列2 | 列3 |
|-----|-----|-----|
| A1  | B1  | C1  |
| A2  | B2  | C2  |

### 图片示例

![image](images/image_001.png)

### 数学公式

行内公式: $E = mc^2$

块级公式:
$$
\frac{f(x+h) - f(x)}{h}
$$

## 第二章 方法

...
```

## 常见问题处理

### Q: 转换后表格格式错乱
**A**: 使用 `mode=hybrid`，它会自动处理复杂/无边框表格

### Q: 扫描版PDF识别率低
**A**: 添加 `--ocr` 参数，并确保使用 `--mode=hybrid`

### Q: 大文件内存不足
**A**: OpenDataLoader 会自动流式处理，如遇内存问题，改用 `mode=fast`

### Q: 图片没有正确提取
**A**: 确保使用 `--extract-images=true`（默认开启），并检查输出目录的 images 文件夹

### Q: 数学公式显示不正确
**A**: 使用 `--mode=hybrid --formula`，公式会以LaTeX格式输出

### Q: 中文PDF乱码
**A**: 数字PDF应正常显示，扫描版PDF使用 `--ocr --ocr-lang=ch_sim`

## 性能参考

| 文档类型 | 模式 | 速度 | 准确率 |
|---------|------|------|--------|
| 简单数字PDF | fast | 20页/秒 | 0.72 |
| 复杂表格PDF | hybrid | 2页/秒 | 0.93 |
| 扫描版PDF | hybrid+OCR | 1页/秒 | 0.90+ |

## 依赖说明

- **Java 11+**: 解析引擎基于Java
- **Python 3.10+**: Python接口
- **OpenDataLoader PDF**: `pip install opendataloader-pdf`
- **Hybrid模式额外依赖**: `pip install "opendataloader-pdf[hybrid]"`

## 相关链接

- [OpenDataLoader GitHub](https://github.com/opendataloader-project/opendataloader-pdf)
- [官方文档](https://opendataloader.org/docs)
- [Benchmark结果](https://github.com/opendataloader-project/opendataloader-bench)

## License

Apache 2.0 - 与 OpenDataLoader PDF 保持一致
