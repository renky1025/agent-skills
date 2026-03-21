# 🎧 {{title}}

## 📋 播客信息

| 项目 | 内容 |
|------|------|
| **主播** | {{host}} |
| **嘉宾** | {{guest}} |
| **日期** | {{date}} |
| **时长** | {{duration}} |
| **系列** | {{series}} |
| **集数** | {{episode}} |
| **视频源** | {{video_path}} |

---

## 📝 内容摘要

{{summary}}

---

## 📑 话题时间索引

{{#each topics}}
### {{title}} ⏱️ {{start_time}}
{{summary}}

{{#if highlights}}
**高光时刻**:
{{#each highlights}}
- [{{time}}] {{description}}
{{/each}}
{{/if}}

---

{{/each}}

---

## 💎 金句摘录

{{#each key_quotes}}
> "{{text}}"
> — {{speaker}} ({{time}})
> 🎙️ **话题**: {{topic}}
> {{#if context}}💬 **上下文**: {{context}}{{/if}}

{{/each}}

---

## ⭐ 推荐片段

{{#each recommended_clips}}
### {{title}} ({{start_time}} - {{end_time}})
{{description}}

**为什么推荐**: {{reason}}

🔗 **分享链接**: 从 {{start_time}} 开始播放

---

{{/each}}

---

## 🔗 相关资源

{{#each resources}}
- [{{title}}]({{url}}) - {{description}}
{{/each}}

---

## 📚 提及的书籍/文章/作品

{{#each mentions}}
- **{{title}}** ({{type}})
  - 提及时间: {{timestamp}}
  - 上下文: {{context}}
  {{#if recommendation}}
  - 推荐程度: {{recommendation}}
  {{/if}}

{{/each}}

---

## 🎭 互动与讨论

{{#if audience_qa}}
### 听众问答
{{#each audience_qa}}
**Q**: {{question}}
**A**: {{answer}}

{{/each}}
{{/if}}

{{#if host_guest_dynamics}}
### 主播与嘉宾互动
{{host_guest_dynamics}}
{{/if}}

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
*模板: podcast | 类型: {{video_type}} | 置信度: {{confidence}}*
