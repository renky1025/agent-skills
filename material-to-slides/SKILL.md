---
name: material-to-slides
description: "Read and deeply understand any material (URL, local file, pasted text) then generate a single-file HTML slide deck. Default style: Guizang Editorial E-Ink (纸墨印刷感 with 5 palettes). Also supports 3 alternate palettes (Slate/Warm/Forest) for different content moods. Use when the user says '把这个做成PPT', 'generate slides', 'deck', 'presentation', '幻灯片', shares a URL/article/file and wants slides, or wants to convert research/notes/docs into a navigable HTML deck. Supports ←/→ navigation, hash sync, PPTX-friendly print."
zh_name: "资料转幻灯片"
emoji: "📄→🎬"
---

# material-to-slides

将任意资料（URL / 本地文件 / 粘贴文本）阅读理解后，生成可直接播放的 HTML 幻灯片。

## 核心工作流（四阶段，严格按顺序）

### 阶段一：读取内容 (Read)

| 输入类型 | 操作 |
|----------|------|
| **URL** | 使用 `webfetch` 获取内容（优先 markdown）；如果是 GitHub 仓库，探索 README 和关键文档 |
| **本地文件** | 使用 `read` 读取 |
| **粘贴文本** | 直接使用 |
| **搜索需求** | 用 `websearch` 获取资料再处理 |

确认内容完整性 — 如果过短或明显不完整，告知用户并请求补充。

### 阶段二：深度理解 (Understand)

逐段分析内容，回答：

1. **核心识别** — 一句话主题？核心论点？资料类型（论文/新闻/产品文档/观点/教程/报告）？
2. **结构分析** — 如何组织的？各部分逻辑关系（递进/并列/因果/对比）？
3. **证据提取** — 具体数据/统计/案例/引用？记录数字、年份、百分比。
4. **信息分级** — 🔴核心（必须出现） / 🟡支撑（应该包含） / 🟢补充（可选）。

### 阶段三：设计 Deck 结构 (Structure)

- 一张 slide 一个核心信息
- 证据紧随论点
- 覆盖所有🔴核心信息

标准结构 8-14 张。短内容最低 4 张。

**固定序列（不可省略）:**
```
Slide 01: 封面 (Hero Cover)
Slide 02: 内容目录 / Agenda (Overview — 编号列表，概括全部章节)
Slide 03..N-1: 正文内容 (按照理解阶段产出的结构填充)
Slide N: 致谢 / Q&A (谢谢 / 感谢观看)
```

封面下一张必须是全局 Agenda 目录。最后一张必须是致谢页。

### 阶段四：生成 HTML (Generate)

默认使用 Guizang Editorial 设计系统。根据内容气质可选传统 3 色板。

---

## 设计系统 A（默认）：Guizang Editorial E-Ink

纸墨印刷感，衬线 display，适合叙事/观点/技术分享/数据分析。

### 调色板（5 选 1，不可混用，不可改 hex）

内容偏商业/科技/通用 → 默认 **Indigo Porcelain**。按内容气质选择：

| 调色板 | ink | paper | paper-tint | 场景 |
|--------|-----|-------|-----------|------|
| 🖋 **墨水经典 Monocle** | `#0a0a0b` | `#f1efea` | `#e8e5de` | 通用商业/科技 |
| 🌊 **靛蓝瓷 Indigo Porcelain** | `#0a1f3d` | `#f1f3f5` | `#e4e8ec` | 科技/研究/数据 |
| 🌿 **森林墨 Forest Ink** | `#1a2e1f` | `#f5f1e8` | `#ece7da` | 自然/可持续/文化 |
| 🍂 **牛皮纸 Kraft Paper** | `#2a1e13` | `#eedfc7` | `#e0d0b6` | 怀旧/人文/文学 |
| 🌙 **沙丘 Dune** | `#1f1a14` | `#f0e6d2` | `#e3d7bf` | 艺术/设计/时尚 |

ink-tint = ink 加 5% 亮度; mute = `#6b7b8a`。

### 字体栈

- Display（英文）: `'Playfair Display', Georgia, 'Times New Roman', serif`
- Display（中文）: `'Noto Serif SC', 'Source Han Serif SC', serif`
- Body: `Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif`
- 数字/编号: `'Playfair Display'` italic 或 `'JetBrains Mono'`

