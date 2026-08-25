# agent-skills 技能库升级优化审计报告

- **审计时间**：2026-08-25
- **审计范围**：`/Users/kyren/workspace/agent-skills/` 下 26 个顶层用户技能（infocard 自带的 `.agents/skills`、`node_modules` 视为第三方依赖，不计入）
- **审计方法**：逐技能读取 `SKILL.md` 及实现文件，核验被引用的脚本 / 兄弟技能 / 外部依赖 / README 一致性；交叉比对功能重叠。
- **结论置信度**：高（关键事实已实机核验）

---

## 结论先行（TL;DR）

1. **仓库快照与运行环境不一致，是头号治理问题。** README 引用了 6 个仓库里不存在的技能（`frontend-design`、`life-quotes`、`material-to-slides`、`viral-hook` 等），而仓库里又有 4 个技能 README 完全没列（`black-humor-writing`、`clean-code`、`edulab`、`obsidian-kb-builder`）。其中 `viral-hook` / `translate-polisher` 在用户的真实 WorkBuddy 运行环境里是已安装技能，只是没提交进这个仓库——所以"悬空引用"多数是**快照不完整**，不应简单删除引用。
2. **内容质量整体偏高。** 6 个技能达到标杆级（5/5），11 个良好（4/5），仅 8 个存在可用性或一致性缺陷（3/5）。没有发现会直接崩溃的硬 bug。
3. **最需要做的三件事**：
   - 重写 / 脚本化生成 README，使其与仓库目录严格一致；
   - 建立"仓库即唯一真源"的治理约定（缺失技能要么补提交、要么在文档里标注运行时依赖）；
   - 统一安装基路径与 frontmatter 规范（当前混用 `~/.claude/skills`、`~/.workbuddy/skills`、`~/.ai-agent/skills` 三套，且 `hermes-setup/skill.md` 小写文件名在大小写敏感 FS 上无法被识别）。

> 校准提示：`github-analyzer` 硬编码的 `http://127.0.0.1:7890` 恰好是用户真实代理，对它而言**不是 bug，是可移植性隐患**；同理 `infocard` 的 `both` 双语模式依赖 `translate-polisher`，在真实环境里可用。下面的建议据此重新定性。

---

## 一、整体质量评分卡

| 等级 | 技能 | 一句话评价 |
|------|------|-----------|
| **5/5 标杆** | `claude-simplify` | 三 Agent 并行审查范式，结构极清晰，无实现依赖 |
| | `curriculum-design` | OBE + 布鲁姆六层次，7 步流程 + 双模板，内容质量标杆 |
| | `de-ai-writing` | 去 AI 味五步法 + 11 类 AI 味，权威真源 |
| | `snowflake-novel-writer` | 雪花写作 10 步 + 反俗套 + references，最完整的小说技能 |
| | `grasp` | 十维认知框架 × 加速学习协议，7 阶段完整闭环 |
| | `clean-code` | 17 章知识库 + 索引 + 跨语言映射，结构标杆 |
| **4/5 良好** | `article-deconstructor` | 10 维拆解，模板清晰，缺真实示例 |
| | `mlx-tts` | Mac 本地 TTS 全流程，绑定 `mlx-audio`（Mac-only） |
| | `design-md-extractor` | 设计系统提取 + DESIGN.md 规范，严谨 |
| | `video-dubbing` | 译制管线完整，TTS 第三步绑定 Mac |
| | `llm-aiops` | 78+ 论文参考库，静态、偏英文 |
| | `claude-remember` | 跨记忆层整理，流程清晰 |
| | `image-design` | 摄影逻辑提示词，实用无依赖 |
| | `weitoutiao-creator` | 微头条 6 步 + evals，引用缺失的 `viral-hook` |
| | `mckinsey-cover` | 咨询封面提示词，专业 |
| | `obsidian-kb-builder` | Karpathy Wiki 模式，脚本齐全，`<skill>` 占位符待参数化 |
| | `novel-writing` | LOCK + 三幕，与 snowflake 高度相邻 |
| | `black-humor-writing` | 黑色幽默五步 SOP，区分度清晰 |
| **3/5 待修** | `skill-security-check` | 文档（手动 grep）与实现（src/ + security-check.js）双轨脱节 |
| | `infocard` | 成熟，但 `both` 依赖 `translate-polisher`、`capture_dsh.js` 死文件 |
| | `github-analyzer` | 写死代理 `127.0.0.1:7890`（用户真实代理，但不可移植） |
| | `pdf2md` | SKILL.md 伪代码与 `pdf2md.py` 重复漂移；强依赖未核实的外部包 |
| | `video-minutes` | 体量偏大，任务分发引用 7 个缺失兄弟技能 |
| | `wechat-article-writer` | **`disable: true` 被禁用**，内容高质量却闲置，引用缺失 `viral-hook` |
| | `edulab` | 脚本路径写死 `/Users/kyren/...`，不可移植 |
| | `hermes-setup` | 文件名小写 `skill.md` + 与其他技能定位偏"孤儿文档" |

