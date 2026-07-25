---
name: infocard
description: "从 URL 或文本内容生成可定制样式的信息卡片图片。智能分析内容结构，动态选择最适合的视觉呈现方式。默认输出与原文同语言的单语卡片到 ~/Downloads/infocard-img/。使用方法：/infocard <URL|文本> [--theme=slate|ocean|sunset|coral|indigo|forest|dark|purple|guofeng] [--width=1080] [--lang=auto|zh|en|both]"
user_invocable: true
version: "6.6.0"
---

# infocard: 智能信息卡片生成器

将任意 URL 内容转化为精美的信息卡片图片。**核心能力：先理解内容，再根据内容特征选择最适合的视觉形式**。

> **设计理念**: 不存在"默认布局"。每一张卡片的视觉形式，都从内容的思想形状中生长出来。

## 使用方法

```
/infocard <URL 或 文本> [--theme=<theme>] [--width=<width>] [--output=<name>]
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `URL 或 文本` | 网页链接 或 纯文本内容 | 必填 |
| `--theme` | 配色主题：`slate`(默认)、`ocean`、`sunset`、`coral`、`indigo`、`forest`、`dark`、`purple`、`dashboard`、`guofeng` | `slate` |
| `--width` | 图片宽度 | `1080` |
| `--output` | 输出文件名（不含扩展名） | 自动提取 |
| `--lang` | 语言版本：`auto`(自动检测，默认)、`zh`(中文)、`en`(英文)、`both`(双语) | `auto` |

### 输出规则

- **默认保存目录**：`~/Downloads/infocard-img/`
- **默认行为（`--lang=auto`）**：自动检测原文语言，仅生成与原文同语言的单语卡片
  - 文件名：`{name}.{ext}`（不添加语言后缀）
- **单语版本**：`--lang=zh` 或 `--lang=en` 时仅生成对应语言版本
  - 文件名：`{name}_zh.png` 或 `{name}_en.png`
- **双语版本**：`--lang=both` 时自动生成中英文两张卡片
  - 中文版文件名：`{name}_zh.png`
  - 英文版文件名：`{name}_en.png`
- 输出目录自动创建，无需手动新建

## 核心设计理念

**内容驱动布局** —— 先理解内容，再选择布局：

1. 提取元信息（标题、副标题、核心要点、金句）
2. **内容精炼**（🔴 关键步骤）—— 将原始内容转化为"知识分享"而非"摘要"：
   - 确定卡片模式（概念解说 / 金句卡片 / 密集知识）
   - 设计类比和具体例子，让抽象概念可感
   - 确保每个区块都在回答"为什么"而非"是什么"
   - 验证：读者看完能否用自己的话复述？
3. 三个维度判断（密度、结构、情绪）
4. 根据判断选择布局和配色
5. 生成匹配的 HTML

## 执行步骤

### 步骤 0: 解析用户输入（必须先执行）

在开始任何操作前，**必须首先解析用户的消息**提取输入内容：

**输入类型判断**（按优先级）：
1. 如果用户消息以 `/infocard` 开头，提取其后第一个非 `--` 开头的 token 作为输入
2. 否则从用户消息中直接查找

**输入类型判定**：
- `input_type = "url"`：当输入以 `http://` 或 `https://` 开头（包括引号内的 URL），提取 URL
- `input_type = "text"`：当输入不是 URL，视为纯文本内容，直接作为卡片素材

**参数提取**（从同一消息中提取）：
- `--theme=xxx` → theme 参数
- `--width=xxx` → width 参数
- `--output=xxx` → output 参数
- `--lang=xxx` → lang 参数

**参数缺省值**：
- `theme`: `slate`
- `width`: `1080`
- `lang`: `auto`
- `output`: URL 输入时从链接自动提取；文本输入时用内容前 20 字

**验证**：必须提取到输入内容（URL 或文本）才能进入步骤 1。无输入则提示用户提供。

### 步骤 1: 获取内容

根据 `input_type` 获取内容：

**如果 `input_type = "url"`**：使用 agent-reach 技能的路由机制获取 URL 内容：

| URL 平台 | agent-reach 命令 |
|---------|-----------------|
| Twitter/X (`x.com` / `twitter.com`) | `twitter tweet <URL>` |
| GitHub (`github.com`) | `gh` CLI 或 Jina Reader |
| 微信公众号 (`mp.weixin.qq.com`) | Exa MCP (`mcporter call 'exa.crawling_exa(...)'`) 或 Camoufox |
| 通用网页 | Jina Reader: `curl -s "https://r.jina.ai/<URL>"` |
| 其他平台 | 回退到 Jina Reader 或 WebFetch |

