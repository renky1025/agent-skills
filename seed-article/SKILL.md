---
name: seed-article
description: 从本地 Markdown 文件和可选封面图片一键清理、翻译、总结并发布文章到 YorkTools CMS 系统的技能。直接利用 AI 自身的能力在上下文中完成翻译与提炼，不需要调用任何外部 AI/翻译接口，最后通过本地脚本上传封面并创建文章。当用户提出类似“帮我把这个 markdown 导入到 YorkTools/CMS”、“使用 seed-article 导入/发布文章”、“帮我清理翻译并发布这篇文章”等命令并给出 markdown 路径/内容时触发。
---

# YorkTools Markdown 导入与翻译技能

本技能指导 AI 助手（如 Claude 或 Gemini）读取本地 Markdown 文章，清理非法字符、标签和超链接，利用助手的原生语言理解和翻译能力对原文进行完整清理，并在翻译成目标语言（中/英）时进行**概括提炼式翻译**，然后使用本地发布脚本将文章发布到 YorkTools CMS 系统。

## 用法

当用户给出类似以下指令时，触发该技能：
- "帮我把本地 markdown 文件 `path/to/article.md` 发布到网站"
- "使用 seed-article 导入文章 `article.md` 并使用封面 `cover.png`"
- "导入文章：文件是 `my-post.md`，封面是 `images/cover.png`"

## 工作流

### 第一步：读取源文件

1. 使用 `view_file` 工具读取用户指定的 Markdown 文件（例如 `<source_file>`）。
2. 获取文件名，如果存在可选的本地封面图片路径（例如 `<cover_image>`），记录该路径。

### 第二步：清理 Markdown 格式（在 AI 内部/上下文中执行）

处理 Markdown 正文内容时，执行以下清洗操作以保证内容格式的正确与安全：
1. **删除 HTML 注释**：移除 `<!-- ... -->` 格式的内容。
2. **清除不安全标签**：移除 `<script>`、`<style>`、`<iframe>` 标签及其包含的内容。
3. **移除所有超链接**：
   - 移除 inline 链接：将 `[链接文本](URL)` 替换为 `链接文本`（注意：**不要**影响图片 `![alt](URL)`）。
   - 移除引用式链接：将 `[链接文本][ref]` 替换为 `链接文本`。
   - 移除引用定义：删除类似 `[ref]: URL` 的行。
   - 移除 HTML 链接：将 `<a href="...">链接文本</a>` 替换为 `链接文本`。
   - 移除尖括号包裹的 URL：将 `<http://...>` 替换为 `http://...` 或直接作为纯文本 URL。
