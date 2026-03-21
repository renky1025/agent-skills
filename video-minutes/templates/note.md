# 📝 {{title}}

## 📋 记录信息

| 项目 | 内容 |
|------|------|
| **日期** | {{date}} |
| **时长** | {{duration}} |
| **标签** | {{tags}} |
| **视频源** | {{video_path}} |

---

## 📝 转录内容

{{clean_transcript}}

---

## 🏷️ 想法归类

{{#each idea_categories}}
### {{name}}
{{#each ideas}}
- {{this}}
{{/each}}

{{/each}}

---

## ✅ 提取的待办

{{#each todos}}
- [ ] {{task}} {{#if priority}}({{priority}}){{/if}}
{{/each}}

---

## 🔗 关联笔记

{{#each related_notes}}
- [[{{this}}]]
{{/each}}

---

## 💭 灵感与想法

{{#each inspirations}}
- 💡 {{this}}
{{/each}}

---

## 📎 附件

- 原始视频: {{video_path}}
- 生成时间: {{generated_at}}

---

*由 Video Minutes 自动生成*
*模板: note | 类型: {{video_type}} | 置信度: {{confidence}}*
