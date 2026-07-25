---
name: glass-cover
description: "玻璃风格封面/卡片图片生成。输入主题文案，生成具有磨砂玻璃、透明层次、光影折射等玻璃质感的封面图或信息卡片。使用方法：/glass-cover <主题文案> [--mode=cover|card] [--style=frosted|crystal|neon|liquid] [--size=1024x1536]"
user_invocable: true
version: "1.0.0"
---

# glass-cover: 玻璃风格封面生成器

输入一段主题文案，生成具有玻璃质感（Glassmorphism���的封面图或信息卡片。核心思路借鉴文章「麦肯锡风格提示词」的双模式设计，将视觉风格替换为玻璃美学。

## Outcome Contract

- **Outcome**：基于用户输入的主题文案，生成一张具有玻璃质感的封面图或信息卡片
- **Done when**：图片已通过 ImageGen 生成并保存到指定目录，用户可查看
- **Evidence**：生成的图片包含明确的玻璃质感视觉元素（磨砂面板、透明层次、折射光效、柔和渐变背景）

## Hard Rules｜硬边界

- 封面模式必须强调简洁、留白、核心词突出，不以信息密度取胜
- 卡片模式必须保持结构清晰、层次分明，不因玻璃效果牺牲可读性
- 所有提示词必须包含玻璃质感的关键视觉元素（frosted glass, translucent, refraction, soft blur）
- 中文内容必须使用中文排版提示词（如"中文排版"、"汉字"），避免生成乱码或英文占位符
- 背景色系以冷色调为主（蓝、青、紫、灰），不适用暖色调破坏玻璃的冷感美学

## 使用方法

```
/glass-cover <主题文案> [--mode=<模式>] [--style=<风格>] [--size=<尺寸>] [--output=<名称>]
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<主题文案>` | 封面要展示的核心文案（标题/主题），支持多行用引号包裹 | 必填 |
| `--mode` | 生成模式：`cover`(封面)、`card`(信息卡片) | `cover` |
| `--style` | 玻璃风格：`frosted`(磨砂)、`crystal`(水晶)、`neon`(霓虹玻璃)、`liquid`(流体玻璃) | `frosted` |
| `--size` | 图片尺寸：`1024x1024`、`1024x1536`(竖版)、`1536x1024`(横版) | `1024x1536` |
| `--output` | 输出文件名（不含扩展名） | 自动从主题提取 |

### 输出规则

- 默认保存目录：`~/Downloads/glass-cover/`
- 文件名：`{output}.png`（自动加序号避免覆盖）
- 输出目录自动创建

## 两种模式（借鉴文章的双模式设计）

### 封面模式 (cover)

适用场景：X/Twitter 封面、公众号封面、播客封面、海报封面

**视觉原则**：
- **简洁至上**：画面以 1-2 个核心视觉元素为主，大量留白
- **核心词突出**：标题文字是视觉锚点，占据画面重心
- **玻璃隐喻**：主文字放在磨砂玻璃面板上，如透过冰层看到的文字
- **留白 ≥ 50%**：让玻璃的透明质感有呼吸空间

**提示词构建逻辑**：
1. 先定义玻璃质感主体（frosted glass panel, crystal object, glass prism）
2. 再确定文字排版位置和风格
3. 最后添加光效和环境氛围（soft lighting, refraction, bokeh）

### 卡片模式 (card)

适用场景：信息图、知识卡片、社交分享图、产品特性图

**视觉原则**：
- **层次分明**：多个玻璃面板分层叠加，形成深度感
- **模块化布局**：不同信息区块用不同透明度的玻璃卡片承载
- **引导阅读路径**：通过光影和层次引导视线
- **留白 30-40%**：信息密度适中，玻璃效果增加呼吸感

**提示词构建逻辑**：
1. 先构建多层玻璃面板的布局结构
2. 再分配每个面板的内容和层级关系
3. 最后统一光效、折射、阴影方向

## 四种玻璃风格

### frosted（磨砂玻璃）

经典 Glassmorphism 风格。磨砂半透明面板，柔和的背光模糊效果，细腻的白色边框。

**视觉特征**：半透明白色/浅色面板、背景模糊、微妙的阴影深度
**色彩倾向**：冷白、冰蓝、浅灰
**适用**：正式场合、技术主题、品牌封面

### crystal（水晶玻璃）

高透明度的水晶质感。清晰的光线折射，棱镜色散效果，晶莹剔透。