---

## 二、跨技能功能重叠与去重

| 功能簇 | 涉及技能 | 重叠度 | 建议 |
|--------|----------|--------|------|
| 去 AI 味 | `de-ai-writing` + `snowflake-novel-writer`(去AI味三遍法) + `wechat-article-writer`(avoid-ai-writing.md) | **高** | 以 `de-ai-writing` 为唯一真源，其余改引用，删除本地副本 |
| 小说创作 | `novel-writing` + `snowflake-novel-writer` | **高** | 明确分工（快速骨架用 novel-writing，精细长写用 snowflake），或合并 |
| 自媒体 / 短文案 | `wechat-article-writer` + `weitoutiao-creator` + `de-ai-writing` + (运行时 `viral-hook`) | **高** | 建立"长文→wechat、短内容→weitoutiao、去味→de-ai、评论钩子→viral-hook"导航；清理 disable 与缺失引用 |
| AI 图片提示词 | `image-design` + `mckinsey-cover` | 中 | 各加"彼此分工"说明，低优先级合并 |
| 图片类产物 | `infocard` + `mckinsey-cover` | 低-中 | 区分清晰，仅互链 |
| 视频处理 | `video-minutes`(纪要) + `video-dubbing`(译制) | 低 | 功能不同，互链即可 |
| 知识 / 笔记 | `obsidian-kb-builder` + `grasp` + `article-deconstructor` | 低 | 合适处互链 |
| 代码质量 | `claude-simplify` + `clean-code` | 互补 | 互链即可，无重复 |
| 安全 | `skill-security-check` | 独立 | — |

**最大去重收益**：「去 AI 味」规则在 3 处各自复制，维护时极易不一致；「小说 / 自媒体写作」有 2-3 个相邻技能，其中 `wechat-article-writer` 还被禁用又引用缺失技能，是最该梳理的一组。

---

## 三、优先级升级建议

### 🔴 高优先级（治理 / 可移植性，影响整体可用性）

1. **重写 README，与仓库目录严格对齐**
   - 现状：README 列了 6 个仓库不存在的技能，漏了 4 个存在的技能；且 `frontend-design` 写成在 `.staged-skills/`（该目录实际也不存在）。
   - 动作：按当前顶层目录重新生成目录表与项目结构图；建议用脚本（如 `ls -d */` 生成）避免再次漂移。

2. **明确"仓库即唯一真源"的治理约定**
   - 现状：`viral-hook` / `translate-polisher` 在用户运行环境存在但未提交进仓库，导致 README 与多个 SKILL.md 的引用在仓库视角"悬空"。
   - 动作：二选一 —— ① 把这些运行时技能也提交进仓库；② 在 README / 相关 SKILL.md 显式标注"此技能依赖运行时已安装的 X，仓库快照不含"。**不要直接删除引用**，否则真实环境会断链。
   - 真正缺失、运行环境也没有的（`frontend-design`、`life-quotes`、`material-to-slides`）：要么补回，要么从 README 删除。

