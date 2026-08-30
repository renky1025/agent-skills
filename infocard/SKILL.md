---
name: infocard
description: "从 URL 或文本生成可定制样式的信息卡片图片。先理解内容，再按密度/结构/情绪选择视觉形式与配色。默认输出与原文同语言的单语卡片到 ~/Downloads/infocard-img/。用法：/infocard <URL|文本> [--theme=guofeng|slate|sunset|coral|indigo|forest|purple|dashboard|editorial] [--width=1080] [--lang=auto|zh|en|both]"
user_invocable: true
version: "6.7.0"
---

# infocard: 智能信息卡片生成器

没有"默认布局"。先读懂内容，再让视觉形式从内容的思想形状中长出来。

## 用法

```
/infocard <URL|文本> [--theme=<theme>] [--width=<width>] [--output=<name>] [--lang=auto|zh|en|both]
```

| 参数 | 说明 | 默认 |
|------|------|------|
| 输入 | 网页链接或纯文本（必填） | — |
| `--theme` | 配色：`guofeng`、`slate`、`sunset`、`coral`、`indigo`、`forest`、`purple`、`dashboard`、`editorial`(默认) | `editorial` |
| `--width` | 图片宽度 | `1080` |
| `--output` | 输出文件名（无扩展名） | 自动提取 |
| `--lang` | 语言：`auto`(自动) / `zh` / `en` / `both`(双语) | `auto` |

输出：`~/Downloads/infocard-img/{name}.png`（双语为 `_zh.png` / `_en.png`，目录自动创建）。

## 执行流程

**0. 解析输入**：提取首个非 `--` 的 token 作输入；`http(s)://` 开头为 URL，否则为文本。`--theme/--width/--output/--lang` 取对应值，缺省如上。无输入则提示用户。

**1. 获取内容**
- URL：Twitter/X → `twitter tweet <URL>`；GitHub → `gh` 或 Jina；微信公众号 → Exa MCP / Camoufox；通用 → `curl -s "https://r.jina.ai/<URL>"` 或 WebFetch。
- 文本：直接采用，跳过本步。
提取正文、作者、来源。

**2. 提取元信息**：标题(≤15字)、副标题(≤30字)、来源、核心要点、金句(<25字)、数据。
三类模式：**概念解说**（提问题 + 类比 + 机制，回答"为什么"）/ **金句**（一句话主导，留白≥50%）/ **密集知识**（分层编号，留白≤30%）。

**内容硬规则（贯穿全程）**
- **知识分享，不是摘要**：沿原文逻辑（问题→分析→解法）展开，解释"为什么"而非罗列"是什么"；读者读完应能复述。
- **用类比替代术语**：每个抽象概念配生活类比或具体场景。
- **不编造**：内容须有原文依据，不脱离原文做通用卡，不虚构类比/例子。
- **产品/对比类**：额外提取核心优势(3-5)、对比数值、规格参数、benchmark；数值优先于模糊描述（写"69.4% vs 64.8%"，不写"更优"）。

**3. 三维判断**
- **密度**：稀(≤50字,留白≥60%) / 中(50-200字) / 密(200+字,留白≤30%)。
- **结构**：单点 / 对比(分栏) / 层级(堆叠) / 流程(纵向) / 辐射(中心) / 并列(网格)。
- **情绪→配色**：沉思→slate/indigo；锐利→coral/sunset；温暖/科研→forest；技术→purple；优雅→guofeng；**发布(产品/模型/对比/benchmark)→dashboard**。

**4. 输出决策**（内部自检）：密度 / 结构 / 情绪 / 锚点 / 配色；发布类另列核心优势、对比数据、规格参数。

**5. 布局**：按结构选形式；dashboard 与 editorial 有专门规范（见「主题配色」）。

**6. 语言**：`auto` 按原文生成单语（中文占比>50% 判中文）；`zh/en` 跨语言须用 `/translate-polisher`（运行时依赖，未安装时降级为内部直译并标注"未校对"）翻译，严禁直译；术语/品牌名(Claude Code、HTML、MCP…)及无法准确对译的短语(one-shot、intent alignment)保留英文。

**7. 生成 HTML**（见下「HTML 规范」）。单语：中文 `Noto Sans SC` / 英文 `Inter`，写 `/tmp/infocard_{name}.html`；双语：先译后写，分别 `_zh.html` / `_en.html`。

**8. 截图**
```bash
mkdir -p ~/Downloads/infocard-img
node ~/.claude/skills/infocard/assets/capture.js /tmp/infocard_{name}.html ~/Downloads/infocard-img/{name}.png 1080 800 fullpage
# 双语：对 _zh.html / _en.html 各跑一次
```

## HTML 规范（违反必出错）

capture.js 会**强制清除 body 的 padding/margin/flex/min-height**，并以 `.card` 定位边界。务必：

1. `<body>` 首子元素为 `<div class="card">`，所有内容在内。
2. body 只设 `background` 与固定 `width:1080px`；margin/padding 为 0。
3. `.card` 设 `width:1080px; box-sizing:border-box;` 并承载全部 padding/布局。
4. 不使用 body 居中、不用 `100vh`/`min-height`。

骨架：
```html
<style>
  body { background: var(--bg); width: 1080px; margin: 0; padding: 0; }
  .card { width: 1080px; padding: 72px 64px 48px; box-sizing: border-box; color: var(--text-primary); font-family: ...; }
</style>
<body><div class="card"><!-- 内容 --></div></body>
```

**布局**：Header 只放标题/副标题；作者名置底栏(Footer, 12-13px, 次级色)；不显示来源/日期。代码块 `white-space:pre-wrap`。