4. **规范化文本 HTML 标签**：将常见加粗/斜体 HTML 标签（如 `<b>`、`<strong>`、`<i>`、`<em>`、`<code>`）转换为 Markdown 语法（`**`、`*`、`` ` ``），并剥离其他所有不安全/不支持的 HTML 标签（如 `<div>`、`<p>` 等），只保留内部纯文本。

### 第三步：AI 翻译与提炼（在 AI 内部/上下文中执行）

**关键原则：不要调用外部 AI 接口、上游大模型或翻译 API。直接利用助手自身的语言和翻译能力在当前对话上下文中完成翻译与总结工作。**

1. **语言检测**：
   - 如果 Markdown 主要内容中包含中文字符，则源语言为 `zh`，目标语言为 `en`。
   - 否则，源语言为 `en`，目标语言为 `zh`。

2. **字段处理**：
   - **标题**：提取 Markdown 的主标题（例如第一个 `# 标题` 或 YAML Front-matter 中的 `title`）。如果都没有，则以文件名作为默认标题。同时将标题翻译成目标语言。
   - **Slug**：
     - 中英文 Slug 必须保持完全一致（以避免前台语言切换时出现 404 错误）。
     - 统一生成一个以英文单词表示的、URL 友好的 Slug（全小写，仅包含字母、数字和短横线 `-`）。无论是 JSON 根部的 `slug`，还是 `translations.zh` 和 `translations.en` 下的 `slug`，都必须使用这个完全相同的英文 Slug 值。
   - **来源地址 (Source URL)**：
     - 从 Markdown 正文的开头或特定行中提取来源地址。寻找类似 `来源: <url>` 或 `Source: <url>` 的行，提取出该 URL 并填入 JSON 对象根部的 `"source"` 字段。若未找到，则默认为空字符串 `""`。
   - **摘要**：
     - 源语言摘要：自动生成源语言 100-150 字的简短摘要。
     - 目标语言摘要：由 AI 概括提炼成目标语言的 100-150 字简短摘要。
   - **正文内容**：
     - **源语言正文**：直接使用第二步清理后的**完整** Markdown 正文。
     - **目标语言正文**：使用 **概括提炼方式（编译）** 将正文翻译成目标语言。**不需要逐字逐句翻译**，应当对正文内容进行精简和结构化提炼，保留核心论点、关键信息和 Markdown 格式（如标题、列表、粗体），避免翻译出无用细节或长篇累赘，且**绝对不能**含有任何超链接。
   - **SEO 字段**：
     - `seoTitle`：`{Title} - CoworkAI`（分别对应各自语言的标题）。
     - `seoDescription`：各自语言的摘要。
     - `seoKeywords`：根据文章内容为两种语言各提取 2-4 个关键词，逗号分隔（例如 `AI,写作` 或 `AI,Writing`）。
   - **标签（tags）**：
     - 提取 1-2 个通用标签，放到 `tags` 数组中。

3. **拼装结构化数据**：
   将上述字段整理为符合 YorkTools 文章接口规范的 JSON 对象，示例如下：
   ```json
   {
     "slug": "<identical_english_slug>",
     "title": "<source_lang_title>",
     "summary": "<source_lang_summary>",
     "content": "<source_lang_full_cleaned_content>",
     "tag": "<source_lang_default_tag_eg_知识分享_or_Knowledge>",
     "source": "<extracted_source_url_or_empty>",
     "coverImage": null,
     "status": "published",
     "isFeatured": false,
     "tags": ["AI"],
     "translations": {
       "zh": {
         "slug": "<identical_english_slug>",
         "title": "<zh_title>",
         "summary": "<zh_summary>",
         "content": "<zh_content_full_or_distilled>",
         "tag": "知识分享",
         "seoTitle": "<zh_title> - CoworkAI",
         "seoDescription": "<zh_summary>",
         "seoKeywords": "关键词1,关键词2"
       },
       "en": {
         "slug": "<identical_english_slug>",
         "title": "<en_title>",
         "summary": "<en_summary>",
         "content": "<en_content_full_or_distilled>",
         "tag": "Knowledge",
         "seoTitle": "<en_title> - CoworkAI",
         "seoDescription": "<en_summary>",
         "seoKeywords": "keyword1,keyword2"
       }
     }
   }
   ```
   *注意：根据检测源语言不同，源语言的 `content` 使用完整的 cleaned markdown，而目标语言的 `content` 使用提炼概括后的翻译。*

### 第四步：写入临时数据文件

1. 将拼装好的 JSON 对象写入本地临时文件，文件路径为 `scripts/temp-payload.json`。
2. 使用 `write_to_file` 工具将 JSON 字符串写入此文件。

### 第五步：调用本地发布脚本

1. 使用 `run_command` 工具，在工作空间根目录下执行以下命令：
   ```bash
   ./scripts/seed-content.sh publish scripts/temp-payload.json <cover_image_path>
   ```
   *注意：如果用户没有提供封面图片，则省略最后一个参数：*
   ```bash
   ./scripts/seed-content.sh publish scripts/temp-payload.json
   ```
2. 运行完毕后，使用 `run_command` 删除临时 JSON 文件 `scripts/temp-payload.json`：
   ```bash
   rm scripts/temp-payload.json
   ```
3. 解析脚本输出，提取新创建文章的 ID、Slug 和访问链接，回复用户。