**如果 `input_type = "text"`**：直接使用用户提供的文本作为内容来源，跳过此步骤。

提取完成后：提取文章/帖子正文、作者、发布时间等元信息。

### 步骤 2: 提取元信息

从内容中提取以下信息：

1. **标题**：≤ 15 字，内容的核心概念
2. **副标题**：一句话核心观点，≤ 30 字
3. **来源**：内容出处（作者、网站名等）
4. **核心要点**：列出关键点，每个用一句话
5. **金句**：独立成段的短句（< 25 字），承载核心洞察
6. **数据**：如有数字、百分比、统计

#### 🔴 内容质量规则：知识分享 × 理解传递（对所有内容适用）

元信息提取完成后，**卡片的最终内容必须是一篇独立的"知识分享"，而不是一篇"摘要"**。这决定了卡片里写什么、怎么写。

**黄金标准：卡片应该让读者看完说"原来如此"，而不是"哦，讲了这些"。**

**三类内容模式，根据内容特征选择：**

**模式 A — 概念解说（适合：科普、原理、方法论）**
卡片的核心是"解释一个概念为什么有意思"。不是罗列要点，而是：
- 先抛出一个**让人好奇的问题**（"为什么一次性检索不够？"）
- 用**类比或比喻**让抽象概念变得可感（"像图书馆查书 vs 大脑回忆"）
- 解释**核心机制**（Cue → Tag → Content 如何工作）
- 点明**为什么这很重要**（"记忆不是文件，是过程"）
- 关键一：**每个区块都在回答"为什么"**，而不是"是什么"
- 关键二：**必须使用类比**——如果读完不能用自己的话讲给别人听，说明卡片的解释没到位

**模式 B — 金句卡片（适合：观点、洞察、金句）**
卡片的核心是一句话的力量。围绕金句展开：
- 金句占据视觉重心
- 副标题是金句的展开阐释
- 可用 2-3 个短句提供背景支撑，**但不得冲淡金句的冲击力**
- 留白 ≥ 50%，一个巨大元素统治画面

**模式 C — 密集知识（适合：教程、对比、产品介绍）**
卡片的核心是信息密度和结构清晰：
- 按逻辑分层排布（并列/流程/层级）
- 每个区块有独立标题
- 可以用编号、图标辅助导航
- 数据和规格突出显示
- 留白 ≤ 30%

**提取原则（全部场景）：**

- **🔴 以原文思想脉络为主线，不做高度概括，不无中生有**：卡片的"知识分享"不是把原文压缩成几条摘要——而是沿着原文的逻辑线索展开，传递原文的核心洞察。具体要求：
  - 内容必须基于原文的具体论述构建，不能脱离原文做"通用概念卡"
  - 不能为了"看起来像知识分享"而编造原文没有的类比、例子或观点
  - 内容结构应反映原文的论述脉络（如：问题→分析→解法→机制），而不是把原文扁平化为几个独立要点
  - 验证：删去所有与原文无关的内容后，剩下的就是卡片全部内容——没有剩余，说明没有编造
- **用类比替代术语解释**：不要写"Cue 是原子级记忆提示"，要写"Cue 是那些细粒度的'记忆钩子'：一个名字、一个时间戳、一个关键词"
- **内容支撑标题**：每个区块都应该让读者更理解标题中的核心概念。如果删掉某个区块不影响理解，它就不该存在
- **传递理解，而非信息**：读者读完应该能向你解释这个概念，而不是复述你写了"3个要点"
- **化抽象为具体**：所有概念必须配具体例子，例子的优先级是：生活类比 > 具体场景 > 技术描述

#### 🔴 产品发布/对比类内容特殊提取规则

当内容涉及**产品发布、模型对比、功能介绍**时（如 AI 模型发布、软件更新、竞品对比），必须额外提取：

1. **核心优势**：产品/模型最突出的 3-5 个卖点（如"成本降低 60x"、"性能提升 35%"）
2. **对比数据**：与竞品的直接对比（排名、分数、价格、速度等），**必须提取具体数值**
3. **规格参数**：关键技术指标（参数量、上下文窗口、定价等）
4. **基准测试**：如有 benchmark 数据，提取具体分数和对比对象
5. **独特卖点**：竞品没有的差异化功能

