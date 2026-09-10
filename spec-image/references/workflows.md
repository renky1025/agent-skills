# spec-image 工作流模板库

按任务类型取用，模板中 `[...]` 为填充位。所有模板已内置该场景的高频负向约束，直接复用。

## A. 生成类（GEN）

### A1 胶片写实人像
要点：岁月痕迹 + 真实肤质 + 抓拍感，拒绝塑料磨皮。
```
Create a photorealistic candid photograph of [主体] in [场景].
[他/她] has weathered skin with visible wrinkles, pores, and sun texture.
[锁定姿态三维度：全身/半身构图、视线朝向、手部交互].
Shot like a 35mm film photograph, [景别] at eye level, using a 50mm lens.
Soft natural daylight, shallow depth of field, subtle film grain, natural color balance.
The image should feel honest and unposed, with real skin texture and everyday detail.
No glamorization, no heavy retouching.
```
参数：竖版 2:3, quality=medium。

### A2 商业广告精准文字排版
要点：品牌调性 + 文案频次 + 排版融合 + 负向过滤。
```
Create a [调性描述：polished campaign image for ...] ad for a brand called [品牌].
The ad shows [画面内容], with the tagline "[文案，双引号]".
Render the tagline exactly once, clearly and legibly, integrated into the ad layout.
[字体特征：sans-serif bold, 居中, 高对比度].
Use clean composition, strong color direction, natural poses.
No extra text, no watermarks, no unrelated logos.
```

### A3 原生透明底 Logo/素材
要点：参数 transparent 与 Prompt 双保险。
```
Create an original, non-infringing logo for [品牌与行业].
The logo should feel [调性]. Use clean, vector-like shapes, a strong silhouette,
and balanced negative space. Favor simplicity over detail so it reads clearly
at small and large sizes. Flat design, minimal strokes, no gradients unless essential.
Deliver a single centered logo with generous padding, clean alpha edges,
and no solid backdrop, scenery, checkerboard, or watermark.
```
参数：必须开启透明通道，输出 PNG。矢量感不等于真矢量，交付时向用户说明。

### A4 四格连环条漫
要点：逐格定义视觉节拍（Visual Beats），每格含动作与冲突。
```
Create a short vertical comic with 4 panels about [主题].
Panel 1: [动作 + 情绪 + 镜头].
Panel 2: [转折].
Panel 3: [高潮].
Panel 4: [收尾].
Consistent character design across all panels, consistent art style.
No text in panels (或: with caption "[...]" exactly once in panel N).
```
参数：竖版 2:3。

### A5 真实移动端 UI 原型
要点：把模型当 UI 设计师，禁用概念艺术风。
```
Create a realistic mobile app UI mockup for [产品与场景].
Show [模块清单：header / 列表 / 卡片区 / 信息栏，逐项列出].
Design it to be practical and easy to use.
White background, subtle natural accent colors, clear typography, minimal decoration.
It should look like a real, well-designed, beautiful app.
Place the UI mockup in an iPhone frame.
```
禁用词：concept art、futuristic UI。

### A6 教学原理图/信息流程图
要点：设定受众 + 术语标签清单 + 箭头流向。
```
Create a simple [学科] diagram titled "[标题，双引号]" for [受众].
Show [核心过程]. Include [步骤/环节清单].
Use arrows to connect the steps, and label the main elements: [术语清单].
Make it look like a clean classroom handout, with a white background,
simple icons, clear labels, and easy-to-read text.
Avoid tiny text, extra decoration, or anything that makes the diagram hard to understand.
```
参数：quality 必须 high。

### A7 商业路演单页
要点：规格书式 + 真实具体数据 + 严厉排除俗套元素。
```
Create one pitch-deck slide titled "[标题]" that feels like a real Series A slide.
Use a clean white background, modern sans-serif typography like Inter, crisp minimal layout.
The slide should include:
* [图表类型，如 TAM/SAM/SOM concentric-circle diagram in muted blues and grays]
* Specific, believable numbers: [逐项列出真实数字]
* [辅助元素：chart / footnotes / logo placeholder]
Avoid clip art, stock photography, gradients, shadows, decorative elements,
or anything that feels generic or overdesigned.
```
参数：16:9, quality=high。

## B. 编辑类（EDIT / EXTRACT）

### B1 虚拟换装（人物一致性标杆模板）
```
Edit the image to dress the person using the provided clothing images.
Do not change [his/her] face, facial features, skin tone, body shape, pose, or identity in any way.
Preserve [his/her] exact likeness, expression, hairstyle, and proportions.
Replace only the clothing, fitting the garments naturally to the existing pose
and body geometry with realistic fabric behavior.
Match lighting, shadows, and color temperature to the original photo so the outfit
integrates photorealistically, without looking pasted on.
Do not change the background, camera angle, framing, or image quality,
and do not add accessories, text, logos, or watermarks.
```

### B2 透明底商品提取
```
Extract the product from the input image and isolate it on a fully transparent background.
Output: centered product, crisp silhouette, no halos/fringing.
Preserve product geometry and label legibility exactly.
Add only light polishing. Do not add a solid backdrop, checkerboard, scenery, or shadow.
Do not restyle the product.
```
参数：透明通道开启，输出 PNG。

### B3 草图转超写实
```
Turn this drawing into a photorealistic image.
Preserve the exact layout, proportions, and perspective.
Choose realistic materials and lighting consistent with the sketch intent.
Do not add new elements or text.
```

### B4 手术级单物替换
```
In this photo, replace ONLY the [目标物] with [替换物].
Preserve camera angle, lighting, floor shadows, reflections, and surrounding objects.
Keep all other aspects of the image unchanged.
Photorealistic contact shadows and material texture.
```

### B5 多图合成
```
Place the [主体] from the second image into the setting of image 1,
[位置关系]. Use the same style of lighting, composition and background.
Do not change anything else.
```
多图时逐图编号指定角色：图 1 = 场景/光影基准，图 2 = 主体来源，图 3 = 风格参考。

## C. 系列类（SERIES）

### C1 两阶段角色一致性
阶段一（角色卡）：
```
Create an illustration introducing a main character.
Character: [服装逐项 / 五官特征 / 气质].
Style: [画风逐项].
Constraints: Original character, no text, plain background.
```
阶段二（逐场景延续，每次重申）：
```
Continue using the same character.
Scene: [新场景].
Character Consistency:
- Same [服装]
- Same facial features, proportions, and color palette
- Same personality
Constraints: Do not redesign the character, no text.
```
每张新图都将上一张满意输出作为参考输入，单场景单变量调整。