**视觉特征**：高透明度、彩虹色折射、锐利边缘光泽
**色彩倾向**：透明底 + 彩虹折射、淡蓝紫光晕
**适用**：创意主题、艺术作品、奢侈品

### neon（霓虹玻璃）

暗色背景 + 霓虹光透过玻璃的赛博朋克感。

**视觉特征**：深色背景、霓虹灯般的光线穿透玻璃边缘、发光文字
**色彩倾向**：暗黑底 + 品红/青色霓虹光
**适用**：科技主题、游戏、夜间场景

### liquid（流体玻璃）

熔融玻璃、液态流动感。有机曲线，粘稠透明质感。

**视觉特征**：流动的玻璃形态、有机曲线、粘稠高光
**色彩倾向**：琥珀色、翡翠绿、透明蓝
**适用**：艺术表达、抽象概念、创意展示

## 执行步骤

### 第一步：解析输入

1. 提取主题文案（必填）
2. 提取可选参数（mode, style, size, output）
3. 如果主题过长（> 50 字），自动建议使用 `card` 模式
4. 如果未指定 output，从主题前 20 字提取（去除标点）

### 第二步：输出设计决策

在进行提示词构建前，先明确设计方向：

```
模式：[cover / card]
风格：[frosted / crystal / neon / liquid]
尺寸：[用户指定或默认]
色彩方案：[根据风格确定主色和辅助色]
核心隐喻：[用什么玻璃物体承载主题——面板/棱镜/球体/流体]
```

### 第三步：构建 ImageGen 提示词

根据模式和风格，从以下提示词模块中选取并组装。

#### 3.1 通用底座（所有提示词的前置描述）

```
high quality, 4K, professional photography style, glassmorphism design,
```

#### 3.2 模式专属提示词

**封面模式 (cover) 底座**：

```
minimalist cover design, centered composition, large negative space,
a single dominant frosted glass panel floating in the center,
the panel contains clean bold typography of the title,
surrounded by empty space with subtle light effects,
no cluttered elements, editorial layout,
```

**卡片模式 (card) 底座**：

```
multi-layered card layout, cascading frosted glass panels,
each panel at different depth levels with varying opacity,
soft shadows creating depth separation between layers,
structured information hierarchy, clean modular design,
```

#### 3.3 风格专属提示词

**frosted（磨砂玻璃）**：

```
frosted glass texture, semi-transparent white panel with backdrop blur effect,
subtle white border rim light around glass edges,
soft diffused lighting, gentle shadow depth,
cool color palette with ice blue and silver tones,
clean environment with soft gradient background from light blue to pale gray,
```

**crystal（水晶玻璃）**：

```
crystal clear glass object, high transparency with prismatic light refraction,
rainbow caustics and spectral highlights on glass surface,
sharp specular reflections on edges, diamond-like clarity,
bright light passing through creating colorful light dispersion,
pure white to subtle blue gradient background,
```

**neon（霓虹玻璃）**：

```
dark moody background, frosted glass panel illuminated by neon light from edges,
cyan and magenta neon glow bleeding through the glass borders,
cyberpunk aesthetic, glass edge lit by colored light,
dark gradient background from deep navy to black,
glass surface reflecting faint colorful light streaks,
```

**liquid（流体玻璃）**：

```
molten liquid glass with organic flowing curves,
viscous transparent material with thick glossy highlights,
smooth fluid shapes resembling melted crystal,
amber and emerald green tinted glass with internal light refraction,
soft studio lighting creating volumetric glow through the liquid glass,
minimal clean background to emphasize the glass form,
```

#### 3.4 中文文字处理提示词

这是关键模块——确保 ImageGen 正确渲染中文：

```
Chinese text "具体文案" rendered clearly on the glass surface,
clean sans-serif Chinese typography, bold weight for title,
the Chinese characters must be legible and correctly formed,
typography as visual anchor, large scale title text,
```

**重要**：`"具体文案"` 必须替换为用户输入的实际文案。如果文案较长，分为主标题（大字）和副标题（小字）两部分描述。

#### 3.5 氛围光效（末尾统一添加）

```
soft ambient lighting, subtle bokeh effects in background,
premium high-end aesthetic, 8K resolution, photorealistic rendering
```

### 第四步：调用 ImageGen 生成

组装完成后，调用 ImageGen：

```json
{
  "prompt": "<组装后的完整提示词>",
  "size": "<用户指定尺寸>",
  "quality": "high",
  "output_dir": "~/Downloads/glass-cover"
}
```

