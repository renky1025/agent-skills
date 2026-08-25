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
python3 pdf2md/pdf2md.py document.pdf

# Hybrid 模式（高质量，支持复杂表格/公式）
python3 pdf2md/pdf2md.py document.pdf --mode=hybrid

# 扫描版PDF（带OCR）
python3 pdf2md/pdf2md.py scan.pdf --mode=hybrid --ocr --ocr-lang=ch_sim

# 学术论文（含公式）
python3 pdf2md/pdf2md.py paper.pdf --mode=hybrid --formula

# 批量处理文件夹
python3 pdf2md/pdf2md.py ./pdfs/ --mode=hybrid --output=./output/

# 检查环境
python3 pdf2md/pdf2md.py --check

# 安装依赖
python3 pdf2md/pdf2md.py --install
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
### 自动安装

如果未安装，助手会自动执行：

```bash
# 基础安装
pip install -U opendataloader-pdf

# 混合模式安装(推荐，支持OCR/公式/图表)
pip install -U "opendataloader-pdf[hybrid]"
```

## 实现说明

完整实现见 `pdf2md/pdf2md.py`，上文「使用 pdf2md CLI 工具」一节已覆盖全部能力：环境检查、单文件/批量转换、混合模式后端、OCR、公式、图片与表格后处理、失败重试。

**本技能不要求手动复现下方历史步骤说明**——直接调用 CLI 即可。如确需了解内部逻辑，以 `pdf2md.py` 源码为准（该脚本本身已包含上述全部步骤的实现，文档与源码不再重复维护，避免漂移）。

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

## 备选方案

- **原生 PDF 读取**：对于简单的数字PDF文档，当前模型可直接读取 PDF 内容并输出 Markdown，无需安装 OpenDataLoader 工具链。适合快速处理少量简单文档。复杂表格、公式、扫描件仍需使用本技能的 hybrid 模式。

## License

Apache 2.0 - 与 OpenDataLoader PDF 保持一致
