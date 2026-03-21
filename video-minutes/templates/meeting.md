# {{title}}

## 📋 会议信息

| 项目 | 内容 |
|------|------|
| **日期** | {{date}} |
| **时长** | {{duration}} |
| **类型** | {{meeting_type}} |
| **视频源** | {{video_path}} |

## 👥 参会人员

{{participants}}

---

## 🎯 核心决议

{{#each decisions}}
- [x] {{this}}
{{/each}}

---

## ✅ 行动项

| # | 任务 | 负责人 | 截止日期 | 优先级 | 状态 |
|---|------|--------|----------|--------|------|
{{#each action_items}}
| {{@index}} | {{task}} | {{assignee}} | {{deadline}} | {{priority}} | ⏳ |
{{/each}}

---

## 📍 关键时间节点

{{#each timeline}}
### {{time}} - {{topic}}
{{summary}}

{{/each}}

---

## 💬 重要讨论摘要

{{discussion_summary}}

---

## 📎 附件

- 原始视频: {{video_path}}
- 生成时间: {{generated_at}}

---

{{#if include_transcript}}
<details>
<summary>📝 完整字幕 (点击展开)</summary>

{{#each transcript_segments}}
**[{{start_time}} - {{end_time}}]** {{#if speaker}}*{{speaker}}*: {{/if}}{{text}}

{{/each}}
</details>
{{/if}}

---

## 🔗 相关链接

{{#if related_notes}}
### 关联笔记
{{#each related_notes}}
- [[{{this}}]]
{{/each}}
{{/if}}

{{#if dispatch_results}}
### 任务分发状态
{{#each dispatch_results}}
- {{tag}}: {{status}} {{#if link}}[查看]({{link}}){{/if}}
{{/each}}
{{/if}}

---

*由 Video Minutes 自动生成*
*模板: meeting | 类型: {{video_type}} | 置信度: {{confidence}}*