**提取原则**：
- 对比数据优先于描述性文字
- 具体数值优先于模糊表述（"69.4%" 优于 "接近顶级水平"）
- 成本/性能比是核心决策因素，必须突出
- 排名/位置信息要清晰（第几名、超过谁）

### 步骤 3: 三个维度判断（关键）

对内容做三个判断，这决定了视觉形式：

#### 3.1 密度（决定画面呼吸）

| 密度 | 核心内容量 | 画面特征 |
|------|-----------|---------|
| **稀** | ≤ 50 字可说清 | 一个巨大元素统治画面，留白 ≥ 60% |
| **中** | 50-200 字 | 有结构的布局，2-3 个主要区块，留白 30-50% |
| **密** | 200+ 字 | 多区块密集排版，留白 ≤ 30% |

**判断方法**：数核心内容字数，不计标题和修饰词。

#### 3.2 结构（决定画面几何）

| 结构 | 信号 | 视觉形式 |
|------|------|---------|
| **单点** | 一个核心概念 | 一个锚点占据重心 |
| **对比** | A vs B、旧 vs 新 | 左右/上下分裂对立 |
| **层级** | 底层支撑上层 | 金字塔、阶梯、嵌套 |
| **流程** | 先后顺序 | 纵向瀑布、时间轴 |
| **辐射** | 核心 + 衍生 | 中心放射 |
| **并列** | 多个并行概念 | 非对称网格 |

**判断方法**：看内容的组织形式，是总分、对比、递进还是并列。

#### 3.3 情绪/色调（决定画面温度）

| 情绪 | 色调 | 触发信号 |
|------|------|---------|
| 沉思的 | slate/indigo | 哲学、认知、本质、意义、思考 |
| 锐利的 | coral/sunset | 批判、解构、争议、对立 |
| 温暖的 | forest | 人文、情感、生活、故事 |
| 技术的 | ocean/dark/purple | 架构、系统、算法、代码、工程、CLI工具 |
| 科研的 | ocean/forest | 论文、实验、数据、研究 |
| 创意的 | sunset/coral | 艺术、设计、创作、美学 |
| 优雅的 | guofeng | 文艺、人文、传统美学、文化内容、古典艺术 |
| **发布的** | **dashboard** | **产品发布、模型更新、功能对比、规格参数、基准测试、定价信息** |

**判断方法**：扫描内容高频关键词，匹配最贴近的情绪。

**🔴 dashboard 风格触发条件**（满足任一即使用）：
- 内容包含产品/模型发布 announcement
- 有明确的竞品对比数据（排名、分数、价格对比）
- 包含技术规格参数表（参数量、定价、性能指标）
- 有 benchmark 基准测试结果
- 核心卖点是"性价比"或"性能优势"

### 步骤 4: 输出判断

根据三个维度，输出设计决策：

```
密度：[稀/中/密]
结构：[单点/对比/层级/流程/辐射/并列]
情绪：[沉思/锐利/温暖/技术/科研/创意/发布]
锚点：[画面中最大的元素是什么？]
配色：[根据情绪选择的主题]
```

**🔴 产品发布/对比类内容必须输出**：
```
核心优势：[列出 3-5 个核心卖点]
对比数据：[竞品对比的具体数值]
规格参数：[关键技术指标]
```

### 步骤 5: 布局选择

根据步骤 4 的判断选择布局：

**密度 → 留白程度：**
- 稀：单栏大字，大量留白
- 中：双栏网格，错落分布
- 密：紧凑排版，多层级

**结构 → 几何形式：**
- 单点：锚点在中心/顶部
- 对比：左右分栏
- 层级：上下堆叠
- 流程：纵向排列
- 辐射：中心发散
- 并列：网格布局

**情绪 → 配色和字体：**
- 沉思：灰色调，serif 字体
- 锐利：强对比，粉色弹点
- 温暖：绿色调，圆润布局
- 技术：蓝色调，mono 字体
- **发布（dashboard）：深色背景 + 绿色强调色，网格分区块，数据表格，编号分区**

#### dashboard 风格布局规范

当判断为 dashboard 风格时，遵循以下布局规则：

