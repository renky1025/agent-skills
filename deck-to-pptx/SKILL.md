---
name: deck-to-pptx
description: Use when you need to turn a topic, brief, or local material folder into a visually strong PowerPoint deck quickly
user_invocable: true
version: "0.1.0"
---

# deck-to-pptx

将主题、说明或本地资料目录快速生成成品感更强的 `.pptx`。

## 用法

```bash
/deck-to-pptx "<主题或资料路径>" [--outline "<补充说明>"] [--audience "<受众>"] [--tone "<语气>"] [--style auto|tech-dark|business-light|editorial|bold-gradient] [--max-slides 8] [--lang zh|en] [--output /path/to/output.pptx]
```

## 输入模式

- 主题：自动联网补资料，失败时退回通用结构
- 主题 + `--outline`：按给定大纲优先生成
- 本地目录：读取 `md/txt/docx`，可识别目录里的图片

## 输出特性

- 自动目录页
- 强标题和更明显的页面角色
- 4 套内置风格自动选择
- `.pptx` 直接导出
