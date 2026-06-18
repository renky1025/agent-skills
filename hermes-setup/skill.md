---
name: hermes-setup
description: >
  全自动安装和配置 Hermes Agent（NousResearch）——从零开始，7 天搭建一个
  自我进化的 AI 个人 Operator。涵盖安装、身份/SOUL.md、模型选择、记忆系统、
  消息网关（Telegram/Discord/Slack/WhatsApp）、Skills 技能系统、Cron 定时任务、
  /goal 自主执行、Dashboard/Kanban、多 Profile 隔离、安全配置。

  综合 @zaimiri 7日指南 + @PrajwalTomar_ 深度剖析 + 官方文档最佳实践。

  Use when the user asks to install/setup/configure Hermes Agent, deploy a
  personal AI agent, "搭建 Hermes", or any request about NousResearch's agent.
triggers:
  - install: hermes/hermes agent/安装hermes/hermes setup/搭建hermes/nous agent
  - config: 配置hermes/hermes配置/hermes config/hermes模型/hermes model
  - identity: hermes身份/hermes personality/SOUL.md/hermes角色/hermes soul
  - memory: hermes记忆/hermes memory/记忆系统
  - gateway: hermes网关/hermes gateway/telegram bot/消息通道
  - goal: /goal/自主执行/auto run/autonomous/后台任务/自动化执行
  - dashboard: hermes dashboard/看板/kanban/localhost 9119
  - skill: hermes skill/技能/自动化流程/自学习
  - cron: 定时任务/cron/定时调度/定时提醒
  - profile: 多环境/多profile/hermes profile/隔离/多账号/hermes profiles
  - model: 模型选择/model tier/gpt/claude/qwen/模型分层
  - comparison: hermes vs claude code/什么时候用hermes/hermes和claude区别
  - security: 安全/hermes安全/bitwarden/egress/权限控制
metadata:
  author: extracted from @zaimiri + @PrajwalTomar_ guides + NousResearch official docs
  source_tweets:
    - https://x.com/zaimiri/status/2066117404392890835
    - https://x.com/PrajwalTomar_/status/2064324584254710262
  official_repo: https://github.com/NousResearch/hermes-agent
  official_docs: https://hermes-agent.nousresearch.com/docs/
  stars: 194k+
  latest_features: Hermes Desktop, Stripe integration, Async subagents, NVIDIA Nemotron Ultra for Hermes
---

# Hermes Agent 安装配置自动化 Skill

## 概述