1. **深色背景**：使用 `#0A0A0A` 或接近纯黑的背景
2. **绿色强调色**：主 accent 使用 `#4ADE80`（亮绿色），用于关键数据和高亮
3. **网格分区块**：内容分为 2-6 个编号区块（1, 2, 3...），每个区块有独立边框
4. **数据表格**：对比数据用表格或并排卡片展示，突出数值差异
5. **编号系统**：每个区块左上角显示编号（圆形或方形 badge）
6. **图标 + 文字**：每个区块标题配图标，增强可读性
7. **顶部大标题**：产品名称/发布主题用超大字号（48-56px）
8. **底部信息**：定价、CTA、来源放在底部
9. **留白控制**：区块间距 16-24px，区块内 padding 20-28px
10. **字体**：使用 Inter 或 Noto Sans SC，粗体用于关键数据

### 步骤 6: 确定目标语言

根据 `--lang` 参数确定生成语言：

| `--lang` 值 | 行为 |
|-------------|------|
| `auto`（默认） | 自动检测原文语言，生成同语言单语卡片 |
| `zh` | 强制生成中文版（若原文非中文，**必须翻译**） |
| `en` | 强制生成英文版（若原文非英文，**必须翻译**） |
| `both` | 生成中英文两张卡片 |

**🔴 翻译规则（所有跨语言场景均适用）**：

只要源语言与目标语言不同，**必须使用 `/translate-polisher` 技能进行翻译，严禁直接机翻或直译**。这适用于 `--lang=zh`（原文英文时）、`--lang=en`（原文中文时）以及 `--lang=both`。

> **为什么要用 translate-polisher**：直译会产生不通顺的译文（如"几乎没有 Claude 能读取的信息是 HTML 无法高效表达的"），不符合中文语境。translate-polisher 的四步精翻流程能确保输出地道、自然的目标语言文本。

**翻译流程**：
1. 将步骤 2 提取的元信息（标题、副标题、核心要点、金句、提示示例等）整理为待翻译文本
2. 调用 `/translate-polisher` 进行翻译
3. 使用翻译技能返回的终稿填充卡片内容
4. 术语、品牌名、产品名（如 Claude Code、HTML、Markdown、MCP）保留原文不译

**注意**：卡片内容属于短文本，translate-polisher 会自动适配短文本处理流程。

**🔴 翻译保真规则**：如果英文翻译成中文后**无法准确传达原文含义**（包括但不限于：技术概念非中文原生、文化特定表达、原文精炼短语在中文中找不到等价的简洁表达），则**保留英文原文，不强制翻译**。宁可让读者读英文原文，也不要因强行翻译导致信息失真。例如："one-shot"不要硬译成"一次性解决"，"intent alignment"不要硬译成"意图对齐"（如果"对齐"在中文上下文中难以传达原意），直接保留英文。

**语言检测规则**：
- 扫描提取的标题和正文内容
- 若中文字符占比 > 50%，判定为中文内容
- 否则判定为英文内容
- 检测完成后记录判定结果，后续步骤使用

### 步骤 7: 生成 HTML

根据确定的 target language 生成对应语言的 HTML。

#### 🔴 强制 HTML 结构规则（违反必出错）

capture.js 截图流程会**强制剥离 body 上的 padding/margin/flex/min-height**，然后用 `.card` 或 `.container` 来定位卡片边界。不遵守以下规则会导致内容被裁切、只剩标题等问题：

> **记住：body 是画布，`.card` 才是卡片。**

**必须遵守的规则：**

1. **必须包裹 `<div class="card">`**：`<body>` 的第一个子元素必须是 `<div class="card">`，所有内容放里面
2. **body 不得有 padding/margin**：所有间距写到 `.card` 上（capture.js 会把 body padding 清零）
3. **body 不得使用 flex/grid 居中**：capture.js 会把 `display` 强制改为 `block`
4. **body 不得使用 `min-height`/`100vh`**：capture.js 会强制改为 `auto`
5. **`.card` 必须设置固定宽度**：`.card { width: 1080px; box-sizing: border-box; }`（padding 计入总宽）
6. **body 只需设置背景色和固定宽度**：`body { background: var(--bg); width: 1080px; margin: 0; padding: 0; }`
7. **所有视觉间距写在 `.card` 上**：padding、布局、颜色等全部在 `.card` 内处理

**最小正确骨架：**
```html
<style>
  body {
    background-color: var(--bg);
    width: 1080px;
    margin: 0;
    padding: 0;
  }
  .card {
    width: 1080px;
    padding: 72px 64px 48px;
    box-sizing: border-box;
    color: var(--text-primary);
    font-family: ...;
  }
</style>
<body>
<div class="card">
  <!-- 所有内容放在这里 -->
</div>
</body>
```

