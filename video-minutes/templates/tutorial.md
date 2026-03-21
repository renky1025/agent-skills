# 🛠️ {{title}}

## 📋 教程信息

| 项目 | 内容 |
|------|------|
| **讲师** | {{instructor}} |
| **难度** | {{difficulty}} |
| **时长** | {{duration}} |
| **主题** | {{topic}} |
| **技术栈** | {{tech_stack}} |
| **视频源** | {{video_path}} |

---

## 📝 内容摘要

{{summary}}

---

## ✅ 步骤清单

{{#each steps}}
### Step {{@index}}: {{title}} ⏱️ {{timestamp}}

{{#if duration}}预计耗时: {{duration}}{{/if}}

{{description}}

{{#if code_snippet}}
```{{language}}
{{code_snippet}}
```
{{/if}}

{{#if screenshot_hint}}
📸 **截图提示**: {{screenshot_hint}}
{{/if}}

{{#if tips}}
💡 **小贴士**:
{{#each tips}}
- {{this}}
{{/each}}
{{/if}}

{{#if warnings}}
⚠️ **注意事项**:
{{#each warnings}}
- {{this}}
{{/each}}
{{/if}}

- [ ] 完成 Step {{@index}}

---

{{/each}}

---

## ⌨️ 快捷键/命令汇总

{{#if keyboard_shortcuts}}
### 快捷键
| 快捷键 | 功能 | 使用场景 |
|--------|------|----------|
{{#each keyboard_shortcuts}}
| {{key}} | {{function}} | {{scene}} |
{{/each}}
{{/if}}

{{#if commands}}
### 常用命令
```bash
{{#each commands}}
# {{description}}
{{command}}

{{/each}}
```
{{/if}}

---

## 🐛 常见问题/踩坑点

{{#each pitfalls}}
### Q{{@index}}: {{question}}
**问题描述**: {{description}}

**解决方案**: {{solution}}

**预防方法**: {{prevention}}

---

{{/each}}

---

## 📚 前置知识

{{#each prerequisites}}
- [{{title}}]({{link}}) - {{description}}
{{/each}}

---

## 🔗 延伸阅读

{{#each resources}}
### {{category}}
{{#each items}}
- [{{title}}]({{url}}) - {{description}}
{{/each}}

{{/each}}

---

## 💬 学习笔记

{{#if personal_notes}}
{{personal_notes}}
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
*模板: tutorial | 类型: {{video_type}} | 置信度: {{confidence}}*