### 版式池（10 个布局，可复用复用）

- **L01 Hero Cover** — 居中 kicker + 5.5vw 衬线大字 + lead（1.1vw, max-width 55%）+ 底部元数据行
- **L02 Act Divider** — kicker + 5.5vw 超大衬线 headline + 引言；支持 invert 反色变体
- **L03 Big Numbers Grid** — 3×2 卡片：label(0.8vw uppercase) + big num(3.5vw italic 衬线) + desc
- **L04 Quote + Visual** — 左 flex:1 (kicker + 2.2vw 衬线斜引文 + cite) + 右 30% 内联 SVG 图形
- **L05 Image Grid** — 3×2 或 3×1 等高图网格，纯 CSS 色块/SVG 替代外部图
- **L06 Pipeline / Flow** — 横向等宽步骤：No + 标题 + 描述，border-right 分隔
- **L07 Hero Question** — 7vw 居中单一问句，周围极简
- **L08 Big Quote** — kicker + 3.8vw 衬线斜引文 + cite，居中极简
- **L09 Before / After** — 1:1 分割，左半 opacity 0.65 + 右半 full；每侧 label + 衬线标题 + 列表
- **L10 Mixed Media** — 8:4 左文字(kicker + headline + 列表) + 右竖形图形
- **L11 Overview / Agenda** — 编号章节目录，紧接封面之后。左栏标题 "内容概要" / "Agenda"，右栏 4-8 条编号章节名，底部 hairline
- **L12 Closing / 致谢** — 最后一页。居中大字 "谢谢" / "Thank You" / "Q&A"，下方致谢或 "感谢观看"，底部来源链接

### 固定顺序要求

每份 deck 必须包含：
1. **封面** (L01 Hero Cover)
2. **Agenda** (L11 Overview) — 紧接封面
3. **正文** (L02-L10 按需组合)
4. **致谢** (L12 Closing) — 最后一页

### 设计铁律

- **禁止**: 渐变 / drop-shadow / 圆角 / 圆形装饰 / blur / SVG 图标库 / emoji 装饰
- **1px hairline 分隔**: 顶部固定 hairline + topic 标签左上 + folio 右下 `01 / 12`（衬线 italic）
- **16:9** 画幅，**真实数据**，**单文件 HTML**，**无外部图片/字体 CDN**（Playfair Display / Inter 需系统已有）
- 对比度 ≥ 4.5:1

### 导航

←/→ 切换，hash 同步，顶部 2px 进度条，打印 `@media print` 每页一张。

---

## 设计系统 B（备选）：经典 3 色板

当内容不适合纸墨风格时使用。3 选 1：

- **🟦 Slate** — `--ink: #1a1a2e; --paper: #f8f9fa; --paper-tint: #eef0f4; --accent: #4361ee; --accent-soft: #e8ecfb; --mute: #8892a4`
- **🟧 Warm** — `--ink: #2d1f14; --paper: #fdf6ec; --paper-tint: #f5ede0; --accent: #c17f4b; --accent-soft: #f0e2d5; --mute: #9a8a7a`
- **🟩 Forest** — `--ink: #1a2e1f; --paper: #f4f7f2; --paper-tint: #e8ede4; --accent: #2d6a4f; --accent-soft: #ddeee3; --mute: #6b8f72`

字体用系统安全栈（Georgia/serif, -apple-system/sans-serif, JetBrains Mono/monospace），布局同上（Cover → Agenda → 正文 → Closing），硬约束相同。

---

