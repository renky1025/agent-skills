---
name: video-minutes
description: |
  智能视频纪要生成器 - 自动提取视频语音、生成字幕、智能分类总结，输出结构化纪要文档

  **MUST use this skill when user mentions:**
  - 处理视频、生成视频纪要、视频转文字、视频总结
  - 会议录像整理、网课笔记、视频内容提取
  - "帮我总结这个视频"、"提取视频字幕"、"视频转笔记"
  - 录屏整理、直播回放分析、培训视频归档

  **支持的视频类型 (auto-detected):**
  - meeting: 会议录像 → 待办事项 + 决议 + 负责人
  - lecture: 课程/讲座 → 知识点图谱 + 时间戳
  - interview: 访谈/采访 → Q&A 整理 + 观点对比
  - presentation: 演讲/汇报 → 核心论点 + 数据可视化
  - podcast: 播客/对话 → 金句摘录 + 话题索引
  - tutorial: 教程/演示 → 步骤清单 + 关键截图提示

  **支持的数据源:**
  - 本地视频文件 (.mp4/.mov/.mkv/.avi)
  - Zoom 录制自动扫描
  - 腾讯会议/钉钉录制
  - YouTube/B站链接 (yt-dlp)
  - 网盘分享链接 (阿里云盘/百度网盘)

  **Do NOT use when:**
  - 仅需视频转文字无总结需求 (直接用 whisper)
  - 视频无音频轨道或音频质量极差
  - 实时视频流处理 (需先录制)
  - 视频时长超过 4 小时 (建议分段处理)

  **触发关键词:** video, 视频, 纪要, 字幕, 总结, meeting, 会议, 课程
---

# Video Minutes Skill

智能视频纪要生成器，支持多类型视频自动分类、智能总结、任务分发。

## 核心特性

- 🤖 **AI 自动分类**: 自动识别视频类型（会议/课程/访谈等），应用对应模板
- 📝 **智能总结**: 提取核心要点、行动项、关键决策
- 🏷️ **任务分发**: 通过 @tags 将待办分发给其他 skill 执行
- 🔗 **多源支持**: 本地文件、Zoom/腾讯会议录制、在线视频链接
- 🌐 **多语言**: 自动检测语言，支持中英日等 99+ 语言
- 📊 **多种输出**: Markdown/Obsidian/Notion/飞书文档

---

## 首次设置 (First-Time Setup)

**配置优先级检测**:

```bash
# 检测配置文件存在性
test -f ".opencode/skills/video-minutes/config.yaml" && echo "project"
test -f "$HOME/.opencode/skills/video-minutes/config.yaml" && echo "user"
test -f "$HOME/.video-minutes-config.json" && echo "legacy"
```

| 结果 | 操作 |
|------|------|
| 找到 YAML | 读取并应用 |
| 找到 legacy JSON | 迁移到 YAML 格式 |
| 未找到 | **执行首次设置向导** (阻塞操作) |

### 首次设置向导 (BLOCKING)

**⚠️ CRITICAL**: 未检测到配置文件时，**必须**先完成设置向导，**阻塞**后续所有视频处理操作。

使用 `AskUserQuestion` 一次性呈现所有问题，等待用户回答后再继续。

---

**🎬 Video Minutes 配置向导**

```
让我为您配置视频纪要生成的默认偏好：

**1. 默认输出语言**
视频语音通常为哪种语言？
- 🌐 自动检测 (推荐)
- 🇨🇳 中文
- 🇺🇸 英文
- 🇯🇵 日文
- 其他: __________

**2. Whisper 模型选择**
语音转文字精度 vs 速度偏好？
- ⚡ Tiny (最快，适合快速预览)
- 🚀 Base (推荐，平衡速度质量)
- 🎯 Small (更精准，慢 2x)
- 🏆 Medium (高精度，慢 4x)
- 💎 Large (最佳质量，慢 8x，需 GPU)

**3. 输出格式偏好**
纪要文档保存为哪种格式？
- 📝 Markdown (推荐，通用)
- 📔 Obsidian (带双链和标签)
- 📊 Notion (自动同步到数据库)
- 🚀 飞书文档 ( Lark )

**4. 输出内容选项**
纪要包含哪些内容？(多选)
- ✅ 内容摘要 (一句话总结)
- ✅ 核心要点 (分点列出)
- ✅ 详细时间线 (带时间戳)
- ✅ 行动项追踪 (TODO 列表)
- ✅ 完整字幕 (可选折叠)
- ✅ 发言人识别 (如果可区分)

**5. 自动扫描路径** (可选)
自动监控哪些目录的新视频？
- 📹 Zoom 录制文件夹
- 📹 腾讯会议录制
- 📹 钉钉会议录制
- 📂 自定义路径: __________

**6. 任务分发集成**
检测到行动项时如何分发？
- ❓ 先问我确认 (推荐)
- 🤖 自动分发到对应 skill
- 📋 仅汇总列出，不分发

**7. 视频类型偏好**
您最常处理的视频类型？
- 💼 会议录像 (提取 TODO)
- 📚 课程讲座 (知识笔记)
- 🎙️ 访谈播客 (Q&A 整理)
- 🎤 演讲汇报 (观点提炼)
- 🛠️ 教程演示 (步骤清单)
```