**布局规范：**
- **顶部（Header）**：只放核心标题、副标题、内容主题相关元素
- **作者信息**：仅保留作者名，放在底部（Footer）不显眼位置
- **来源、日期**：不显示
- Footer 样式：字号 12-13px，颜色使用 `var(--text-secondary)` 或更低透明度

**🔴 图标使用规范 — 内联 SVG 雪碧图（必须使用，禁止 CDN Web Component）：**

**关键规则**：capture.js 截图时，`esm.sh/ionicons@8.0.0/loader` 等 CDN Web Component 可能因网络延迟或渲染时机问题导致图标缺失。**必须使用内联 SVG `<use>` 雪碧图**，零外部依赖，截图 100% 可靠。

**正确做法：**
- 在 `<body>` 之前定义 `<svg style="display:none"><defs>` 雪碧图，包含所有需要的图标
- 使用 `<svg class="icon" viewBox="0 0 24 24"><use href="#i-xxx"/></svg>` 引用图标
- 定义通用 `.icon` CSS 类控制大小和颜色
- 每个内容区块最多使用 1 个图标，避免过度装饰

**必须包含的 CSS（在 `<style>` 中添加）：**
```css
.icon { width: 1em; height: 1em; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; display: inline-block; vertical-align: -0.125em; flex-shrink: 0; pointer-events: none; }
```

**必须包含的 SVG 雪碧图骨架（在 `<body>` 前添加）：**
```html
<svg style="display:none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <symbol id="i-flash" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></symbol>
    <symbol id="i-sparkles" viewBox="0 0 24 24"><path d="M12 3l1.5 4.5L18 9l-4.5 1.5L12 15l-1.5-4.5L6 9l4.5-1.5L12 3z"/><path d="M5 17l1 2.5L8.5 20l-2.5 1L5 23l-1-2.5L1.5 20 4 19.5 5 17z"/><path d="M19 14l.5 1.5L21 16l-1.5.5L19 18l-.5-1.5L17 16l1.5-.5L19 14z"/></symbol>
    <symbol id="i-layers" viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></symbol>
    <symbol id="i-speed" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></symbol>
    <symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></symbol>
    <symbol id="i-branch" viewBox="0 0 24 24"><line x1="6" y1="3" x2="6" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 01-9 9"/></symbol>
    <symbol id="i-bulb" viewBox="0 0 24 24"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0018 8 6 6 0 006 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 008.91 14"/></symbol>
    <symbol id="i-chart" viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></symbol>
    <symbol id="i-compare" viewBox="0 0 24 24"><circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M13 6h3a2 2 0 012 2v7"/><line x1="6" y1="9" x2="6" y2="21"/></symbol>
    <symbol id="i-code" viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></symbol>
    <symbol id="i-book" viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 016.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/></symbol>
    <symbol id="i-people" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></symbol>
    <symbol id="i-check" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></symbol>
  </defs>
</svg>
```

**内容类型 → 图标 ID 映射：**

| 内容类型 | 推荐图标 ID | 使用位置 |
|---------|------------|---------|
| 核心观点 / 洞察 | `i-bulb` | section-title, feature-icon |
| 功能 / 特性 | `i-sparkles` | feature-icon, card-icon |
| 步骤 / 流程 | `i-layers` | section-title, step-icon |
| 对比 / 比较 | `i-compare` | section-title |
| 数据 / 统计 | `i-chart` | data-item, metric-item |
| 代码 / 技术 | `i-code` | section-title, code-block |
| 安全 / 认证 | `i-shield` | feature-card |
| 性能 / 速度 | `i-flash`, `i-speed` | metric-item |
| 引用 / 金句 | `i-bulb` | quote-icon |
| 总结 / 要点 | `i-check` | summary-box |
| 来源 / 链接 | `i-book`, `i-code` | footer |

**图标使用示例：**