**图标：内联 SVG 雪碧图，禁止 CDN Web Component**（`<ion-icon>` 截图会缺失）。在 `<body>` 前放 `<svg style="display:none"><defs>` 雪碧图，用 `<svg class="icon"><use href="#i-xxx"/></svg>` 引用；每区块至多 1 个图标。通用类：
```css
.icon { width:1em; height:1em; fill:none; stroke:currentColor; stroke-width:2; stroke-linecap:round; stroke-linejoin:round; display:inline-block; vertical-align:-0.125em; flex-shrink:0; pointer-events:none; }
```
雪碧图（按需取用）：
```html
<svg style="display:none" xmlns="http://www.w3.org/2000/svg"><defs>
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
</defs></svg>
```
图标映射：观点/金句→`i-bulb`；特性→`i-sparkles`；步骤/流程→`i-layers`；对比→`i-compare`；数据→`i-chart`；代码→`i-code`；安全→`i-shield`；性能→`i-flash`/`i-speed`；总结→`i-check`；来源→`i-book`。

## 主题配色

### slate · 沉思/技术
```
--bg: #F8FAFC
--text-primary: #0F172A
--text-secondary: #475569
--accent: #0F172A
--border: #E2E8F0
```

### coral · 锐利/创意
```
--bg: #FFF1F2
--text-primary: #4C0519
--accent: #E11D48
--border: #FFE4E6
```

### indigo · 沉思/教育
```
--bg: #EEF2FF
--text-primary: #1E1B4B
--accent: #4F46E5
--border: #E0E7FF
```

### forest · 温暖/科研
```
--bg: #F0FDF4
--text-primary: #052E16
--accent: #16A34A
--border: #DCFCE7
```

### sunset · 锐利/创意
```
--bg: #FFFAF4
--text-primary: #451A03
--accent: #EA580C
--border: #FFEDD5
```

### editorial · 编辑/杂志风（长文/专访/报告/知识图谱）
```
--bg: #F6F1E7
--card-bg: #FFFFFF
--text-primary: #1A1A1A
--text-secondary: #5A544A
--accent: #15233F
--accent-light: #DDE7F0
--border: #D8CFC0
--highlight-bg: #F1ECDE
--dark-card: #15233F
--gold: #F5C518
--navy: #15233F
```
布局：无圆角无阴影，靠发丝线与留白分层。①报头 kicker(作者·来源)+描边胶囊按钮；②双色衬线大标题(英文墨黑/中文藏青,56-72px)；③导语+超大黄色数字锚点(如 10K+)；④发丝线分隔的四列元信息；⑤编号分区01-04(藏青大号Oswald)，末区反白(藏青底/黄号/奶白字)；⑥浅蓝引文块+藏青左线；⑦底部藏青反白总结条+署名。字体：标题/编号/引文衬线(Noto Serif SC、Georgia)，kicker/标签 Oswald，正文 Noto Sans SC/Inter。

### purple · CLI/暗色科技
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

### dashboard · 发布/数据
```
--bg: #0A0A0A
--card-bg: #141414
--text-primary: #FFFFFF
--text-secondary: #A0A0A0
--accent: #4ADE80
--accent-light: rgba(74,222,128,0.1)
--border: #2A2A2A
--highlight-bg: #1A1A1A
--dark-card: #0F0F0F
--green: #4ADE80
--orange: #F59E0B
--blue: #3B82F6
```
布局：深色底+绿色强调；2-6 个编号区块(1,2,3)带边框；对比数据用表格/并排卡；顶部超大产品名(48-56px)；底部放定价/CTA/来源；区块间距16-24px。

### guofeng（默认）· 国风/人文
```
--bg: #F5EDE0
--card-bg: #FAF3E7
--text-primary: #2D1F14
--text-secondary: #7A6A5A
--accent: #C5615C
--accent-light: rgba(197,97,92,0.15)
--border: #E2D4C2
--highlight-bg: #F0E6D6
--dark-card: #2D1F14
```

## 关键约束（一次记牢）

- **先读内容再选布局**：密度定留白、结构定形式、情绪定配色。
- **body 只是画布，`.card` 才是卡片**：间距全写在 `.card`，body 无 padding/居中/`100vh`。
- **图标只用内联 SVG 雪碧图**，禁用 `<ion-icon>` CDN。
- **跨语言必走 `/translate-polisher`**（运行时依赖，缺失时降级为内部直译并标注"未校对"），禁止直译；保真优先，难译处保留英文。
- **发布/对比内容用 dashboard**；对比写具体数值，提取 3-5 核心优势。
- **内容=知识分享≠摘要**：用类比、沿原文脉络、不编造；每区块都服务于理解标题。
- **默认主题 = editorial（杂志风）**：未指定 `--theme` 时采用杂志风（纸色底+白卡、衬线标题、发丝线分层、无圆角无阴影）。
- **元信息禁止插在卡片正中**：作者/日期/阅读量/点赞/收藏等互动数据不是核心知识，以四列网格等形式放在卡片中间既突兀又无意义；作者可置于报头 kicker 或底部署名，互动数据除非本身就是卡片主题否则不展示。
- **内容须忠实原文**：抽取时不擅自改写、增删或"优化"原文要点与数据；保留原文数值与表述，不自行发挥。
- **不显示来源/平台字样**：禁止出现 "X ARTICLE" 等平台标识或来源行；作者可保留，来源不展示。
- 默认单语；双语须显式 `--lang=both`，不擅自生成两张。
