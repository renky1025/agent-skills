# 📚 {{title}}

## 📖 课程信息

| 项目 | 内容 |
|------|------|
| **讲师** | {{speaker}} |
| **日期** | {{date}} |
| **时长** | {{duration}} |
| **主题** | {{topics}} |
| **视频源** | {{video_path}} |

---

## 🗺️ 知识图谱

```mermaid
{{knowledge_graph}}
```

---

## ⏱️ 章节速览

{{#each chapters}}
### {{@index}}. {{title}} ({{start_time}} - {{end_time}})
{{summary}}

**要点:**
{{#each key_points}}
- {{this}}
{{/each}}

{{/each}}

---

## 📝 核心概念

{{#each key_concepts}}
### {{name}}
{{description}}

{{#if related}}
**相关概念**: {{related}}
{{/if}}

{{/each}}

---

## 💡 重点摘录

{{#each key_quotes}}
> "{{text}}"
> — {{#if speaker}}{{speaker}}{{/if}} {{time}}
>
> 💬 **上下文**: {{context}}

{{/each}}

---

## 🔍 深度解读

{{analysis}}

---

## ❓ 疑问与思考

{{#each questions}}
### Q{{@index}}: {{question}}
**我的思考**: {{thoughts}}

{{/each}}

---

## 🔗 延伸阅读

{{#each references}}
- [{{title}}]({{url}}) - {{description}}
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
**[{{start_time}} - {{end_time}}]** {{#if speaker}}*{{speaker}}*: {{/if}}{{text}}

{{/each}}
</details>
{{/if}}

---

*由 Video Minutes 自动生成*
*模板: lecture | 类型: {{video_type}} | 置信度: {{confidence}}*