**配置保存路径**: `~/.opencode/skills/video-minutes/config.yaml`

```yaml
# config.yaml 示例
version: "1.1.0"

output:
  language: auto  # auto/zh/en/ja
  format: obsidian  # markdown/obsidian/notion/lark
  directory: "~/Documents/video-minutes"
  filename_template: "{date}-{type}-{title}"

content:
  include_summary: true
  include_key_points: true
  include_timeline: true
  include_action_items: true
  include_transcript: true
  transcript_collapsed: true  # 默认折叠
  speaker_identification: true
  max_summary_points: 10

whisper:
  model: base  # tiny/base/small/medium/large/large-v1/large-v2/large-v3
  device: auto  # auto/cpu/cuda/mps
  compute_type: int8  # int8/int8_float16/float16/float32
  language: null  # null=auto

classification:
  enabled: true
  confidence_threshold: 0.7

dispatch:
  confirm_before_dispatch: true
  auto_dispatch_tags: ["@reminder"]  # 自动分发的标签

scanning:
  enabled: true
  interval_minutes: 60
  paths:
    - "~/Documents/Zoom"
    - "~/Documents/腾讯会议"

integrations:
  obsidian_vault: "~/Obsidian/VideoNotes"
  notion_database_id: null
  lark_webhook: null
```

---

## 使用方法

### 命令行用法

```bash
# 基本用法
python .opencode/skills/video-minutes/generate_minutes.py <视频路径>

# 指定类型 (跳过自动分类)
python .opencode/skills/video-minutes/generate_minutes.py meeting.mp4 --type meeting

# 指定输出
python .opencode/skills/video-minutes/generate_minutes.py lecture.mp4 -o ~/Notes/课程.md

# 指定语言
python .opencode/skills/video-minutes/generate_minutes.py interview.mp4 --language zh

# 使用更高精度模型
python .opencode/skills/video-minutes/generate_minutes.py presentation.mp4 --model medium

# 仅提取字幕不生成纪要
python .opencode/skills/video-minutes/generate_minutes.py video.mp4 --transcript-only

# 批量处理目录
python .opencode/skills/video-minutes/generate_minutes.py ~/Recordings/ --batch
```

### 自动扫描

```bash
# 扫描配置路径中的新视频
python .opencode/skills/video-minutes/scripts/scan-and-process.py

# 扫描指定目录
python .opencode/skills/video-minutes/scripts/scan-and-process.py ~/Downloads --since-hours 24

# 查看待处理队列
python .opencode/skills/video-minutes/scripts/queue.py --list

# 查看处理统计
python .opencode/skills/video-minutes/scripts/queue.py --stats
```

---

## 视频类型分类系统

### 自动分类逻辑

```
视频文件
    ↓
音频指纹分析 + 内容采样
    ↓
分类模型 (Gemini/本地模型)
    ↓
类型判断 + 置信度评分
    ↓
选择对应模板生成纪要
```

### 分类维度

| 维度 | 检测指标 | 影响 |
|------|----------|------|
| **说话人数量** | 单/双/多人 | note/podcast vs meeting/interview |
| **对话模式** | 独白/问答/讨论 | lecture vs interview vs meeting |
| **内容特征** | 任务/知识点/观点 | 提取 TODO vs 知识图谱 vs 金句 |
| **视觉线索** | PPT/白板/屏幕分享 | presentation vs tutorial |
| **时长** | <15min/15-60min/>60min | 详略程度 |

### 7 种视频类型