## HTML 骨架（默认 Guizang Editorial）

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>标题</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  html { font-size: 16px; scroll-behavior: smooth; }
  body {
    font-family: Inter, 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    background: var(--paper);
    color: var(--ink);
    overflow: hidden;
    width: 100vw; height: 100vh;
    -webkit-font-smoothing: antialiased;
  }
  :root {
    --ink: #0a1f3d;
    --ink-tint: #152a4a;
    --paper: #f1f3f5;
    --paper-tint: #e4e8ec;
    --mute: #6b7b8a;
  }
  .deck { position: relative; width: 100vw; height: 100vh; overflow: hidden; }
  .slide {
    position: absolute; top: 0; left: 0;
    width: 100%; height: 100%;
    display: flex; flex-direction: column;
    justify-content: center;
    padding: 6.5vh 6.5vw;
    opacity: 0; visibility: hidden;
    transition: opacity 0.3s ease;
  }
  .slide.active { opacity: 1; visibility: visible; position: relative; }
  .progress { position: fixed; top: 0; left: 0; height: 2px; background: var(--ink); transition: width 0.3s ease; opacity: 0.4; z-index: 100; }
  .folio { position: fixed; bottom: 2.5vh; right: 2.5vw; font-size: 0.75vw; color: var(--mute); z-index: 100; font-family: 'Playfair Display', Georgia, serif; font-style: italic; }
  .topic-label { position: fixed; top: 2.5vh; left: 2.5vw; font-size: 0.65vw; text-transform: uppercase; letter-spacing: 0.12em; color: var(--mute); z-index: 100; }
  .hairline-top { position: fixed; top: 4.5vh; left: 2.5vw; right: 2.5vw; height: 1px; background: var(--paper-tint); z-index: 100; }
  .kicker { font-size: 0.7vw; text-transform: uppercase; letter-spacing: 0.12em; color: var(--mute); margin-bottom: 1.5vh; }

  /* L01 */ .layout-cover { text-align: center; justify-content: center; align-items: center; }
  .layout-cover h1 { font-family: 'Playfair Display', 'Noto Serif SC', Georgia, serif; font-size: clamp(2.5rem, 5.5vw, 5.5vw); line-height: 1.15; max-width: 85%; margin: 0 auto; letter-spacing: -0.02em; font-weight: 700; }
  .layout-cover .lead { font-size: clamp(0.85rem, 1.1vw, 1.1rem); color: var(--mute); max-width: 55%; margin: 1.5vh auto 0; line-height: 1.6; }

  /* L02 */ .layout-divider { text-align: center; justify-content: center; align-items: center; }
  .layout-divider h2 { font-family: 'Playfair Display', 'Noto Serif SC', Georgia, serif; font-size: clamp(2rem, 5.5vw, 5.5vw); line-height: 1.15; max-width: 75%; margin: 0 auto 1.5vh; font-weight: 700; }
  .layout-divider .sub-quote { font-size: clamp(0.85rem, 1.2vw, 1.2rem); color: var(--mute); font-style: italic; }
  .layout-divider.invert { background: var(--ink); color: var(--paper); }

  /* L03 */ .layout-grid .grid-3x2 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5vw; }
  .layout-grid .grid-card .big-num { font-size: clamp(1.8rem, 3.5vw, 3.5vw); font-weight: 700; font-family: 'Playfair Display', Georgia, serif; font-style: italic; }

  /* L04 */ .layout-quote-visual { flex-direction: row; align-items: center; gap: 4vw; }
  .layout-quote-visual .left blockquote { font-family: 'Playfair Display', 'Noto Serif SC', Georgia, serif; font-size: clamp(1rem, 2.2vw, 2.2vw); line-height: 1.4; font-style: italic; }
  .layout-quote-visual .right { flex: 0 0 30%; height: 45vh; background: var(--paper-tint); display: flex; align-items: center; justify-content: center; }

  /* L06 */ .layout-pipeline .steps { display: flex; }
  .layout-pipeline .step { flex: 1; padding: 2vh 1.2vw; border-right: 1px solid var(--paper-tint); }
  .layout-pipeline .step .step-num { font-family: 'Playfair Display', Georgia, serif; font-size: clamp(0.9rem, 1.2vw, 1.2vw); font-style: italic; color: var(--mute); }

  /* L08 */ .layout-bigquote { text-align: center; justify-content: center; align-items: center; }
  .layout-bigquote blockquote { font-family: 'Playfair Display', 'Noto Serif SC', Georgia, serif; font-size: clamp(1.3rem, 3.8vw, 3.8vw); line-height: 1.3; max-width: 80%; font-style: italic; }

  /* L09 */ .layout-beforeafter { flex-direction: row; align-items: stretch; gap: 0; padding: 0; }
  .layout-beforeafter .half { flex: 1; display: flex; flex-direction: column; justify-content: center; padding: 6.5vh 4vw; }
  .layout-beforeafter .half.before { background: var(--paper-tint); opacity: 0.65; }
  .layout-beforeafter .half.after { background: var(--paper); }

  /* L10 */ .layout-mixed { flex-direction: row; align-items: center; gap: 3vw; }
  .layout-mixed .left { flex: 8; }
  .layout-mixed .right { flex: 4; height: 40vh; background: var(--paper-tint); display: flex; align-items: center; justify-content: center; }

  /* L11 Agenda */ .layout-agenda { justify-content: center; }
  .layout-agenda h2 { font-family: 'Playfair Display', 'Noto Serif SC', Georgia, serif; font-size: clamp(1.2rem, 2vw, 2vw); margin-bottom: 3vh; }
  .layout-agenda .agenda-list { list-style: none; display: flex; flex-direction: column; gap: 1.2vh; }
  .layout-agenda .agenda-list li { font-size: clamp(0.85rem, 1.2vw, 1.2rem); line-height: 1.5; color: var(--ink-tint); padding-left: 2.5vw; position: relative; }
  .layout-agenda .agenda-list li::before { content: attr(data-num); position: absolute; left: 0; font-family: 'Playfair Display', Georgia, serif; font-style: italic; color: var(--mute); font-size: clamp(0.7rem, 0.9vw, 0.9rem); }

  /* L12 Closing */ .layout-closing { text-align: center; justify-content: center; align-items: center; }
  .layout-closing h1 { font-family: 'Playfair Display', 'Noto Serif SC', Georgia, serif; font-size: clamp(2.5rem, 5vw, 5vw); line-height: 1.2; margin-bottom: 1.5vh; }
  .layout-closing .thanks { font-size: clamp(0.9rem, 1.3vw, 1.3rem); color: var(--ink-tint); }
  .layout-closing .qa { font-size: clamp(0.75rem, 1vw, 1rem); color: var(--mute); font-style: italic; margin-top: 2vh; }
  .layout-closing .source-link { font-size: clamp(0.65rem, 0.8vw, 0.8rem); color: var(--mute); margin-top: 3vh; }

  @media print {
    @page { size: 1920px 1080px; margin: 0; }
    body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .slide { position: relative; opacity: 1; visibility: visible; page-break-after: always; height: 1080px; width: 1920px; }
    .progress, .folio, .topic-label, .hairline-top { display: none; }
  }
