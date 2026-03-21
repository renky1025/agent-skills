# 🎙️ {{title}}

## 📋 访谈信息

| 项目 | 内容 |
|------|------|
| **受访者** | {{interviewee}} |
| **采访者** | {{interviewer}} |
| **日期** | {{date}} |
| **时长** | {{duration}} |
| **主题** | {{topic}} |
| **视频源** | {{video_path}} |

---

## 📝 内容摘要

{{summary}}

---

## ❓ 问答整理

{{#each qa_pairs}}
### Q{{@index}}: {{question}}
**提问时间**: {{asked_at}}

**A**: {{answer}}

**回答时间**: {{answered_at}}

{{#if follow_up}}
**追问**: {{follow_up}}
{{/if}}

---

{{/each}}

---

## 🎭 双方观点对比

### 采访者观点
{{#each interviewer_views}}
- {{this}}
{{/each}}

### 受访者观点
{{#each interviewee_views}}
- {{this}}
{{/each}}

### 共识与分歧
{{consensus_analysis}}

---

## 💎 金句摘录

{{#each key_quotes}}
> "{{text}}"
> — {{speaker}} ({{time}})
> 📝 **话题**: {{topic}}

{{/each}}

---

## 📊 话题索引

{{#each topics}}
### {{name}}
- **时间段**: {{start_time}} - {{end_time}}
- **核心内容**: {{summary}}
- **关键引用**: {{key_quote}}

{{/each}}

---

## 🔍 深度分析

{{analysis}}

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
*模板: interview | 类型: {{video_type}} | 置信度: {{confidence}}*