#### 1. Meeting (会议录像)
**特征**: 多人参与、任务分配、决策讨论
**输出重点**:
- 参会人员列表
- 核心决议清单
- 行动项追踪表（含负责人、截止日期）
- 待跟进事项

**模板**: `templates/meeting.md`

```markdown
# 会议纪要: {{title}}

## 📋 会议信息
- **日期**: {{date}}
- **时长**: {{duration}}
- **参会人**: {{participants}}
- **视频**: {{video_path}}

## 🎯 核心决议
{{decisions}}

## ✅ 行动项
| 任务 | 负责人 | 截止日期 | 优先级 |
|------|--------|----------|--------|
{{action_items}}

## 📍 关键时间节点
{{timeline}}

## 💬 重要讨论摘要
{{discussion_summary}}

---
{{#if include_transcript}}
<details>
<summary>📝 完整字幕 (点击展开)</summary>

{{transcript}}
</details>
{{/if}}
```

#### 2. Lecture (课程/讲座)
**特征**: 单/双主讲人、结构化内容、知识点密集
**输出重点**:
- 课程大纲/目录
- 核心概念图谱
- 重点摘录（带时间戳）
- 延伸阅读建议

**模板**: `templates/lecture.md`

```markdown
# 📚 课程笔记: {{title}}

## 📖 课程信息
- **讲师**: {{speaker}}
- **时长**: {{duration}}
- **主题**: {{topics}}

## 🗺️ 知识图谱
```mermaid
{{knowledge_graph}}
```

## ⏱️ 章节速览
{{chapters}}

## 📝 核心概念
{{key_concepts}}

## 💡 重点摘录
{{key_quotes}}

## ❓ 疑问与思考
{{questions}}

## 🔗 延伸阅读
{{references}}
```

#### 3. Interview (访谈/采访)
**特征**: 问答形式、双方观点、深入探讨
**输出重点**:
- Q&A 结构化整理
- 双方核心观点对比
- 金句摘录
- 话题索引

**模板**: `templates/interview.md`

#### 4. Presentation (演讲/汇报)
**特征**: PPT 辅助、数据展示、观点阐述
**输出重点**:
- 核心论点（金字塔结构）
- 关键数据/图表描述
- 结论与建议
- 演讲技巧点评（可选）

**模板**: `templates/presentation.md`

#### 5. Podcast (播客/对话)
**特征**: 轻松对话、话题跳跃、金句频出
**输出重点**:
- 话题时间索引
- 金句摘录
- 推荐片段（高光时刻）
- 相关资源链接

**模板**: `templates/podcast.md`

#### 6. Tutorial (教程/演示)
**特征**: 步骤演示、操作指导、屏幕录制
**输出重点**:
- 步骤清单（可勾选）
- 关键截图提示
- 常见问题/踩坑点
- 快捷键/命令汇总

**模板**: `templates/tutorial.md`

#### 7. Note (个人录屏/语音备忘)
**特征**: 自言自语、快速记录、想法片段
**输出重点**:
- 清理格式化文本
- 想法归类标签
- 待办提取
- 关联笔记链接

**模板**: `templates/note.md`

---

## 任务分发系统 (@tags)

### 提取标签规则

AI 从视频中提取行动项时，自动识别并添加 @tags:

| Tag | 触发条件 | 分发给 |
|-----|----------|--------|
| `@user` | 指派给具体人员 | 用户通知 |
| `@assistant` | 需要 AI 执行 | 内置工具 |
| `@Codex` | 代码相关任务 | agent-swarm |
| `@Claude` | 前端/设计任务 | agent-swarm |
| `@article` | 需要写文章 | content-publisher |
| `@reminder` | 需要提醒 | cron/gcal |
| `@research` | 需要调研 | web_search |
| `@design` | 需要设计稿 | image-gen |
| `@meeting` | 需要安排会议 | calendar |
| `@review` | 需要审核 | 通知相关人员 |

### 确认机制流程

```
视频处理完成
    ↓
提取行动项 + 自动标记 @tags
    ↓
向用户展示提取结果
    ↓
用户确认/修改/取消
    ↓
分发到对应 skill 执行
    ↓
更新任务追踪状态
```

### 示例交互

**AI**: 已从会议视频中提取以下行动项：