3. **统一安装基路径约定**
   - 现状：`infocard` 用 `~/.claude/skills/infocard/assets/capture.js`，`edulab` 用 `~/.workbuddy/skills/edulab/...` 且写死 `/Users/kyren/.workbuddy/binaries/...`，`video-minutes` 用 `~/.ai-agent/skills/...`。
   - 动作：全库统一为单一基路径（建议 `~/.workbuddy/skills`），脚本路径改为相对路径或运行时参数；`edulab` 删除 `/Users/kyren/` 绝对路径。

4. **`hermes-setup` 文件名小写 → 重命名 `SKILL.md`**
   - 现状：`hermes-setup/skill.md` 在 Linux / CI / 大小写敏感 FS 上不被识别为技能。
   - 动作：重命名；并统一 frontmatter 的 `stars` 数字（194k 与 185K 不一致）。

### 🟡 中优先级（质量 / 一致性 / 去重）

5. **去重「去 AI 味」内容**
   - 动作：以 `de-ai-writing` 为唯一真源，`snowflake-novel-writer` 与 `wechat-article-writer` 改为引用，删除本地 `anti-ai-writing.md` / `avoid-ai-writing.md` 副本（或建立双向同步机制）。

6. **`skill-security-check` 文档与实现对齐**
   - 现状：SKILL.md 描述手动 grep 流程，但 `src/` 与 `scripts/security-check.js` 才是工具且未被引用；`package.json` 指向未提交的 `dist/`。
   - 动作：SKILL.md 写明调用入口（建议以 `scripts/security-check.js` 为唯一入口），或补充 `npm run build` 步骤；清理示例报告里引用的不存在技能。

7. **`pdf2md` 精简文档 + 核实依赖**
   - 现状：SKILL.md 大量伪代码与 `pdf2md.py` 重复，易漂移；强依赖外部包 `opendataloader-pdf` 未核实真实性。
   - 动作：删伪代码、改为"调用 `python3 pdf2md/pdf2md.py ...`"并链接源码；核实该 pip 包；统一默认输出路径表述。

8. **`video-minutes` 任务分发降级**
   - 现状：分发系统引用 7 个缺失兄弟技能（`task-dispatcher` / `content-publisher` / `cron` / `gcal` / `transcribe` / `elyfinn-voice-notes` / `agent-swarm`），实际不可达；且体量偏大。
   - 动作：分发目标改为"可选 / 可配置"，缺失时降级为本地 TODO 列表；评估裁剪过度设计的扫描队列。

9. **`wechat-article-writer` 的 `disable: true` 意图确认**
   - 现状：v2.2.0 高质量技能被禁用，且引用缺失的 `viral-hook`。
   - 动作：确认是有意归档还是误留。若启用 → 去掉 `disable` 并清理引用；若归档 → 迁移核心内容到 `weitoutiao-creator` 或删除目录。

10. **`infocard` 清理**
    - 动作：删除未被引用的 `capture_dsh.js`（或说明用途）；`both` 双语模式显式标注"依赖 translate-polisher，缺失时降级为单语"；统一 `capture.js` 路径为参数化。

### 🟢 低优先级（增强 / 打磨）

11. **`novel-writing` 与 `snowflake-novel-writer` 加分工导航**（顶部各加一段"何时用我 vs 另一个"）。
12. **补充触发词结构化区块**：纯提示词技能（`article-deconstructor`、`curriculum-design`、`llm-aiops`、`obsidian-kb-builder`）统一增加 `when_to_use` / 触发词字段，提升自动触发准确率。
13. **`image-design` / `mckinsey-cover` / `infocard` 互链与分工说明**，避免误用。
14. **frontmatter 字段规范化**：约定统一字段集（`name` 必需；`version` / `user_invocable` / `allowed-tools` / `when_to_use` 按需选用），消除 `agent_created` / `disable` / `triggers` 混用。
15. **为内容型技能各补 1 个真实端到端示例**（`curriculum-design`、`black-humor-writing`、`grasp`、`obsidian-kb-builder` 等）。