</style>
</head>
<body>
<div class="deck" id="deck">
  <!-- slides -->
</div>
<script>
(function() {
  const slides = document.querySelectorAll('.slide');
  const total = slides.length;
  let current = parseInt(location.hash.slice(1)) || 0;
  function goTo(n) {
    slides.forEach(s => s.classList.remove('active'));
    current = Math.max(0, Math.min(n, total - 1));
    slides[current].classList.add('active');
    location.hash = '#' + current;
    document.querySelector('.progress').style.width = ((current + 1) / total * 100) + '%';
    document.querySelector('.folio').textContent = String(current + 1).padStart(2, '0') + ' / ' + String(total).padStart(2, '0');
  }
  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') { e.preventDefault(); goTo(current + 1); }
    if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); goTo(current - 1); }
  });
  window.addEventListener('hashchange', () => goTo(parseInt(location.hash.slice(1)) || 0));
  goTo(0);
})();
</script>
</body>
</html>
```

### Debug 清单

- [ ] 所有数据来自用户材料（无捏造）
- [ ] 🔴 核心信息全部覆盖
- [ ] 证据紧跟在论点之后
- [ ] 封面→Agenda→正文→致谢 固定序列正确
- [ ] Agenda 页概括了全部正文章节
- [ ] 调色板统一（唯一 palette，没有混用）
- [ ] 符合所选设计系统的铁律
- [ ] 键盘 ←/→ 可导航，页码正确
- [ ] 打印时每页一张 slide
- [ ] 无外部资源引用
- [ ] 封面信息正确反映原文

## 输出

单文件 HTML，文件名 `<英文slug>-deck.html`。告知用户 slide 数、调色板、来源、←/→ 导航。