```html
<!-- 区块标题带图标 -->
<div class="section-title">
  <svg class="icon" viewBox="0 0 24 24"><use href="#i-bulb"/></svg>
  核心观点
</div>

<!-- 特性卡片带图标 -->
<div class="feature-item">
  <svg class="feature-icon" viewBox="0 0 24 24"><use href="#i-sparkles"/></svg>
  <div class="feature-text">
    <strong>实时协作</strong>
    多人同时编辑，实时同步
  </div>
</div>

<!-- 步骤带图标 -->
<div class="step-title">
  <svg class="step-icon" viewBox="0 0 24 24"><use href="#i-layers"/></svg>
  第一步：安装 CLI
</div>

<!-- 列表项带图标 -->
<ul class="bullet-list">
  <li><svg class="icon" viewBox="0 0 24 24"><use href="#i-check"/></svg>支持 TypeScript 类型推导</li>
</ul>

<!-- 引用带图标 -->
<div class="quote-section">
  <svg class="quote-icon" viewBox="0 0 24 24"><use href="#i-bulb"/></svg>
  <div class="quote-text">代码是写给人看的，顺带能在机器上运行</div>
</div>
```

**单语生成（`--lang=auto/zh/en`）**：
- 若目标语言为中文：
  - 使用 `Noto Sans SC` 字体
  - HTML 写入 `/tmp/infocard_{name}.html`
- 若目标语言为英文：
  - 使用 `Inter` 字体
  - HTML 写入 `/tmp/infocard_{name}.html`

**双语生成（`--lang=both`）**：
- 中文版：使用 `Noto Sans SC`，写入 `/tmp/infocard_{name}_zh.html`
- 英文版：需先翻译，再使用 `Inter`，写入 `/tmp/infocard_{name}_en.html`

#### 翻译子步骤（源语言 ≠ 目标语言时执行）

**必须使用 `/translate-polisher` 技能翻译，不得直接翻译。**

1. 将步骤 2 提取的元信息（标题、副标题、核心要点、金句等）整理为待翻译文本
2. 调用 `/translate-polisher` 进行翻译（中文→英文 或 英文→中文）
3. 使用翻译技能返回的终稿作为另一语言版本内容

**注意**：
- 卡片内容属于短文本，translate-polisher 会自动适配短文本处理流程
- 术语、品牌名、产品名等专有名词保留原文不译
- 保留原文格式标记（如加粗、链接等）

### 步骤 8: 截图生成

```bash
mkdir -p ~/Downloads/infocard-img
```

**单语截图（`--lang=auto/zh/en`）**：
```bash
node infocard/assets/capture.js /tmp/infocard_{name}.html ~/Downloads/infocard-img/{name}.png 1080 800 fullpage
```

**双语截图（`--lang=both`）**：
```bash
node infocard/assets/capture.js /tmp/infocard_{name}_zh.html ~/Downloads/infocard-img/{name}_zh.png 1080 800 fullpage
node infocard/assets/capture.js /tmp/infocard_{name}_en.html ~/Downloads/infocard-img/{name}_en.png 1080 800 fullpage
```

## 主题配色

### slate（默认）
适合：沉思、技术
```
--bg: #F8FAFC
--text-primary: #0F172A
--text-secondary: #475569
--accent: #0F172A
--border: #E2E8F0
```

### ocean
适合：技术、科研、现代 SaaS
```
--bg: #F4F6F9
--card-bg: #FFFFFF
--text-primary: #0F1A2C
--text-secondary: #5B7294
--accent: #0E8C8A
--accent-light: #EBF4F4
--border: #E4EAF1
--highlight-bg: #F7FAFC
--dark-card: #0D2638
```

### coral
适合：锐利、创意
```
--bg: #FFF1F2
--text-primary: #4C0519
--accent: #E11D48
--border: #FFE4E6
```

### indigo
适合：沉思、教育
```
--bg: #EEF2FF
--text-primary: #1E1B4B
--accent: #4F46E5
--border: #E0E7FF
```

### forest
适合：温暖、科研
```
--bg: #F0FDF4
--text-primary: #052E16
--accent: #16A34A
--border: #DCFCE7
```

### sunset
适合：锐利、创意
```
--bg: #FFFAF4
--text-primary: #451A03
--accent: #EA580C
--border: #FFEDD5
```

### dark
适合：技术、开发者
```
--bg: #0B0F19
--text-primary: #F9FAFB
--accent: #10B981
--border: #1F2937
```

### purple
适合：开发者工具、CLI、暗色科技
```
--bg: #0F111A
--text-primary: #F0F0F5
--text-secondary: #8B8DA3
--accent: #A78BFA
--accent-light: #2A2C3D
--border: #1E2030
--highlight-bg: #181924
--dark-card: #1A1B26
```

