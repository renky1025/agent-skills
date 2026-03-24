---
name: infocard
description: "从 URL 提取内容，生成可定制样式的信息卡片图片。智能分析内容结构，动态选择最适合的布局形式（列表、代码块、卡片网格、时间轴等）。使用方法: /infocard <URL> [--theme=green|blue|purple|orange|pink|dark] [--width=1080]"
user_invocable: true
version: "2.0.0"
---

# infocard: 信息卡片铸造器

将任意 URL 内容转化为精美的信息卡片图片。**核心能力：智能分析内容类型，动态选择最适合的视觉呈现方式**。

## 核心设计理念

**内容驱动布局** —— 不是套用固定模板，而是：
1. 分析内容本质（痛点/步骤/对比/列表/代码）
2. 提取核心信息密度（稀疏/中等/密集）
3. 选择最适合的视觉结构
4. 生成匹配的 HTML 布局

## 使用方法

```
/infocard <URL> [--theme=<theme>] [--width=<width>] [--output=<name>]
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `URL` | 要抓取的网页链接 | 必填 |
| `--theme` | 配色主题: `green`, `blue`, `purple`, `orange`, `pink`, `dark` | `green` |
| `--width` | 图片宽度 | `1080` |
| `--output` | 输出文件名（不含扩展名） | 自动提取 |

## 主题配色

### green（默认）
适合：科技、开源、产品发布
```
--bg: #F8FAF9
--accent: #22C55E
--accent-light: #86EFAC
--dark-card: #1F2937
```

### blue
适合：商业、金融、专业报告
```
--bg: #F0F7FF
--accent: #3B82F6
--accent-light: #93C5FD
--dark-card: #1E3A5F
```

### purple
适合：创意、设计、艺术
```
--bg: #FAF5FF
--accent: #A855F7
--accent-light: #D8B4FE
--dark-card: #3B0764
```

### orange
适合：运营、增长、营销活动
```
--bg: #FFF7ED
--accent: #F97316
--accent-light: #FDBA74
--dark-card: #7C2D12
```

### pink
适合：生活方式、时尚、社媒内容
```
--bg: #FDF2F8
--accent: #EC4899
--accent-light: #F9A8D4
--dark-card: #831843
```

### dark
适合：深色主题、夜间模式
```
--bg: #1F2937
--accent: #10B981
--accent-light: #34D399
--dark-card: #111827
```

## 执行步骤

### 步骤 1: 内容抓取与分析

使用 agent-reach 或 WebFetch 获取内容：

```bash
agent-reach read <URL> --json
```

### 步骤 2: 内容解构（关键）

分析内容并提取以下维度：

#### 2.1 内容类型识别

| 内容特征 | 对应布局 | 使用场景 |
|---------|---------|---------|
| 多个痛点/问题 | **列表布局** | 产品痛点、用户问题 |
| 步骤/流程 | **代码块/编号列表** | 安装步骤、使用教程 |
| 多个并列特性 | **卡片网格** | 功能特性、集成方式 |
| 层级架构 | **层级缩进** | 系统架构、组件关系 |
| 对比/选择 | **左右对比** | 方案对比、优缺点 |
| 时间线 | **时间轴** | 更新日志、里程碑 |
| 引用/金句 | **引述块** | 核心观点、总结 |

#### 2.2 信息密度判断

| 密度 | 特征 | 布局策略 |
|------|------|---------|
| **稀疏** | 内容少，每点简短 | 单栏大字体，大量留白 |
| **中等** | 4-6个要点，有详有略 | 双栏网格，错落分布 |
| **密集** | 信息量大，细节多 | 紧凑排版，多层级，小字号 |

#### 2.3 输出分析结果

```
内容类型：[痛点列表/步骤教程/功能特性/架构说明/方案对比/其他]
信息密度：[稀疏/中等/密集]
建议分栏数：[2栏/3栏/4栏/混合]
特殊元素：[代码块/数据指标/引用/对比表]
```

### 步骤 3: 动态布局选择

根据分析结果，从以下布局模式中组合：

#### 布局 A: 列表型（适合痛点、特性）
```
┌─────────────────────────┐
│ 1 解决的核心痛点         │
│ ┌─────────────────────┐ │
│ │ ● 痛点1：一句话描述  │ │
│ │ ● 痛点2：一句话描述  │ │
│ │ ● 痛点3：一句话描述  │ │
│ │ ● 痛点4：一句话描述  │ │
│ └─────────────────────┘ │
└─────────────────────────┘
```

#### 布局 B: 带标签卡片（适合设计亮点、架构）
```
┌─────────────────────────┐
│ 2 关键设计亮点           │
│ ┌─────────────────────┐ │
│ │ [数据库]            │ │
│ │ 基于 TiDB Cloud...  │ │
│ └─────────────────────┘ │
│ ┌─────────────────────┐ │
│ │ [架构]              │ │
│ │ 无状态架构，支持... │ │
│ └─────────────────────┘ │
└─────────────────────────┘
```

#### 布局 C: 代码块（适合安装、配置）
```
┌─────────────────────────┐
│ 3 极简安装体验           │
│ ┌─────────────────────┐ │
│ │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │ │
│ │ # 1. 获取 API Key   │ │
│ │ curl -X POST ...    │ │
│ │                     │ │
│ │ # 2. 安装插件       │ │
│ │ npm install ...     │ │
│ └─────────────────────┘ │
└─────────────────────────┘
```

#### 布局 D: 2x2 网格（适合集成方式、功能矩阵）
```
┌─────────────────────────┐
│ 4 多生态集成方式         │
│ ┌──────────┬──────────┐ │
│ │ [A]      │ [B]      │ │
│ │ 描述...  │ 描述...  │ │
│ ├──────────┼──────────┤ │
│ │ [C]      │ [D]      │ │
│ │ 描述...  │ 描述...  │ │
│ └──────────┴──────────┘ │
└─────────────────────────┘
```

#### 布局 E: 对比型（适合方案对比）
```
┌─────────────────────────┐
│ 方案对比                │
│ ┌──────────┬──────────┐ │
│ │ 方案A    │ 方案B    │ │
│ │ ● 优点   │ ● 优点   │ │
│ │ ● 缺点   │ ● 缺点   │ │
│ └──────────┴──────────┘ │
└─────────────────────────┘
```

### 步骤 4: 内容提取原则

#### 4.1 标题提取
- 提取文章主标题（≤ 20 字）
- 副标题：一句话核心观点（≤ 30 字）
- 栏目标题：从内容中提炼，不是固定格式

#### 4.2 内容精炼
- **痛点**：每点 1 句话，突出核心问题
- **特性**：标题 + 一句话描述
- **步骤**：编号 + 命令/操作 + 简要说明
- **数据**：突出数字，带上下文

#### 4.3 自适应分栏
- 内容少 → 2 栏，每栏内容充实
- 内容多 → 3-4 栏，或 2 栏 + 底部扩展
- 代码/长内容 → 单独一栏，占满宽度

### 步骤 5: 生成 HTML

#### Header 区域（根据内容调整）
```html
<!-- 有数据指标时 -->
<header class="header">
  <div class="header-left">
    <div class="header-tag">分类标签</div>
    <h1 class="header-title">主标题</h1>
    <p class="header-subtitle">副标题</p>
  </div>
  <div class="header-right">
    <div class="stat-card">
      <div class="stat-number">数字</div>
      <div class="stat-label">标签</div>
    </div>
  </div>
