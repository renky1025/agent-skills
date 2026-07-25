---
name: claude-remember
description: Review auto-memory entries and propose promotions across memory layers (project-level, user-level, shared). Also detects outdated, conflicting, and duplicate entries. Adaptable to any AI agent's memory hierarchy.
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "AskUserQuestion"]
when_to_use: |
  Use when the user wants to review, organize, or promote their auto-memory entries.
  Trigger phrases: "review my memories", "organize memories", "promote to MEMORY.md",
  "clean up memories", "memory review", "check for duplicate memories",
  "what should go in MEMORY.md".
argument-hint: "[optional focus area or specific memory to review]"
---

# Memory Review

## Goal
Review the user's memory landscape and produce a clear report of proposed changes, grouped by action type. Do NOT apply changes — present proposals for user approval.

## Memory File Locations

AI agent 的记忆系统通常分多个层级。执行本技能前，先确认当前运行环境的记忆层级：

1. **项目级记忆**: 存储于项目根目录下的记忆文件（如 `MEMORY.md` / `CLAUDE.md` / `.cursorrules` 等），所有协作者共享
2. **用户级记忆**: 存储于用户主目录下的全局记忆文件，跨项目共享个人偏好
3. **运行日报**: 每日追加的工作日志（如 `YYYY-MM-DD.md`）
4. **自动记忆/云记忆**: 系统自动维护的长期记忆（通常不可手动修改）

> **执行前先扫描**: 使用 Glob/Grep 工具确认实际存在的记忆文件路径，不要假设固定的文件命名。

## Steps

### 1. Gather all memory layers

Read all existing memory files from the locations above. Your auto-memory content is already in your system prompt — review it there. Note which team memory sections exist, if any.

**Success criteria**: You have the contents of all memory layers and can compare them.

### 2. Classify each auto-memory entry

For each substantive entry in auto-memory, determine the best destination:

| Destination | What belongs there | Examples |
|---|---|---|
| **项目 MEMORY.md** | 项目级约定和规范，所有协作者应遵循 | "用 bun 不用 npm"、"API 路由使用 kebab-case"、"测试命令是 bun test" |
| **用户 MEMORY.md** | 跨项目的用户个人偏好和习惯 | "偏好简洁回复"、"总是解释 trade-off"、"运行测试前不要提交" |
| **项目日报** | 每日工作日志，仅追加 | 当天完成的工作、技术选型、项目约定变更 |
| **保持在自动记忆** | 临时上下文、工作笔记、不明确归属的条目 | 会话特定观察、不确定的模式 |

**Important distinctions:**
- 记忆文件存储的是 AI 助手的指令，不包括用户对外部工具的偏好（编辑器主题、IDE 快捷键等）
- Workflow practices (PR conventions, merge strategies, branch naming) are ambiguous — ask the user whether they're personal or team-wide
- When unsure, ask rather than guess

**Success criteria**: Each entry has a proposed destination or is flagged as ambiguous.

### 3. Identify cleanup opportunities

Scan across all layers for:
- **Duplicates**: Auto-memory entries already captured in project or user memory files → propose removing from auto-memory
- **Outdated**: Memory entries contradicted by newer auto-memory entries → propose updating the older layer
- **Conflicts**: Contradictions between any two layers → propose resolution, noting which is more recent

**Success criteria**: All cross-layer issues identified.

### 4. Present the report

Output a structured report grouped by action type:
1. **Promotions** — entries to move, with destination and rationale
2. **Cleanup** — duplicates, outdated entries, conflicts to resolve
3. **Ambiguous** — entries where you need the user's input on destination
4. **No action needed** — brief note on entries that should stay put

If auto-memory is empty, say so and offer to review existing memory files for cleanup.

**Success criteria**: User can review and approve/reject each proposal individually.

## Rules

- Present ALL proposals before making any changes
- Do NOT modify files without explicit user approval
- Do NOT create new files unless the target doesn't exist yet
- Ask about ambiguous entries — don't guess
- Use AskUserQuestion for clarifications when needed