### dashboard
适合：产品发布、功能对比、数据展示、技术规格
```
--bg: #0A0A0A
--card-bg: #141414
--text-primary: #FFFFFF
--text-secondary: #A0A0A0
--accent: #4ADE80
--accent-light: rgba(74, 222, 128, 0.1)
--border: #2A2A2A
--highlight-bg: #1A1A1A
--dark-card: #0F0F0F
--green: #4ADE80
--orange: #F59E0B
--blue: #3B82F6
```

### guofeng（国风）
适合：文艺、人文、传统美学、文化内容、古典艺术
```
--bg: #F5EDE0           /* 宣纸暖白 — 仿古宣纸底色 */
--card-bg: #FAF3E7      /* 卡片面 — 略亮的纸色 */
--text-primary: #2D1F14  /* 墨色 — 深棕黑，如浓墨 */
--text-secondary: #7A6A5A /* 茶色 — 温润的棕灰 */
--accent: #C5615C        /* 朱砂红 — 取自画中红袍 */
--accent-light: rgba(197, 97, 92, 0.15)
--border: #E2D4C2        /* 淡赭 — 柔和边界 */
--highlight-bg: #F0E6D6  /* 淡金底 — 暖色高亮区 */
--dark-card: #2D1F14     /* 深墨 — 深色区块底色 */
```

## 示例：内容→判断→布局

### 示例 1：单一观点（稀 + 单点 + 沉思）

**内容**：关于 AI 编程的核心观点
**判断**：稀 + 单点 + 沉思
**布局**：单栏大字，标题突出，大量留白

### 示例 2：方案对比（中 + 对比 + 锐利）

**内容**：Windsurf vs Cursor 对比
**判断**：中 + 对比 + 锐利
**布局**：左右分栏，绿色/红色区分优劣势

### 示例 3：教程步骤（密 + 流程 + 技术）

**内容**：安装配置教程
**判断**：密 + 流程 + 技术
**布局**：纵向步骤排布，小字号紧凑

### 示例 4：产品发布/模型对比（中 + 层级 + 发布）

**内容**：Cursor Composer 2.5 发布，包含基准测试排名、成本对比、规格参数
**判断**：中 + 层级 + 发布
**布局**：dashboard 风格，深色背景 + 绿色强调色，网格分区块展示排名、成本、规格、提升数据

## 注意事项

1. **先理解内容** — 不存在默认布局，先提取内容再判断
2. **密度决定留白** — 稀内容不要硬塞，密内容不要硬撑
3. **结构决定形式** — 对比就用分栏，流程就用纵向
4. **情绪决定配色** — 技术内容配蓝色，温暖内容配绿色
5. **代码换行** — 代码块使用 white-space: pre-wrap
6. **要点+描述** — 每个核心要点搭配说明描述
7. **作者信息位置** — 仅保留作者名，放在底部（Footer）不显眼位置；不显示来源和日期
8. **默认单语输出** — 不指定 `--lang` 时，自动检测原文语言，仅生成一张同语言卡片
9. **双语需显式指定** — 只有用户明确要求 `--lang=both` 时才生成两张卡片
10. **跨语言必须用 translate-polisher** — 只要源语言与目标语言不同（包括 `--lang=zh` 原文英文、`--lang=en` 原文中文），必须通过 `/translate-polisher` 翻译，严禁直译。直译会产生生硬、不符合目标语言语境的文本。
11. **🔴 必须使用内联 SVG 雪碧图替代 CDN Web Component 图标** — capture.js 截图时 `<ion-icon>` 依赖 `esm.sh/ionicons@8.0.0/loader` CDN，可能因网络或渲染时机导致图标缺失。必须使用内联 `<svg><use href="#i-xxx"/></svg>` 方式，零外部依赖。详见"图标使用规范"
12. **🔴 必须用 `.card` 包裹内容** — 所有内容必须放在 `<div class="card">` 内，body 不得有 padding/margin/flex/min-height，否则截图只截到第一个子元素
13. **🔴 产品发布/对比必须用 dashboard 风格** — 当内容涉及产品发布、模型对比、基准测试时，必须使用 dashboard 主题，突出对比数据和核心优势
14. **🔴 对比数据必须提取具体数值** — 不要只写"性能更好"，要写"69.4% vs 64.8%"；不要只写"更便宜"，要写"$0.07 vs $4.10"
15. **🔴 内容必须是知识分享，不是总结** — 卡片是"让读者理解一个概念"，不是"告诉读者原文讲了什么"。区别在于：总结是在原文基础上压缩（删除细节），知识分享是在原文基础上重构（解释为什么重要）。以下两条是判断标准：a) 读者读完是否能用自己的话向别人解释？b) 卡片是否使用了类比或具体例子让抽象概念可感？
16. **🔴 用类比代替术语轰炸** — 每个抽象概念都应配一个生活类比。"检索再推理范式" → "像去图书馆但不确定要找什么书"；"选择性激活" → "只跟随'股票投资'标签，忽略'埃隆·马斯克'"。类比让卡片从"能读"变成"能记住"
17. **🔴 翻译保真优先于强行翻译** — 英文→中文时，如果核心概念、术语或精炼短语翻译后丢失原意或变得冗长，直接保留英文原文。不要为了"全中文"牺牲信息准确性。例如："one-shot"、"intent alignment"、"spec-driven development"如果翻译不精确，宁可保留英文。
18. **🔴 以原文脉络为主线，不编造内容** — 卡片的知识分享必须沿原文的论述逻辑展开（问题→分析→解法→机制等），禁止脱离原文做高度概括，禁止编造原文没有的类比、例子或观点。卡片的每一句话都应有原文依据。

