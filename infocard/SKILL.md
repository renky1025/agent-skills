---
name: infocard
description: "从 URL 或文本内容生成可定制样式的信息卡片图片。智能分析内容结构，动态选择最适合的视觉呈现方式。默认输出与原文同语言的单语卡片到 ~/Downloads/infocard-img/。使用方法：/infocard <URL|文本> [--theme=slate|ocean|sunset|coral|indigo|forest|dark|purple] [--width=1080] [--lang=auto|zh|en|both]"
user_invocable: true
version: "6.4.0"
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
| `--theme` | 配色主题：`slate`(默认)、`ocean`、`sunset`、`coral`、`indigo`、`forest`、`dark`、`purple`、`dashboard` | `slate` |
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
2. 三个维度判断（密度、结构、情绪）
3. 根据判断选择布局和配色
4. 生成匹配的 HTML

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

**图标使用规范（Ionicons 8.x）：**
- 图标库已预置于 `template.html`（CDN: `esm.sh/ionicons@8.0.0/loader`），无需额外引入
- 图标元素格式：`<ion-icon name="icon-name"></ion-icon>`
- 统一使用 `outline` 变体（如 `bulb-outline`），与卡片设计风格一致
- 图标颜色自动继承父元素 `color` 属性，跟随主题配色
- 图标应起到视觉引导作用，每个内容区块最多使用 1 个图标，避免过度装饰

**内容类型 → 图标映射：**

| 内容类型 | 推荐图标 | 使用位置 |
|---------|---------|---------|
| 核心观点 / 洞察 | `bulb-outline` | section-title, feature-icon |
| 功能 / 特性 | `sparkles-outline`, `pricetags-outline` | feature-icon, card-icon |
| 步骤 / 流程 | `layers-outline`, `footsteps-outline` | section-title, step-icon |
| 对比 / 比较 | `git-compare-outline`, `swap-horizontal-outline` | section-title |
| 数据 / 统计 | `stats-chart-outline`, `bar-chart-outline` | data-item, metric-item |
| 代码 / 技术 | `code-slash-outline`, `terminal-outline` | section-title, code-block |
| 引用 / 金句 | `chatbubble-ellipses-outline` | quote-icon |
| 总结 / 要点 | `checkmark-circle-outline`, `checkbox-outline` | summary-box |
| 警告 / 注意 | `warning-outline`, `alert-circle-outline` | pain-point-list |
| 来源 / 链接 | `link-outline`, `open-outline` | footer |
| 安全 / 认证 | `shield-checkmark-outline`, `lock-closed-outline` | feature-card |
| 性能 / 速度 | `flash-outline`, `speedometer-outline` | metric-item |
| AI / 智能 | `hardware-chip-outline`, `color-wand-outline` | header-tag |

**图标使用示例：**

```html
<!-- 区块标题带图标 -->
<div class="section-title">
  <ion-icon name="bulb-outline"></ion-icon>
  核心观点
</div>

<!-- 特性卡片带图标 -->
<div class="feature-item">
  <ion-icon class="feature-icon" name="sparkles-outline"></ion-icon>
  <div class="feature-text">
    <strong>实时协作</strong>
    多人同时编辑，实时同步
  </div>
</div>

<!-- 步骤带图标 -->
<div class="step-title">
  <ion-icon class="step-icon" name="footsteps-outline"></ion-icon>
  第一步：安装 CLI
</div>

<!-- 列表项带图标 -->
<ul class="bullet-list">
  <li><ion-icon name="checkmark-circle-outline"></ion-icon>支持 TypeScript 类型推导</li>
</ul>

<!-- 引用带图标 -->
<div class="quote-section">
  <ion-icon class="quote-icon" name="chatbubble-ellipses-outline"></ion-icon>
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
node ~/.claude/skills/infocard/assets/capture.js /tmp/infocard_{name}.html ~/Downloads/infocard-img/{name}.png 1080 800 fullpage
```

**双语截图（`--lang=both`）**：
```bash
node ~/.claude/skills/infocard/assets/capture.js /tmp/infocard_{name}_zh.html ~/Downloads/infocard-img/{name}_zh.png 1080 800 fullpage
node ~/.claude/skills/infocard/assets/capture.js /tmp/infocard_{name}_en.html ~/Downloads/infocard-img/{name}_en.png 1080 800 fullpage
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
11. **图标适度使用** — 每个内容区块最多 1 个图标，统一使用 Ionicons outline 变体；避免重复和过度装饰
12. **🔴 必须用 `.card` 包裹内容** — 所有内容必须放在 `<div class="card">` 内，body 不得有 padding/margin/flex/min-height，否则截图只截到第一个子元素
13. **🔴 产品发布/对比必须用 dashboard 风格** — 当内容涉及产品发布、模型对比、基准测试时，必须使用 dashboard 主题，突出对比数据和核心优势
14. **🔴 对比数据必须提取具体数值** — 不要只写"性能更好"，要写"69.4% vs 64.8%"；不要只写"更便宜"，要写"$0.07 vs $4.10"

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