```markdown
### @Codex
- [ ] 实现用户认证模块的 JWT 刷新机制 (deadline: 周五)
- [ ] 优化数据库查询性能，目标 QPS > 1000

### @article
- [ ] 撰写"微服务架构实践"技术博客 (deadline: 下周四)

### @reminder
- [ ] cron: 0 10 * * 1 周报提醒
- [ ] 2026-04-01 跟进 Q2 OKR 进度

### @meeting
- [ ] 安排下周与产品团队的评审会
```

**用户**: 第1项改成 @张三，第2项优先级降低

**AI**: ✅ 已更新，确认分发吗？

**用户**: 确认

**AI**: 🚀 正在分发任务...
- ✅ @Codex 任务已发送至 agent-swarm
- ✅ @article 草稿已创建在 ~/Drafts/
- ✅ @reminder 已添加到 cron
- ✅ @meeting 会议邀请已发送到日历

---

## 数据源集成

### 已支持

| 来源 | 接入方式 | 自动扫描 |
|------|----------|----------|
| 本地视频文件 | 直接路径 | ❌ |
| Zoom 录制 | `~/Documents/Zoom` | ✅ |

### 计划中

| 来源 | 接入方式 | 状态 |
|------|----------|------|
| 腾讯会议 | `~/Documents/腾讯会议` | 🔜 |
| 钉钉会议 | 自定义路径 | 🔜 |
| YouTube | yt-dlp + URL | 🔜 |
| Bilibili | yt-dlp + URL | 🔜 |
| 阿里云盘 | 分享链接解析 | 🔜 |
| 百度网盘 | 分享链接解析 | 🔜 |
| Google Drive | API 集成 | 🔜 |

---

## 输出格式详情

### Markdown (默认)

标准 Markdown 格式，兼容所有编辑器。

### Obsidian

```markdown
---
date: {{date}}
type: {{video_type}}
tags: [video-minutes, {{type_tag}}]
source: {{video_path}}
duration: {{duration}}
---

# {{title}}

## 关联笔记
- [[相关笔记1]]
- [[相关笔记2]]

## 内容
{{content}}

## 行动项
- [ ] #task 任务1 @{{assignee}}
```

### Notion

自动创建数据库条目，包含：
- 标题、日期、类型、时长
- 内容块（Toggle 列表）
- 行动项（Checkbox）
- 嵌入视频链接

### 飞书文档

调用 Lark API 创建文档，支持：
- 富文本格式
- @提及用户
- 插入任务清单

---

## 依赖安装

### 必需依赖

```bash
# ffmpeg
brew install ffmpeg              # macOS
sudo apt install ffmpeg          # Ubuntu
winget install Gyan.FFmpeg       # Windows

# Python 依赖
pip install -r requirements.txt
```

### requirements.txt

```
# 🚀 insanely-fast-whisper (高性能转录)
faster-whisper>=1.0.0

# 其他依赖
ffmpeg-python>=0.2.0
pyyaml>=6.0
requests>=2.31.0
notion-client>=2.2.1
yt-dlp>=2023.12.30
onnxruntime>=1.16.0
torch>=2.0.0
```

---

## 性能优化

### insanely-fast-whisper 优势