---

## 四、统一规范建议（可直接落地）

### 4.1 推荐 SKILL.md frontmatter 标准

```yaml
---
name: <skill-name>            # 必需，与目录名一致
description: <一句话 + 触发场景>   # 必需，含触发词利于自动调用
version: "x.y.z"              # 建议统一
user_invocable: true          # 是否可由 /name 触发
when_to_use:                  # 建议：触发词结构化，提升准确率
  - 场景1
  - 场景2
allowed-tools: [...]          # 有脚本/命令依赖时声明
---
```

### 4.2 安装基路径约定

- 全库统一基路径：`~/.workbuddy/skills/<skill>/`
- 脚本内一律用相对路径或运行时参数（如 `<skill>/scripts/xxx.py`），禁止写死 `/Users/kyren/...`
- 外部依赖（pandoc / ffmpeg / mlx-audio 等）在 Prerequisites 段统一声明

### 4.3 README 治理

- 目录表 / 项目结构图由脚本生成，纳入提交前检查，避免再次与目录脱节
- 对"运行时依赖但未提交"的技能，在 README 用统一标记（如 `⚡运行时依赖`）注明

---

## 五、快速行动清单（可直接勾选）

- [ ] 重写 README，与 26 个顶层目录严格一致
- [ ] 决定 `viral-hook` / `translate-polisher` 等运行时技能是否补提交进仓库
- [ ] 删除 / 标注 README 中 4 个真正缺失的技能（frontend-design / life-quotes / material-to-slides 等）
- [ ] `hermes-setup/skill.md` → `SKILL.md`
- [ ] 全库安装基路径统一为 `~/.workbuddy/skills`，`edulab` 去绝对路径
- [ ] `wechat-article-writer` 确认 `disable: true` 意图
- [ ] 「去 AI 味」内容以 `de-ai-writing` 为唯一真源去重
- [ ] `skill-security-check` 文档与实现对齐
- [ ] `pdf2md` 删伪代码、核实 `opendataloader-pdf`
- [ ] `video-minutes` 分发降级为可选 / 本地 TODO
- [ ] `infocard` 删 `capture_dsh.js`，双语模式加依赖标注
- [ ] `novel-writing` ↔ `snowflake-novel-writer` 加分工导航
- [ ] 纯提示词技能补 `when_to_use` 触发词区块

---

## 附录：重点技能问题明细（已实机核验）

- **github-analyzer**：`SKILL.md` 第 18/36/77 行写死 `http://127.0.0.1:7890`。该地址是用户真实代理，**对其可用**；隐患在于换机 / 他人环境直接失败。建议改读环境变量 `GITHUB_PROXY`，缺失时直连并提示。
- **infocard**：第 55/216 行双语模式硬依赖 `/translate-polisher`（运行环境存在，仓库缺失）；顶层 `capture_dsh.js` 未被任何流程引用（死文件）。
- **wechat-article-writer**：第 5 行 `disable: true`，v2.2.0 内容成熟却被禁用；第 36 行引用缺失的 `viral-hook`。
- **hermes-setup**：目录内实际文件为 `skill.md`（小写）；frontmatter `stars: 194k+` 与正文 `185K+` 不一致。
- **edulab**：`scripts/` 下路径写死 `/Users/kyren/.workbuddy/binaries/python/envs/default/bin/python`，仅在精确安装到 WorkBuddy 且该 managed venv 存在时可用。
- **video-minutes**：任务分发引用 7 个仓库（及运行时）均不存在的兄弟技能，分发实际不可达。