从零安装配置 [Hermes Agent](https://github.com/NousResearch/hermes-agent)（NousResearch），
综合 @zaimiri 的 **7 天渐进式搭建法** + @PrajwalTomar_ 的深度实战指南，构建一个稳定、自我进化的 AI 个人 Operator。

**Hermes 是什么？** 它不是"Claude Code 2.0"。Claude Code/Cursor/Codex 是**会话式 agent**——每次打开从零开始。Hermes 是**持久式 agent**——跑在服务器上 24/7，记得每一次对话，自主写 skill，主动联系你。它不是一个编码工具，而是一个全新的 agent 品类。

**核心理念：** 先可靠，再惊艳。不要一气呵成搭 10 个工具连 5 个 API，而是按正确顺序堆叠每一层。

```
Telegram → Hermes → memory → skill → tool call → verified output → short receipt
Cron → Hermes → sources → filter → alert only if useful
```

**最新动态（2026年6月）：**
- 🖥️ **Hermes Desktop** 桌面版正式发布
- 💳 **Stripe 集成** — Agent 可直接购买、支付 API、自动订阅 SaaS
- 🔄 **异步 Subagent** — delegate 不再阻塞聊天
- 🧠 **NVIDIA Nemotron Ultra** 专为 Hermes 后训练
- 📈 GitHub 185K+ stars，团队半年扩 3 倍

---

## 系统要求

| 平台 | 支持情况 | 说明 |
|------|---------|------|
| Linux | ✅ 全功能 | Ubuntu 20.04+, Debian 11+, CentOS 8+ |
| macOS | ✅ 全功能 | Intel & Apple Silicon |
| WSL2 | ✅ 全功能 | Windows 11 推荐 |
| Windows (Native) | ✅ PowerShell 支持 | `iex (irm ...)` 安装。含便携 Git Bash |
| Termux (Android) | ✅ 全功能 | 有独立安装文档 |
| Docker | ✅ 后端支持 | 作为 terminal backend |

**安装器自动处理：** uv, Python 3.11, Node.js 22, ripgrep, ffmpeg, Git Bash (Windows)。

---

## 环境检查

```bash
# 检查系统是否满足基本要求
python3 --version  # 需要 3.10+
curl --version

# 磁盘空间检查（安装后约占用 2-3GB）
df -h ~
```

---

## 🗓 Day 1：安装 & 验证基础

**目标：** 证明 Hermes 能跑、能调用工具、能响应。不自定义，只验证地基。

### 1.1 安装

```bash
# Linux / macOS / WSL2 / Termux
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# Windows Native (PowerShell)
iex (irm https://hermes-agent.nousresearch.com/install.ps1)

# 重载 shell（安装后必做）
source ~/.zshrc   # 或 source ~/.bashrc
```

### 1.2 首次设置

```bash
# 方式 A：交互式向导（推荐新手）
hermes setup

# 方式 B：快速通道 — 用一个 Nous Portal 订阅搞定（模型 + 搜索 + 图片 + TTS）
hermes setup --portal  # OAuth 登录，自动配置

# 方式 C：纯手动
hermes config set model anthropic/claude-sonnet-4-20250514
hermes config set OPENAI_API_KEY sk-...      # 或 OpenRouter / 其他
```

### 1.3 验证

```bash
# 健康检查
hermes doctor

# 选择模型提供商
hermes model

# 启动对话测试
hermes chat
```

**验证通过标准：** 能成功发送消息并收到回复。`hermes doctor` 无红色错误。

### 1.4 可选：配置终端后端

```bash
# 查看当前终端配置
hermes config

# 切换后端（本地 → Docker → SSH → Modal → Daytona）
hermes config set terminal.backend local
hermes config set terminal.backend docker
hermes config set terminal.backend modal    # 服务端无状态，按需唤醒
hermes config set terminal.backend daytona  # 同上
```

---

## 🗓 Day 2：身份层（Identity / SOUL.md）

**目标：** 定义 agent 的人格、语气、边界。**工具可以等，人格先定。**

在 Day 2 就做好身份定义，否则加了记忆和工具后 agent 会变得混乱。

### 2.1 查看/编辑身份文件

```bash
# 查看当前 SOUL.md
cat ~/.hermes/SOUL.md

# 编辑
hermes config edit  # 找到 SOUL.md 路径或直接编辑
nano ~/.hermes/SOUL.md
```

### 2.2 官方推荐 SOUL.md 模板

SOUL.md 占据 system prompt 的 **slot #1**，定义了 agent 的持久身份。一旦填好，它会完全替换内置默认身份。
这不是项目级别的（那是 AGENTS.md 的事），**这是 agent 本身的底层人格。**

Nous Research 官方发布的规范模板：

```markdown
# Identity

## Personality
Who the agent is.
— "You are a pragmatic senior engineer with strong taste."
— "You are a creative strategist who values clarity over cleverness."

## Style
How it should sound.
— "Be direct without being cold."
— "Push back when something is a bad idea."
— "Use examples, not abstractions."

## What to avoid
— "Sycophancy."
— "Hype language."
— "Overexplaining obvious things."
— "Guessing file contents, dates, system state, or live facts."

## Technical posture
— "Prefer simple systems over clever systems."
— "Ask before risky writes (delete, overwrite, deploy, pay)."
— "If a workflow becomes repeatable, offer to save it as a skill."
```

**关键安全底线（建议每个人都在 SOUL.md 加上这一条）：**
```
— "Never send money to anyone without explicit confirmation."
```
一条规则覆盖大多数个人使用的风险。

> **趋势：** 社区已经从 CLAUDE.md 迁移到 SOUL.md 作为最主要的 leverage 文件。同一个概念，新一代 agent 的文件。

### 2.3 预设 Personality

```bash
# Hermes 内置 personality 预设
hermes personality          # 列出可用
hermes personality default  # 切换
```

### 2.4 验证

```bash
hermes chat  # 测试 agent 的语气和行为是否符合预期
```

---

## ⚡ 模型分层指南（Model Tier Guide）

Hermes 是 provider-agnostic 的，随时可以 `hermes model` 切换。社区总结出三层实用配置：

| 层级 | 推荐模型 | 用途 | 成本 |
|------|---------|------|------|
| 🟢 **日常驱动** | GPT-5.5 (现有 $20/月 ChatGPT 订阅) | 日常对话、简单任务 | $20/月 |
| 🔵 **复杂推理** | Claude Opus 4 / Sonnet 4 (API key) | 多步骤任务、/goal 自主运行 | ~几百$/月(重度) |
| 🟣 **长程自主** | Qwen 3.7 Max (OpenRouter) | 35h+ 连续执行，1000+ tool calls 不丢上下文 | 按量计费 |

**推荐起点：** GPT-5.5 日常 + Claude API key 用于 `/goal` 跑。其他等真正需要再上。

```bash
hermes model                          # 交互式切换
hermes config set model openrouter/anthropic/claude-sonnet-4
hermes config set model openrouter/qwen/qwen-3.7-max
```

> Skill 文件和记忆不依赖模型，切换后自动继承。

如果不想管理多个账单，**Nous Portal** (`hermes setup --portal`) 提供 $20/月 OAuth 一站式订阅。

---

**目标：** 只保存一个月后仍然有用的信息。**不要存档一切，存档能减少重复引导的信息。**

### 3.1 记忆存储位置

```bash
ls ~/.hermes/memories/
# MEMORY.md  — 持久事实
# USER.md    — 用户画像
```

### 3.2 高质量记忆示例

**应该存的（一个月后仍有用）：**
- "User prefers short Telegram receipts."
- "Use Typefully as draft-only for Zaimiri posts."
- "Client-facing docs must not mention internal agent names."
- "For calculations, use a tool instead of mental math."

**不要存的（临时上下文）：**
- "We are currently debugging issue #217."
- "User asked for three article angles today."
- "Drafted a post about Hermes last night."

### 3.3 管理记忆

```bash
# 直接编辑记忆文件
nano ~/.hermes/memories/MEMORY.md

# Hermes 也会在对话中自动学习记忆
# 使用 /remember 在对话中保存事实
```

### 3.4 可选：Honcho 记忆提供商

Hermes 支持 [Honcho](https://github.com/plastic-labs/honcho) dialectic user modeling
（辩证式用户建模），随时间构建更深的用户画像：

```bash
hermes config set memory.provider honcho
hermes config set HONCHO_API_KEY hk-...
```

---

## 🗓 Day 4：接入实际使用界面（Gateway）

**目标：** 把 Hermes 放到你每天使用的界面中。终端 agent 再强，想不起来打开就是废的。

### 4.1 支持的平台

| 平台 | 状态 | 配置方式 |
|------|------|---------|
| Telegram | ✅ 推荐 | Bot Token |
| Discord | ✅ | Bot Token + Guild ID |
| Slack | ✅ | App Token |
| WhatsApp | ✅ | API 配置 |
| Signal | ✅ | CLI + Phone number |
| Email | ✅ | SMTP/IMAP |

### 4.2 Telegram 配置（推荐起点）

```bash
# 1. 创建 Telegram Bot（在 Telegram 中找 @BotFather）
#    → /newbot → 获取 token: 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# 2. 配置 Hermes
hermes gateway setup

# 3. 按提示输入 Bot Token

# 4. 启动网关
hermes gateway start
```

**🔓 真正的解锁：第一条消息**

配置好 bot 后，**给它发第一条消息**——你是谁、你在做什么、你未来 3-6 个月的目标。

这条消息直接进入 agent 的持久记忆，会过滤它以后生成的每一个主动任务。**跳过这一步，agent 就在盲跑。**

这就是"在手机上指挥 agent"的真相：你可以坐在沙发上发新任务，喝咖啡时检查过夜完成的工作，出门吃饭时从手机上看 6 个 agent 的进度。agent 不在乎你在哪个设备上。

```bash
# 第一次发送机器人消息示例
# "Hi, I'm a founder building AI tools. My main goals for the next 3 months are: 
#  1. Ship our MVP by Aug
#  2. Research competitor landscape
#  3. Build content pipeline for launch"
# → 这条进入记忆，过滤所有后续的主动建议
```

### 4.3 Gateway 管理命令

```bash
hermes gateway          # 查看状态
hermes gateway setup    # 配置/重新配置
hermes gateway start    # 启动（前台）
hermes gateway start --daemon  # 后台守护进程
hermes gateway stop     # 停止

# 多平台同时运行
hermes gateway start --platforms telegram,discord,slack
```

### 4.4 安全配置

```bash
# 限制允许的用户（DM pairing）
hermes config set gateway.allowed_users @yourusername
hermes config set gateway.allowed_chat_ids -1001234567890

# 命令审批
hermes config set safety.command_approval true
```

---

## 🗓 Day 5：创建第一个 Skill

**目标：** 从真实重复任务中提取一个 Skill。**不要先造 10 个理论上的 skill。**

Skill = 过程记忆（procedural memory）。告诉 agent 下次怎么做。

### 5.1 Skill 存放位置

```bash
ls ~/.hermes/skills/
# 每个 skill 是一个 .md 文件或子目录
```

### 5.2 Skill 模板

```markdown
---
name: process-x-link
description: Extract X/Twitter link → draft Zaimiri-native post → save to Typefully
trigger: When user sends a raw X link in the content topic
---

## Steps

1. Inspect the source URL with twitter-cli: `twitter tweet URL --json`
2. Extract: core argument, key quotes, structure
3. Write a fresh Zaimiri-native draft (match voice, don't rephrase — recompose)
4. Route to Typefully as draft-only
5. Send one-line receipt to user

## Common errors
- Tweet deleted → notify user
- Paywalled content → note in draft

## Verification
- Draft saved in Typefully drafts folder
- Receipt sent
```

### 5.3 Skill 管理

```bash
# 在对话中创建
# Hermes 在复杂任务后会主动询问是否保存为 skill

# 浏览已安装 skill
hermes skills
# 或在聊天中使用 /skills

# 手动创建
mkdir -p ~/.hermes/skills/my-skill
nano ~/.hermes/skills/my-skill/skill.md
```

### 5.4 好的 Skill 标准

- **有触发条件：** "当用户发送 X 链接时"
- **有步骤：** 具体的命令和流程
- **有输出：** "发送一行收据"
- **有错误处理：** "如果推文被删除则通知用户"
- **从真实重复中来：** 不是 "be smarter"

### 5.5 自动 Skill 创建（Hermes 核心差异）

Hermes 在每次任务后会**自动写 skill 文件**。当一个任务需要 5 次以上的 tool call 时，它会生成一个 markdown skill：

```markdown
---
name: research-competitor
description: Research a competitor and draft comparison analysis
trigger: When user says "research [company]"
---

## Procedure
1. Search for latest news with web_search
2. Visit company website and analyze
3. Compare with our positioning
4. Draft analysis brief

## Pitfalls
- Pricing pages frequently A/B test based on geo
- Some sources require login

## Verification
- Confirm 3+ independent sources agree on key claims
- Check dates on all sources (avoid stale data)

## Auto-improvement notes
- [2026-06-10] Added geo pricing check
- [2026-06-08] Switched to 3-source minimum
```

每次使用这个 skill 时，Hermes 会检查之前的 auto-improvement notes 来决定是否修改流程。

### 5.6 实践经验

Hermes 有**自主学习闭环**：
- 自动从经验创建 skill
- 在使用中自我改进 skill
- 跨会话搜索（FTS5）和 LLM 总结回忆

```bash
# 查看自主学习功能
hermes config set skills.auto_create true
hermes config set skills.auto_improve true
```

---

## 🗓 Day 6：添加一个安静的定时任务（Cron）

**目标：** 加一个定时调度，但**只在你明确了 context 和 procedure 之后才加**。

### 6.1 规则

- **安静：** 没有信号就不说话。
- **窄范围：** 一个 cron 只做一件事。
- **一天一个起步：** 不要一开始就加 10 个定时任务。

### 6.2 Cron 存放位置

```bash
ls ~/.hermes/cron/
```

### 6.3 创建 Cron

```bash
# 在对话中用自然语言创建
# "每天早上 8:30 检查 Hermes Agent 更新，只有有实质更新才通知我"

# 手动创建
mkdir -p ~/.hermes/cron
```

### 6.4 Cron 模板

```markdown
---
name: daily-research-brief
schedule: "30 8 * * 1-5"  # Weekdays at 8:30
platform: telegram         # Deliver to Telegram
quiet: true                # No signal = no message
---

## Sources
- Twitter: @NousResearch, @zaimiri
- GitHub: NousResearch/hermes-agent releases
- Discord: #announcements channel

## Filter
Only alert if:
- New release or version
- Changed setup instructions
- Breaking issue or useful workflow example
- New feature worth knowing

## Output
- One-paragraph summary
- If no signal: stay silent
```

### 6.5 Cron 管理

```bash
# 查看所有定时任务
hermes cron list

# 暂停/恢复
hermes cron pause daily-research-brief
hermes cron resume daily-research-brief

# 删除
hermes cron remove daily-research-brief
```

### 6.6 好的第一 Cron 建议

- `daily-research-brief` — 每日研究简报
- `weekly-repo-cleanup` — 每周仓库清理
- `morning-inbox-digest` — 早上收件箱摘要
- `server-health-alert` — 服务器健康告警
- `content-radar` — 内容雷达
- `private-source-monitor` — 私有源监控

---

## 🗓 Day 7：Profile 隔离（按需）

**目标：** 只在真正需要隔离时才拆分 Profile。**不要为了酷而创建多个 agent。**

### 7.1 何时需要新 Profile

需要不同以下内容时才拆分：
- **记忆**（memory）
- **身份**（identity）
- **工具**（tools）
- **权限**（permissions）
- **凭证**（credentials）
- **交付渠道**（delivery channel）

### 7.2 Profile 管理

```bash
# 列出 profile
hermes profile list

# 创建新 profile
hermes profile create coding
hermes profile create content
hermes profile create research
hermes profile create client

# 切换到特定 profile 启动
hermes --profile content chat

# 启动 gateway 时指定 profile
hermes --profile client gateway start

# 删除 profile
hermes profile remove coding
```

### 7.3 高阶模式：Profile 组织架构图

这不是简单的环境拆分，而是**把 agent 当作一个团队来管理**。每个 profile 有独立的 SOUL.md、记忆、技能库、模型配置。

```
~/.hermes/profiles/
├── chief-of-staff/       # 参谋长 — 知道你的最高优先级，跑每日简报
├── head-of-research/     # 研究主管 — 深度调研竞品分析和市场趋势
├── head-of-content/      # 内容主管 — 起草和排期 X 帖子、文章
└── head-of-finance/      # 财务主管 — 对账 Stripe、订阅、现金流
```

**使用场景：** 早上一个 Telegram 消息触发 4 个 profile 并行工作。喝完咖啡回来：
- Chief of Staff 已列出今天需要你关注的事项
- Head of Research 已丢下一篇竞品分析更新
- Head of Content 已准备了 3 篇草稿等你审
- Head of Finance 已标记了账上的异常

```bash
# 创建组织架构
hermes profile create chief-of-staff
hermes profile create head-of-research
hermes profile create head-of-content
hermes profile create head-of-finance

# 为每个 profile 设置独立的 SOUL.md
nano ~/.hermes/profiles/chief-of-staff/SOUL.md

# 不同 profile 用不同模型
hermes --profile head-of-research config set model openrouter/anthropic/claude-sonnet-4
hermes --profile head-of-finance config set safety.command_approval true

# 启动特定 profile
hermes --profile chief-of-staff chat
```

> **下一层进化：** Open specialists（处理混乱的开放任务）+ Closed specialists（运行可重复的流水线）。不同 profile 各司其职，互不干扰。

```bash
# 个人 Operator（默认）
hermes profile create default
hermes config set model anthropic/claude-sonnet-4-20250514

# 内容创作
hermes profile create content
hermes --profile content config set model openrouter/anthropic/claude-sonnet-4

# 代码开发
hermes profile create coding
hermes --profile coding config set terminal.backend docker

# 客户端项目
hermes profile create client
hermes --profile client config set safety.command_approval true

# 研究监控
hermes profile create research
```

### 7.4 判断原则

> 如果新场景需要不同的记忆或权限 → 创建 Profile
> 如果只需要一个下午的不同任务 → 用同一个 agent

---

## 🎯 /goal 自主执行（Autonomous Overnight Runs）

**核心命令：** 把 Hermes 从"响应式聊天机器人"变成"后台工作线程"。设一个目标就去跑，人不用盯着。

| 命令 | 作用 |
|------|------|
| `/goal [描述]` | 开始自主执行 |
| `/goal status` | 查看执行进度 |
| `/goal pause` | 暂停（不丢上下文） |
| `/goal resume` | 继续执行 |
| `/goal clear` | 结束当前目标 |
| `/subgoal [文本]` | 执行中添加新条件 |

### 配置执行深度

```bash
# 默认 max_turns 是 5-10，太浅了

# 研究/报告/内容草稿
hermes config set goals.max_turns 20

# 代码重构/多步骤构建
hermes config set goals.max_turns 50

# 别随手设 100，每步都花钱
```

### 真实使用场景

**过夜运行（最能体现价值的使用方式）：**
1. 睡觉前发 `/goal research the top 5 design tools shipping multi-agent design in 2026, summarize their differentiators, and draft a comparison post`
2. 设 `max_turns: 30`
3. 睡觉
4. 起床 → 一篇完整的草稿等你看

> 一句话：**把原本吃掉你整个早晨的工作，在咖啡前就做完了。**

---

## 📊 Dashboard & Kanban 看板

```bash
hermes dashboard    # 在浏览器打开 localhost:9119
```

**第一个建议：** 打开后点击 **Skills**，不是 Models。运行良好的 Hermes 会积累上百个针对你工作流的 skill，全部是可读的 markdown 文件。

### Kanban 工作流

Hermes daemon（v0.16+）每 60 秒检查新任务。

1. 把早上的待办清单丢进 **Triage** 列
2. Hermes 自动读取每个任务，拆成子任务，分配给 sub-agent
3. sub-agent 并行执行
4. 到中午大部分已移到 **Done** 或等你的审批

> 这一刻 Hermes 不再是一个"工具"，而是一个**你管理的团队**。你编排，agent 执行。

**Browser Automation / Computer Use** 默认关闭（安全原因），可在 Dashboard 中按 profile 开启。

---

## 🔄 Hermes vs Claude Code：什么时候用什么？

这是每个 builder 第一反应会问的问题。最清晰的答案：

| 场景 | 用 Claude Code | 用 Hermes |
|------|---------------|-----------|
| 深度编码 | ✅ 扎根复杂应用的聚焦编码 | ❌ |
| 单仓库持久上下文 | ✅ CLAUDE.md 足够胜任 | ❌ |
| 单次可交付功能 | ✅ 一次会话能 ship 的 | ❌ |
| 最强编码模型 | ✅ 完整 plan mode + verification | ❌ |
| 研究/文档/排期/业务分析 | ❌ | ✅ |
| 自主运行数小时或过夜 | ❌ | ✅ /goal |
| 手机上访问 agent | ❌ | ✅ Telegram |
| 跨周累积的工作流 | ❌ | ✅ 内容/财务/研究 |
| 多个专业 agent 并行 | ❌ | ✅ Profiles |

**诚实答案：两个都跑。** Claude Code 留在编码循环里，Hermes 处理编码之外的一切——运营、研究、草稿、审查、对账。

> 这不是换掉你现有的工具，而是**补齐你缺少的那一半栈。**

---

## 🛡️ 安全配置

### Day 1 安全基线

```bash
# SOUL.md 加一句
# "Never send money to anyone without explicit confirmation."

# 命令审批
hermes config set safety.command_approval true

# 限制 Telegram 用户
hermes config set gateway.allowed_users @yourusername
```

### 生产部署安全

生产环境需要以下配置才能放心让 agent 接触真实凭证：

```bash
# Bitwarden 密钥管理
hermes secrets bitwarden setup

# Egress 防火墙（限制出站）
hermes egress install

# Browser/Computer use 仅开给需要的 profile
# 从 Dashboard → 按 profile 开启
```

---

### 安装 & 更新

```bash
hermes setup           # 设置向导
hermes model           # 选择模型
hermes doctor          # 诊断问题
hermes update          # 升级到最新版
hermes version         # 查看版本
```

### 配置

```bash
hermes config          # 查看配置
hermes config edit     # 编辑配置
hermes config set KEY VAL   # 设值（API key → .env，其余 → config.yaml）
hermes config check    # 检查遗漏选项
hermes config migrate  # 交互式补全缺失配置
```

### 终端

```bash
hermes                 # 启动 TUI 对话
hermes chat            # 启动 CLI 对话
hermes chat --model openrouter/anthropic/claude-sonnet-4  # 临时指定模型
```

### 消息网关

```bash
hermes gateway              # 查看状态
hermes gateway setup        # 配置
hermes gateway start        # 启动（前台）
hermes gateway start --daemon --platforms telegram  # 后台启动 Telegram
hermes gateway stop         # 停止
```

### 工具

```bash
hermes tools           # 查看/配置工具
hermes tools enable web_search
hermes tools enable file_editor
```

### Skills

```bash
hermes skills          # 列出所有技能
# 聊天中使用 /skill-name 或 /skills 浏览
```

### Cron

```bash
hermes cron list       # 列出定时任务
hermes cron pause NAME
hermes cron resume NAME
hermes cron remove NAME
```

### 迁移

```bash
hermes claw migrate              # 从 OpenClaw 迁移
hermes claw migrate --dry-run    # 预览
```

### Subagent（异步委托）

```bash
# 最新特性（v0.16+）：异步 subagent — delegate 不再阻塞聊天
# Hermes 在后台派生子 agent 并行工作，你可以继续聊天
# 使用 dashboard 或 /goal status 查看进度
hermes update  # 确保升级到最新版
```

### Stripe 集成（2026年6月新功能）

```bash
# Hermes + Stripe 合作：agent 可以直接购买、支付 API、自动订阅 SaaS
# 每个操作有可配置的安全限额
hermes config set stripe.enabled true
hermes config set stripe.max_transaction_amount 100  # 单笔限额（美元）
```

### 目录结构

```
~/.hermes/
├── config.yaml     # 设置（模型、终端、TTS、压缩等）
├── .env            # API keys 和密钥
├── auth.json       # OAuth 凭证（Nous Portal 等）
├── SOUL.md         # 身份层（slot #1 in system prompt）
├── memories/       # 持久记忆（MEMORY.md, USER.md）
│   ├── MEMORY.md
│   └── USER.md
├── profiles/       # 多 profile 配置
│   ├── chief-of-staff/
│   ├── head-of-research/
│   └── head-of-content/
├── skills/         # 技能（自动创建 + 手动管理）
├── cron/           # 定时调度
├── sessions/       # Gateway 会话
└── logs/           # 日志（error.log, gateway.log — 密钥自动打码）
```

---

## 疑难解答

### 安装失败

```bash
# 常见原因
1. python3 版本 < 3.10 → 升级 Python
2. curl 未安装 → apt install curl / brew install curl
3. 磁盘空间不足 → df -h ~，清理空间
4. 网络问题 → 使用代理或切换镜像

# 详细诊断
hermes doctor
```

### Gateway 连接问题

```bash
# Telegram Bot 不响应
1. 确认 Bot Token 正确 → 在 Telegram 中 /mybots 查看
2. 确认网关正在运行 → hermes gateway
3. 检查日志 → cat ~/.hermes/logs/gateway.log
4. 防火墙 → 确保出站连接正常

# 如需重启
hermes gateway stop
hermes gateway start --daemon
```

### 模型/API 问题

```bash
# 切换模型
hermes model                          # 交互式选择
hermes config set model openrouter/anthropic/claude-sonnet-4

# 查看可用模型列表
hermes model list

# 测试连接
hermes chat --model openrouter/anthropic/claude-sonnet-4 --single-turn "hello"
```

---

## 参考链接

- [Official Hermes Agent Repo](https://github.com/NousResearch/hermes-agent) — ⭐ 185K+
- [Official Docs](https://hermes-agent.nousresearch.com/docs/)
- [@zaimiri 7-Day Setup Guide](https://x.com/zaimiri/status/2066117404392890835) — 渐进式搭建法
- [@PrajwalTomar_ Deep Hermes Breakdown](https://x.com/PrajwalTomar_/status/2064324584254710262) — Hermes vs Claude Code, /goal, Dashboard, SOUL.md 模板
- [Nous Portal](https://portal.nousresearch.com) — 一站式模型 + 工具网关订阅
- [Hermes Agent SDK](https://github.com/mz2/hermes-agent-sdk) — Workshop SDK
- [Hermes Self-Evolution](https://github.com/NousResearch/hermes-agent-self-evolution) — DSPy + GEPA 自我进化
- [AgentSkills.io](https://agentskills.io) — 开放式 skill 标准
- [Hermes Desktop](https://hermes-agent.nousresearch.com/) — 桌面版应用
- [Nous Research (@NousResearch)](https://x.com/NousResearch) — 官方 Twitter
- [Teknium (@Teknium)](https://x.com/Teknium) — Hermes 核心开发者，异步 subagent 公告