**提示词总长度控制**：
- 封面模式：控制在 300-500 字符
- 卡片模式：控制在 400-600 字符
- 避免过度描述导致画面混乱

### 第五步：展示结果

使用 `present_files` 展示生成的图片，同时输出：

```
✅ 玻璃风格封面已生成
模式：{mode} | 风格：{style}
文件：{输出路径}
```

## 提示词示例

### 示例 1：封面模式 + 磨砂玻璃

**输入**：`/glass-cover "AI 时代的个人知识管理" --mode=cover --style=frosted`

**组装后提示词**：

```
high quality, 4K, professional photography style, glassmorphism design,
minimalist cover design, centered composition, large negative space,
a single dominant frosted glass panel floating in the center,
Chinese text "AI 时代的个人知识管理" rendered clearly on the glass surface,
clean sans-serif Chinese typography, bold weight for title,
the Chinese characters must be legible and correctly formed,
frosted glass texture, semi-transparent white panel with backdrop blur effect,
subtle white border rim light around glass edges,
soft diffused lighting, gentle shadow depth,
cool color palette with ice blue and silver tones,
clean environment with soft gradient background from light blue to pale gray,
soft ambient lighting, subtle bokeh effects in background,
premium high-end aesthetic, 8K resolution, photorealistic rendering
```

### 示例 2：卡片模式 + 水晶玻璃

**输入**：`/glass-cover "三步搭建 AI 工作流\n1. 定义目标\n2. 连接工具\n3. 自动化执行" --mode=card --style=crystal`

**组装后提示词**：

```
high quality, 4K, professional photography style, glassmorphism design,
multi-layered card layout, cascading crystal glass panels,
each panel at different depth levels with varying transparency,
Chinese text "三步搭建 AI 工作流" as main title on the topmost glass panel,
three smaller glass cards below showing steps "定义目标" "连接工具" "自动化执行",
clean sans-serif Chinese typography, the characters must be legible,
crystal clear glass object, high transparency with prismatic light refraction,
rainbow caustics and spectral highlights on glass surface,
sharp specular reflections on edges, diamond-like clarity,
pure white to subtle blue gradient background,
structured information hierarchy, clean modular design,
soft shadows creating depth separation between layers,
soft ambient lighting, subtle bokeh effects, 8K photorealistic
```

## 注意事项

1. **中文渲染是最大风险点** — ImageGen 对中文字符的渲染不稳定，提示词中必须强调 "Chinese text"、"Chinese characters must be legible and correctly formed"，且文案中不能有生僻字或过长文本
2. **控制文字量** — 封面模式文字 ≤ 20 字，卡片模式每个面板文字 ≤ 10 字，超出部分会被渲染成乱码或占位符
3. **一个核心隐喻** — 每张图只用一个玻璃物体作为主角（面板/棱镜/球体/流体），多物体容易导致画面混乱
4. **冷色调优先** — 玻璃美学的核心是"冷感"，避免添加暖色元素（除非用户明确要求）
5. **credit 提醒** — 每次调用 ImageGen 消耗约 5-10 credits，在生成前告知用户
6. **生成结果不确定** — AI 图像生成具有随机性，不满意可重新生成（相同提示词可能产出不同结果）
7. **两种模式的选择** — 纯标题选 cover，包含结构化内容（步骤、列表、对比）选 card

## Gotchas｜踩过的坑

| 踩过的坑 | 规则 |
|---|---|
| 中文文字被渲染成乱码或英文占位符 | 提示词中必须加入 "Chinese text" 前缀 + "legible and correctly formed" 约束；文案控制在 20 字以内 |
| 玻璃效果不明显，看起来像普通卡片 | 必须同时包含 frosted glass + backdrop blur + rim light 三个关键词；缺一不可 |
| 卡片模式文字过多导致画面拥挤 | 卡片模式每个面板文字 ≤ 10 字，多出的内容不要强行放入 |
| 霓虹风格玻璃面板不可见 | neon 风格必须在提示词中明确 "glass panel illuminated by neon light from edges"，否则玻璃质感丢失 |
| 封面模式留白不够 | 封面提示词中必须包含 "large negative space" + "no cluttered elements" |

---

## 参考来源

- 设计理念借鉴自 Adrain Punk 的「麦肯锡风格提示词」X Article（推文 ID: 2062080784572534958）中的双模式（封面/信息图）设计思路
- 玻璃质感视觉语言参考 Glassmorphism 设计趋势（Apple Vision Pro / macOS 风格）
