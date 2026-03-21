# 🎤 {{title}}

## 📋 演讲信息

| 项目 | 内容 |
|------|------|
| **演讲者** | {{speaker}} |
| **日期** | {{date}} |
| **时长** | {{duration}} |
| **场合** | {{venue}} |
| **主题** | {{topic}} |
| **视频源** | {{video_path}} |

---

## 📝 内容摘要

{{summary}}

---

## 🏛️ 核心论点 (金字塔结构)

### 中心思想
{{central_thesis}}

### 主要论点
{{#each main_arguments}}
#### {{@index}}. {{title}}
{{description}}

**支持证据**:
{{#each evidence}}
- {{this}}
{{/each}}

**时间戳**: {{timestamp}}

---

{{/each}}

### 次要论点
{{#each supporting_points}}
- {{this}}
{{/each}}

---

## 📊 关键数据/图表

{{#each data_points}}
### {{title}}
- **数据**: {{value}}
- **来源**: {{source}}
- **时间戳**: {{timestamp}}
- **解读**: {{interpretation}}

{{/each}}

---

## 🎯 结论与建议

{{conclusion}}

### 行动呼吁
{{call_to_action}}

---

## 💎 金句摘录

{{#each key_quotes}}
> "{{text}}"
> — {{speaker}} ({{time}})
> 🎤 **场合**: {{context}}

{{/each}}

---

## 🖼️ 幻灯片内容

{{#each slides}}
### Slide {{number}} ({{time}})
{{#if title}}**{{title}}**{{/if}}

{{content}}

{{#if key_point}}
💡 **要点**: {{key_point}}
{{/if}}

---

{{/each}}

---

## 📎 附件

- 原始视频: {{video_path}}
- 生成时间: {{generated_at}}

---

{{#if include_transcript}}
<details>
<summary>📝 完整字幕 (点击展开)</summary>

{{#each transcript_segments}}
**[{{start_time}} - {{end_time}}]** *{{speaker}}*: {{text}}

{{/each}}
</details>
{{/if}}

---

*由 Video Minutes 自动生成*
*模板: presentation | 类型: {{video_type}} | 置信度: {{confidence}}*
