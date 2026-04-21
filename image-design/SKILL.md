---
name: image-design
description: 高级质感图片设计 —— 基于摄影逻辑的 AI 图片提示词生成技能。当用户需要生成图片、写提示词、或讨论 AI 图片质量时激活此技能。通过主体描述、构图位置、光线逻辑、相机视角、风格与质感五大模块，生成专业级 AI 绘图提示词。适用于 GPT-image2、nanobanana、Midjourney、Stable Diffusion 等 AI 绘图工具。
---

# 高级质感图片设计

帮助用户生成专业级的 AI 图片提示词，遵循摄影学五大核心维度。

## 核心公式

```
[主体描述] + [构图位置] + [光线逻辑] + [相机视角] + [风格与质感]
```

每一张高质量 AI 图片的提示词都应覆盖这五个维度。

---

## 一、主体描述 + 构图位置

### 位置提示词

| 场景需求 | 提示词 |
|---------|--------|
| 主体偏左 | `positioned at left one-third of the frame` |
| 主体偏右 | `subject at right one-third of the frame` |
| 主体偏上 | `subject placed at top one-third of the frame` |
| 主体偏下 | `subject positioned near bottom third` |

### 平衡元素写法

| 用法 | 提示词 | 效果 |
|------|--------|------|
| 光平衡 | `balanced composition through contrast between light and shadow` | 明暗平衡 |
| 物体平衡 | `counterbalanced by small object on the opposite side` | 物体对重 |
| 色彩平衡 | `asymmetrical balance through warm and cool tones` | 色彩平衡 |
| 结构平衡 | `balanced by architectural elements in background` | 结构支撑画面 |

### 动线写法

| 类型 | 提示词 | 效果 |
|------|--------|------|
| 道路动线 | `leading lines from foreground toward the subject` | 从前景引导视线进入画面 |
| 光线动线 | `diagonal light from top-right guiding viewer's eye` | 用光的方向引导视线 |
| 透视动线 | `path leading into depth, vanishing perspective` | 增强空间深度 |
| 目光动线 | `subject looking toward distant light` | 人物目光带出画外空间 |

### 构图模板

```
[主体], positioned at [left/right/top/bottom] one-third of the frame,
[leading lines / light direction] guiding toward the subject,
[balance element description],
[lighting style],
[environment],
--ar [aspect_ratio]
```

---

## 二、光线逻辑

**三角公式：光线 = 方向 × 光比 × 色温**

### 1. 方向：光从哪来、打在哪、造成什么结果

三要素：**方向**（from right）、**照射对象**（subject's face）、**阴影结果**（long shadows）

正确写法示例：
> `soft sunlight entering from the right window, lighting the subject's face, casting long shadows on the table`

#### 主光与辅光

```
(subject), lit by warm key light from the right, soft fill light from the left, creating balanced shadows
```

### 2. 光比：控制画面的深度与视觉节奏

AI 模型倾向于"亮度平均"，必须明确告诉 AI：哪里是亮面、哪里是暗面、亮暗之间是突变还是渐变。

示例：
> `a man standing under a streetlight, face illuminated brightly, background fading into shadow, strong contrast ratio, smooth light falloff`

### 3. 色温：光的情绪与时间逻辑

错误：`warm lighting`（整张图偏橙，像套滤镜）

正确：`warm sunlight hitting the character's face, cool blue ambient light in the background`（建立冷暖对比，分出层次）

#### 色温与时间段

| 时间 | 色温趋势 | 情绪表现 | 提示词参考 |
|------|---------|---------|-----------|
| 清晨 | 偏冷 | 宁静、朦胧 | `misty morning light, cool tone` |
| 正午 | 中性 | 清晰、真实 | `neutral daylight` |
| 傍晚 | 偏暖 | 柔和、浪漫 | `golden hour sunlight` |
| 夜晚 | 冷暖混合 | 孤独、都市感 | `warm lamp light, cool ambient shadow` |

### 光线综合示例

```
a woman standing near a window,
lit by warm sunlight entering from the right,
soft highlight on her face, background in cool shadow,
medium contrast lighting ratio, smooth gradient light transition
```

> 描述光的**逻辑**，而不是光的**形容词**。

---

## 三、相机视角

### 3 种角度

| 角度 | 画面感觉 | 什么时候用 | 提示词 |
|------|---------|-----------|--------|
| 平视 (Eye-level) | 自然、真实、纪实感强 | 想让画面可信度高 | `eye-level angle, camera positioned at human eye height, natural perspective, realistic proportions` |
| 低角度仰视 (Low Angle) | 主体巨大、有力量、史诗感 | 想让画面更高级、更商业化 | `low-angle shot, camera positioned near ground level, slight upward perspective, monumental feeling` |
| 高角度俯视 (High Angle) | 戏剧、视觉张力强 | 想做艺术风格，想展示更多信息 | `high-angle shot, overhead view, dramatic top-down perspective, strong visual tension` |

