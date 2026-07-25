---
name: claude-remember
description: Review auto-memory entries and propose promotions to project MEMORY.md, user MEMORY.md, or shared memory. Also detects outdated, conflicting, and duplicate entries across memory layers. Originally designed for Claude Code (CLAUDE.md) — adapts to WorkBuddy memory hierarchy.
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

本技能原本为 Claude Code 设计。在 WorkBuddy 环境中，等效的记忆层级为：

1. **项目记忆**: `.workbuddy/memory/MEMORY.md` 和 `.workbuddy/memory/YYYY-MM-DD.md`（项目级）
2. **用户记忆**: `~/.workbuddy/MEMORY.md`（跨项目用户偏好）
3. **身份与灵魂**: `~/.workbuddy/SOUL.md`、`~/.workbuddy/IDENTITY.md`、`~/.workbuddy/USER.md`
4. **云记忆**: 系统自动维护的长期记忆（不可手动修改）

> **注意**: 在 Claude Code 环境中，对应文件为 `CLAUDE.md`、`CLAUDE.local.md`、`~/.claude/CLAUDE.md`。跨环境使用时请注意映射关系。

## Steps

### 1. Gather all memory layers

Read all existing memory files from the locations above. Your auto-memory content is already in your system prompt — review it there. Note which team memory sections exist, if any.

**Success criteria**: You have the contents of all memory layers and can compare them.

### 2. Classify each auto-memory entry

For each substantive entry in auto-memory, determine the best destination:

| Destination | What belongs there | Examples |
|---|---|---|
| **项目 MEMORY.md** | 项目级约定和规范，所有协作者应遵循 | "用 bun 不用 npm"、"API 路由使用 kebab-case"、"测试命令是 bun test" |
| **用户 ~/.workbuddy/MEMORY.md** | 跨项目的用户个人偏好和习惯 | "偏好简洁回复"、"总是解释 trade-off"、"运行测试前不要提交" |
| **项目日报** | 每日工作日志，仅追加 | 当天完成的工作、技术选型、项目约定变更 |
| **保持在自动记忆** | 临时上下文、工作笔记、不明确归属的条目 | 会话特定观察、不确定的模式 |

**Important distinctions:**
- CLAUDE.md and CLAUDE.local.md contain instructions for Claude, not user preferences for external tools (editor theme, IDE keybindings, etc. don't belong in either)
- Workflow practices (PR conventions, merge strategies, branch naming) are ambiguous — ask the user whether they're personal or team-wide
- When unsure, ask rather than guess

**Success criteria**: Each entry has a proposed destination or is flagged as ambiguous.

### 3. Identify cleanup opportunities

Scan across all layers for:
- **Duplicates**: Auto-memory entries already captured in project or user MEMORY.md → propose removing from auto-memory
- **Outdated**: MEMORY.md entries contradicted by newer auto-memory entries → propose updating the older layer
- **Conflicts**: Contradictions between any two layers → propose resolution, noting which is more recent

**Success criteria**: All cross-layer issues identified.

### 4. Present the report

Output a structured report grouped by action type:
1. **Promotions** — entries to move, with destination and rationale
2. **Cleanup** — duplicates, outdated entries, conflicts to resolve
3. **Ambiguous** — entries where you need the user's input on destination
4. **No action needed** — brief note on entries that should stay put

If auto-memory is empty, say so and offer to review MEMORY.md for cleanup.

**Success criteria**: User can review and approve/reject each proposal individually.

## Rules

- Present ALL proposals before making any changes
- Do NOT modify files without explicit user approval
- Do NOT create new files unless the target doesn't exist yet
- Ask about ambiguous entries — don't guess
- Use AskUserQuestion for clarifications when needed

> **跨环境说明**: 本技能最初为 Claude Code 的 CLAUDE.md 记忆系统设计。在 WorkBuddy 环境中，记忆层级为项目 `.workbuddy/memory/MEMORY.md` + `YYYY-MM-DD.md` 日报 + 用户 `~/.workbuddy/MEMORY.md` + 云记忆。执行时请适配这些路径而非 CLAUDE.md。
