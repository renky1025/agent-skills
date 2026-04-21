---
name: videofy
description: "将 Markdown 文档和图片转换为 PowerPoint (.pptx)。智能提取标题、根据内容量规划页面、多主题配色、创意布局设计。使用方法：/videofy <文件夹路径> [--theme=<主题>] [--max-slides=<数量>]"
user_invocable: true
version: "6.0.0"
---

# videofy v6.0: Markdown + Images → PowerPoint

智能将 Markdown 文档和图片转换为精美的 PowerPoint 演示文稿，支持目录驱动页面规划、多种现代主题、智能布局选择。

## 核心特性

### 1. 目录驱动页面规划
- **Agenda页**：通读全文后生成主题摘要，作为页面导航
- **严格对应**：每个内容页都服务于目录中的某个主题
- **智能分配**：根据内容量自动分配每个主题的页面数
- **页面控制**：支持 `--max-slides` 参数限制总页数

### 2. 模块化架构
```
videofy/
├── videofy.py           # 主入口（简洁）
├── videofy_lib/
│   ├── models.py        # 数据模型
│   ├── config.py        # 配置常量
│   ├── parser/          # Markdown解析
│   │   ├── markdown.py
│   │   ├── page_planner.py
│   │   └── image_matcher.py
│   ├── layout/          # 布局系统
│   │   ├── base.py
│   │   ├── registry.py
│   │   ├── selector.py
│   │   └── layouts/     # 具体布局实现
│   ├── generator/       # PPTX生成
│   │   └── pptx_generator.py
│   └── utils/           # 工具函数
```

### 3. 灵活布局系统

| 布局类型 | 用途 | 特点 |
|---------|------|------|
| `title` | 标题页 | Hero风格，大标题居中 |
| `agenda` | 目录页 | 网格展示所有主题 |
| `topic_cover` | 主题封面 | 章节起始页，带编号 |
| `topic_overview` | 主题概览 | 要点卡片网格 |
| `topic_detail` | 主题详情 | 列表式详细内容 |
| `split_left` | 左图右文 | 图片40%+文字60% |
| `split_right` | 右图左文 | 文字60%+图片40% |
| `code` | 代码页 | IDE风格展示 |
| `end` | 结束页 | 感谢页面 |

### 4. 现代主题设计

| 主题 | 风格 | 特点 |
|------|------|------|
| `linear` | Linear App | 深色背景+紫蓝渐变，极简书写 |
| `vercel` | Vercel | 纯黑+白色强调，科技感 |
| `claude` | Claude | 深蓝紫+橙色，经典 |
| `indigo` | Indigo | 靛蓝渐变，优雅 |
| `emerald` | Emerald | 深绿商务风 |

## 使用方法

```bash
/videofy <文件夹路径> [选项]
```

### 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `文件夹路径` | 包含 .md 文件和 images/ 的目录 | 必填 |
| `--theme, -t` | 主题配色 | `linear` |
| `--max-slides, -n` | 最大页面数 | `15` |
| `--output, -o` | 输出文件路径 | `<文件夹名>.pptx` |

### 示例

```bash
# 基础使用（自动主题）
/videofy ~/Documents/article

# 指定主题和页面数
/videofy ~/Documents/article --theme=linear --max-slides=10

# 指定输出文件
/videofy ~/Documents/article --output=~/Desktop/my_presentation.pptx
```

## 文件夹结构

```
输入文件夹/
├── *.md              # Markdown 文档
├── images/           # 图片文件夹（可选）
│   └── *.jpg/png
└── *.pptx            # 生成的演示文稿
```

## 页面规划策略

### 页面组成

```
总页数 = 标题页 + 目录页 + 内容页 + 结束页
       = 1 + 1 + N + 1
       = 3 + N
```

### 内容分配

1. **标题页**（1页）：文档标题+副标题
2. **目录页**（1页）：Agenda，列出所有主题
3. **内容页**（N页）：
   - 每个主题至少1页（封面页）
   - 剩余页面按内容量分配给各主题
   - 主题内部可包含：概览页、图片页、代码页、详情页
4. **结束页**（1页）：感谢观看

### 示例（max-slides=10）

| 页码 | 类型 | 内容 | 对应主题 |
|-----|------|------|---------|
| 1 | title | 文档标题 | - |
| 2 | agenda | 4个主题列表 | - |
| 3 | topic_cover | 主题1封面 | 主题1 |
| 4 | topic_overview | 主题1概览 | 主题1 |
| 5 | topic_cover | 主题2封面 | 主题2 |
| 6 | split_left | 主题2图文 | 主题2 |
| 7 | topic_cover | 主题3封面 | 主题3 |
| 8 | code | 主题3代码 | 主题3 |
| 9 | topic_cover | 主题4封面 | 主题4 |
| 10 | end | 感谢观看 | - |

## 依赖

- Python 3.8+
- python-pptx: `pip install python-pptx`

## 技术流程

```
Markdown
  ↓ 智能解析
章节结构 + 内容块
  ↓ 页面规划（目录驱动）
Agenda + Slides
  ↓ python-pptx 生成
PowerPoint (.pptx)
```

## 与 v5.x 的改进

1. ✅ **输出格式**：从视频改为 PowerPoint (.pptx)
2. ✅ **移除音频**：不再需要背景音乐处理
3. ✅ **移除FFmpeg**：不再需要视频合成
4. ✅ **直接可用**：生成的 PPTX 可直接编辑和演示
5. ✅ **保留核心**：保留目录驱动、智能布局、现代主题

## v6.0 架构图

```
┌─────────────────┐
│   videofy.py    │
│   (CLI入口)     │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐   ┌─▼─────────────┐
│Parser │   │ PagePlanner   │
│Module │   │ (目录驱动)     │
└───┬───┘   └───────┬───────┘
    │               │
    │         ┌─────┴─────┐
    │         │  Agenda   │
    │         │  Slides   │
    │         └─────┬─────┘
    │               │
    └───────┬───────┘
            │
    ┌───────▼────────┐
    │ PPTXGenerator  │
│  python-pptx   │
    └───────┬────────┘
            │
    ┌───────▼────────┐
    │   output.pptx  │
    └────────────────┘
```