### 镜头焦段（Focal Length）

| 焦段 | 特点 | 提示词 |
|------|------|--------|
| 广角 24-35mm | 空间感强、电影感十足 | `35mm lens photography, wide perspective, cinematic street style` |
| 标准 50mm | 最接近人眼、最真实 | `50mm lens, natural field of view, realistic proportions` |
| 中长焦 85mm | 人像神器、背景虚化柔美 | `85mm portrait lens, shallow depth of field, soft bokeh background` |
| 超广角/鱼眼 | 强烈视觉冲击 | `fisheye lens, exaggerated perspective, bold visual impact` |

### 黄金组合公式

| 目标 | 组合 |
|------|------|
| 最自然真实的纪实照片 | eye-level angle + 35mm lens + f2.8 |
| 最高级的人像广告 | low-angle shot + 85mm lens + f1.8 |
| 最电影的环境人像 | eye-level shot + 35mm lens + f2.8 + cinematic depth |
| 最戏剧的艺术风格 | high-angle shot + 50mm lens + f5.6 |

---

## 四、风格与质感

### 制造"不完美"的真实感

AI 默认追求锐利清晰。加入这些词降低"配合度"：

- `iPhone-style`：手机的真实感
- `Candid shot` / `Secretly photographed`：抓拍核心词
- `Slightly shaky` / `Softly blurred due to motion`：动态模糊

### 胶卷选择

| 胶卷 | 特点 | 适合场景 |
|------|------|---------|
| Kodak Portra 400 | 肤色还原极佳，色彩细腻温润 | 人像、生活感 |
| Fujifilm Pro 400H | 偏冷调，绿蓝色出色 | 日系、清冷、风景 |
| Kodak Gold 200 | 暖调，高饱和，复古感强 | 怀旧、街头、夏日氛围 |
| Cinestill 800T | 夜景神卷，高光光晕 | 夜景、电影感 |

写法：`shot on Kodak Portra 400, film grain, vintage aesthetic`

### 数字化渲染风格

- `Unreal Engine 5` / `Octane Render`：极致光影计算
- `Ray Tracing`：强调反射和折射的真实感

**注意：胶片感和 3D 渲染感冲突，不要混用。**

### 导演/艺术家风格借用

- `Wes Anderson style`：素雅、对称、高饱和配色
- `Blade Runner 2049 aesthetic`：赛博朋克、高对比霓虹
- `Hiroshi Sugimoto`：极致极简主义和留白

**一次只借用一种核心美学，不要堆砌。**

---

## 工作流程

当用户请求生成图片或提示词时：

1. **理解需求**：用户想要什么主体？什么情绪？什么用途？
2. **构建提示词**：按五大模块逐一填充
3. **输出完整提示词**：整合所有元素
4. **解释设计逻辑**：告知用户为什么这么写

### 关键注意事项

- 风格材质词放在提示词**后半段**，作为整体画面的"润色"
- 胶片风格和 3D 渲染风格**不要混用**
- 一次只借用**一种**核心美学风格
- 描述光的**逻辑**，而不是光的**形容词**
- 镜头和角度**必须一起写**，AI 才能完全理解拍摄方式
- **不完美才真实**：适当加入动态模糊、颗粒感、抓拍行为词

---

## 示例

### 小白写法（❌ 避免）

```
A beautiful girl standing in street.
```
结果：平平无奇，像个塑料手办

### 大师写法（✓ 推荐）

```
Ultra-realistic iPhone-style candid shot of a young Korean woman in her 20s
(idol-like facial ratio, natural beauty), captured from a distance as if
secretly photographed. She is walking through a quiet autumn city street
at morning, expression neutral with no smile, eyes slightly down or
looking forward naturally (not toward the camera). Her outfit is casual
office-casual: light knit top + simple slacks + thin jacket or cardigan,
soft neutral colors. Hair long, slightly wavy, neatly styled with natural
movement. The photo is slightly shaky and softly blurred due to motion for
true candid feel. Background: soft autumn morning light, muted golden tones,
blurred buildings and commuters passing far behind. Realistic depth, no
cinematic contrast. Shot from a distance with slight zoom, 45-degree angle
from the side. Film tone: soft Kodak Portra 400 grain, warm but subtle
color fade, realistic skin texture. No illustration style, no dramatic
lighting, pure realism, everyday emotion, quiet atmosphere.
--ar 9:16
```