</header>

<!-- 无数据指标时 -->
<header class="header-simple">
  <div class="header-tag">分类标签</div>
  <h1 class="header-title">主标题</h1>
  <p class="header-subtitle">副标题</p>
</header>
```

#### 内容区域（根据布局选择）

**列表布局：**
```html
<div class="section-card">
  <div class="section-header">
    <span class="section-number">1</span>
    <span class="section-title">痛点/问题</span>
  </div>
  <ul class="bullet-list">
    <li><strong>痛点1：</strong>一句话描述</li>
    <li><strong>痛点2：</strong>一句话描述</li>
  </ul>
</div>
```

**带标签卡片：**
```html
<div class="section-card">
  <div class="section-header">
    <span class="section-number">2</span>
    <span class="section-title">设计亮点</span>
  </div>
  <div class="feature-card" style="border-left-color: #3B82F6;">
    <span class="feature-tag" style="background: #3B82F6;">数据库</span>
    <div class="feature-title">基于 TiDB Cloud</div>
    <div class="feature-desc">描述文本...</div>
  </div>
</div>
```

**代码块：**
```html
<div class="section-card full-width">
  <div class="section-header">
    <span class="section-number">3</span>
    <span class="section-title">安装步骤</span>
  </div>
  <div class="code-block">
    <div class="code-line"><span class="code-comment"># 1. 获取 API Key</span></div>
    <div class="code-line">curl -X POST https://api...</div>
  </div>
</div>
```

**2x2 网格：**
```html
<div class="section-card">
  <div class="section-header">
    <span class="section-number">4</span>
    <span class="section-title">集成方式</span>
  </div>
  <div class="grid-2x2">
    <div class="grid-item">
      <span class="grid-tag">Claude Code</span>
      <p>描述文本...</p>
    </div>
    <div class="grid-item">
      <span class="grid-tag">OpenClaw</span>
      <p>描述文本...</p>
    </div>
    <!-- 更多... -->
  </div>