基于 [faster-whisper](https://github.com/SYSTRAN/faster-whisper)，比原始 Whisper **快 2-4 倍**：

| 特性 | openai-whisper | faster-whisper |
|------|----------------|----------------|
| **速度** | 1x (基准) | 2-4x ⚡ |
| **内存** | 较高 | 降低 50% 💾 |
| **精度** | 标准 | 相同 ✓ |
| **量化** | float32 | int8/int16 🔧 |
| **VAD** | 无 | 内置 🎙️ |

### 模型选择建议

| 模型 | 显存需求 | 适合场景 |
|------|----------|----------|
| `tiny` | ~1GB | 快速预览、实时测试 |
| `base` | ~1GB | **推荐**，平衡速度质量 |
| `small` | ~2GB | 更精准，慢 2x |
| `medium` | ~5GB | 高精度，慢 4x |
| `large-v3` | ~10GB | 最佳质量，慢 8x |

### 设备与精度配置

```yaml
whisper:
  device: auto        # auto/cpu/cuda/mps
  compute_type: int8  # int8/int8_float16/float16/float32
```

- **int8**: 最快，内存占用最小，质量损失极小
- **float16**: 更快，需要 GPU
- **float32**: 标准精度

---

## 目录结构 (更新)

```
opencode/skills/video-minutes/
├── SKILL.md                          # 本文件
├── config.yaml                       # 默认配置模板
├── README.md                         # 快速开始指南
├── requirements.txt                  # Python 依赖 ⭐
├── scripts/
│   ├── generate_minutes.py           # 主入口 ⭐
│   ├── insanely_fast_transcriber.py  # 高性能转录器 ⭐ NEW
│   ├── video_processor.py            # 视频处理
│   ├── classifier.py                 # 视频类型分类
│   ├── config_manager.py             # 配置管理
│   └── dispatcher.py                 # 任务分发
├── templates/                        # 类型特定模板
│   ├── meeting.md
│   ├── lecture.md
│   ├── interview.md
│   ├── presentation.md
│   ├── podcast.md
│   ├── tutorial.md
│   └── note.md
└── references/
    └── config/
        └── config-schema.md          # 配置 schema
```

---

## 依赖安装

### 必需依赖

```bash
# ffmpeg
brew install ffmpeg              # macOS
sudo apt install ffmpeg          # Ubuntu
winget install Gyan.FFmpeg       # Windows

# Python 依赖
pip install -r requirements.txt
```

### requirements.txt

```
openai-whisper>=20231117
ffmpeg-python>=0.2.0
pyyaml>=6.0
requests>=2.31.0
notion-client>=2.2.1
yt-dlp>=2023.12.30
```

---

## 配置参考

### 完整配置项

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `output.language` | string | "auto" | 输出语言 |
| `output.format` | string | "markdown" | 输出格式 |
| `output.directory` | string | "~/video-minutes" | 输出目录 |
| `whisper.model` | string | "base" | 转录模型 |
| `whisper.device` | string | "auto" | 计算设备 |
| `classification.enabled` | bool | true | 启用分类 |
| `dispatch.confirm_before_dispatch` | bool | true | 分发前确认 |
| `scanning.enabled` | bool | true | 启用自动扫描 |
| `scanning.interval_minutes` | int | 60 | 扫描间隔 |

---

## 故障排除

### 常见问题

**Q: Whisper 下载模型失败**
A: 设置镜像 `export WHISPER_MIRROR=https://hf-mirror.com`

**Q: 视频无音频**
A: 检查视频编码 `ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1 input.mp4`

**Q: 分类不准确**
A: 手动指定类型 `--type meeting` 或调整 `classification.confidence_threshold`

**Q: 处理超时**
A: 长视频建议分段 `--segment-duration 1800` (30分钟一段)

---

## 相关 Skill

| Skill | 关系 |
|-------|------|
| `agent-swarm` | 接收 `@Codex` `@Claude` 代码任务 |
| `content-publisher` | 接收 `@article` 文章任务 |
| `cron` / `gcal` | 接收 `@reminder` 提醒任务 |
| `elyfinn-voice-notes` | 语音备忘录处理 (姊妹 skill) |
| `transcribe` | 纯转录功能 (无总结) |

---

## 版本历史

### v2.0.0 (2026-03-25) - 当前
- 🚀 **新增 insanely-fast-whisper 支持** - 基于 faster-whisper，速度提升 2-4 倍
- ⚡ **性能优化** - 支持 int8 量化、VAD 过滤、词级时间戳
- 💾 **内存优化** - 显存占用降低 50%
- 🔧 **新配置项** - `compute_type` 支持多种精度模式

### v1.2.0 (2026-03-21)
- ✅ 新增视频类型自动分类系统 (7种类型)
- ✅ 新增任务分发集成 (@tags)
- ✅ 新增 Obsidian/Notion/飞书多格式输出
- ✅ 新增首次设置向导
- ✅ 新增自动扫描队列系统
- ✅ 新增发言人识别

### v1.1.0 (2026-03-15)
- 🔧 重构配置系统 (YAML 格式)
- 🔧 支持多语言自动检测
- 🔧 优化 Whisper 模型选择逻辑

### v1.0.0 (2026-03-01)
- 🎉 初始版本
- ✅ 基础视频转文字
- ✅ Markdown 纪要生成
- ✅ 命令行接口

---

## Roadmap

- [ ] 实时转录 (直播场景)
- [ ] 多模态分析 (PPT 内容提取)
- [ ] 视频摘要生成 (短视频)
- [ ] 团队协作功能 (共享队列)
- [ ] 移动端支持 (iOS Shortcuts)