## 常见错误

1. **不看内容直接套模板** — 必须在步骤 2 提取内容
2. **密度判断错误** — 把修饰词算进去，要算核心内容
3. **结构判断错误** — 对比内容用单点布局是大忌
4. **情绪配错色调** — 哲学内容配粉色会很奇怪
5. **默认生成双语** — 未确认用户意图就生成两张卡片；默认应只生成一张
6. **直接翻译而非使用翻译技能** — 只要源语言与目标语言不同（包括 `--lang=zh/en/both`），必须通过 `/translate-polisher` 翻译，不得自行直译。直译会产生硬译腔、不符合目标语言习惯。
7. **🔴 把 padding 写在 body 上** — 这是最常见的截图裁切错误。body 上的 padding/margin 会被 capture.js 强制清零。所有间距必须写在 `.card` 上。
8. **🔴 忘记包裹 `.card` 元素** — capture.js 通过 `.card` 或 `.container` 定位卡片边界。如果没有这个包裹元素，截图只会拍到 body 的第一个子元素（通常是 header/标题）。
9. **🔴 产品发布内容不用 dashboard 风格** — 模型发布、竞品对比、基准测试必须用 dashboard 深色网格布局，不能用普通浅色卡片
10. ** 对比数据只写描述不写数值** — "成本更低" 是无效信息，必须写 "$0.07 vs $4.10（降低 60 倍）"
11. **🔴 没有提取核心优势** — 产品发布类内容必须提取 3-5 个核心卖点，不能只罗列功能
12. **🔴 把卡片写成论文摘要** — 最常见的错误：列出 5 个"核心要点"，每个都是名词解释级别的概括（"范式转变"、"CTC图结构"）。读者看到这 5 个点只会记住"有这些东西"，但完全不懂为什么。正确做法：选择一个角度，深入解释，让读者真的理解。
13. **🔴 没有类比，全是抽象术语** — 如果卡片里连续出现 3 个以上专业术语没有类比或具体例子，立即重写。术语属于原文摘要，不属于知识分享。
14. **🔴 内容脱节于标题** — 写完所有区块后检查：每个区块是否都能让人更理解标题里的概念？如果有一个区块删掉不影响对标题的理解，它就不属于这张卡片。
15. **🔴 强行翻译导致信息失真** — 英文原文中精确的概念（如 "one-shot"、"intent alignment"、"spec-driven development"）在中文中没有完美对应的简洁表达时，强行翻译成冗长或不准确的短语。宁可保留英文原文，也不要让读者看到"一次性解决方案"这种模糊表述。
16. **🔴 脱离原文编造知识分享** — 读了原文后不按原文逻辑走，自己编一套"通用知识框架"替换原文的具体内容。例如：原文讲的是在AI工作流中插入Spec Agent来处理复杂Issue，却做了一张通用的"为什么要写规格说明"卡片。卡片内容必须基于原文的具体内容，不能替换成另一篇文章。
17. **🔴 使用 `<ion-icon>` CDN Web Component 导致截图图标缺失** — `esm.sh/ionicons@8.0.0/loader` 在 Playwright 截图时可能因 web component 渲染时机或网络问题导致图标不可见。**必须使用内联 SVG `<use>` 雪碧图**。放在 HTML `<head>` 中的 `<script type="module" src="https://esm.sh/ionicons@8.0.0/loader">` 也要一并移除。