</div>
```

### 步骤 6: 截图生成

```bash
node ~/.claude/skills/infocard/assets/capture.js /tmp/infocard_{name}.html ~/Downloads/{name}.png 1080 800 fullpage
```

## 布局决策树

```
开始
  │
  ├─ 内容是否包含步骤/命令？
  │   └─ 是 → 使用代码块布局
  │
  ├─ 内容是否为多个并列特性？
  │   ├─ 数量 ≤ 4 → 使用 2x2 网格
  │   └─ 数量 > 4 → 使用标签卡片列表
  │
  ├─ 内容是否为问题/痛点？
  │   └─ 是 → 使用 bullet 列表
  │
  ├─ 内容是否为对比？
  │   └─ 是 → 使用左右对比布局
  │
  └─ 其他 → 使用文本卡片，灵活调整
```

## 示例对比

### 示例 1：产品功能介绍（2x2 网格）
```
┌─────────────────────────────────────┐
│ Mem9: OpenClaw 的云端持久记忆层      │
├───────────────┬─────────────────────┤
│ 1 解决的核心   │ 2 极简安装体验       │
│   痛点         │                     │
│ ● 重启失忆    │ ┌─────────────────┐ │
│ ● 换机重建    │ │ # 获取 API Key  │ │
│ ● 文件易丢    │ │ curl -X POST... │ │
│ ● 知识孤岛    │ └─────────────────┘ │
├───────────────┼─────────────────────┤
│ 3 关键设计     │ 4 多生态集成         │
│   亮点         │                     │
│ [DB] TiDB... │ [Claude] [OpenClaw] │
│ [架构] 无状态 │ [OpenCode] [REST]   │
└───────────────┴─────────────────────┘
```

### 示例 2：技术架构说明（层级布局）
```
┌─────────────────────────────────────┐
│ Claude .claude/ 文件夹完全指南       │
├─────────────────────────────────────┤
│ 1 CLAUDE.md（核心）                  │
│    加载到系统 prompt，全程保持       │
├─────────────────────────────────────┤
│ 2 Commands vs Skills                 │
│    Commands: 手动触发 /command       │
│    Skills: 自动识别触发              │
├─────────────────────────────────────┤
│ 3 Agents & Settings                  │
│    子代理配置 + 权限控制             │
└─────────────────────────────────────┘
```

### 示例 3：教程步骤（垂直流程）
```
┌─────────────────────────────────────┐
│ 5 分钟入门指南                       │
├─────────────────────────────────────┤
│ 步骤 1：安装                         │
│ $ npm install package                │
├─────────────────────────────────────┤
│ 步骤 2：配置                         │
│ 编辑 config.json                     │
├─────────────────────────────────────┤
│ 步骤 3：运行                         │
│ $ npm start                          │
└─────────────────────────────────────┘
```

## CSS 工具类参考

```css
/* 布局 */
.content-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.content-grid-3 { grid-template-columns: 1fr 1fr 1fr; }
.full-width { grid-column: 1 / -1; }

/* 列表 */
.bullet-list { list-style: none; padding: 0; }
.bullet-list li { padding: 8px 0; padding-left: 20px; position: relative; }
.bullet-list li::before { content: "●"; position: absolute; left: 0; color: var(--accent); }

/* 代码块 */
.code-block { background: #1E293B; color: #E2E8F0; padding: 16px; border-radius: 8px; font-family: monospace; }
.code-comment { color: #64748B; }

/* 网格 */
.grid-2x2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.grid-item { background: var(--bg); padding: 16px; border-radius: 8px; }
.grid-tag { font-size: 12px; font-weight: 600; color: var(--accent); }

/* 带标签卡片 */
.feature-card { border-left: 4px solid; padding: 16px; background: var(--bg); border-radius: 0 8px 8px 0; margin-bottom: 12px; }
.feature-tag { display: inline-block; padding: 4px 10px; border-radius: 4px; color: white; font-size: 11px; font-weight: 600; margin-bottom: 8px; }
```

## 注意事项

1. **内容优先** — 永远先分析内容，再选布局，不要反过来
2. **灵活分栏** — 2-4 栏都可以，根据内容多少决定
3. **避免拥挤** — 密集的代码/长文本单独一栏
4. **视觉节奏** — 长短结合，避免所有栏目高度相同
5. **字体层级** — 标题 18px，正文 14-15px，代码 13px
6. **颜色克制** — 标签/强调色最多 3 种，保持统一
