# 首次设置流程 (First-Time Setup)

## 概述

当用户首次使用 video-minutes skill 时，**必须**完成此设置流程。

**触发条件**:
1. 未检测到配置文件 (`~/.opencode/skills/video-minutes/config.yaml`)
2. 检测到 legacy JSON 配置 (`~/.video-minutes-config.json`)

**阻塞性质**: 设置完成前，**禁止**继续任何视频处理操作。

## 设置流程图

```
检测配置文件
    ↓
┌───────────────┐
│  是否存在？    │──NO──→ 显示欢迎消息
└───────────────┘              ↓
    ↓ YES                    询问配置选项
  读取配置                   (AskUserQuestion)
    ↓                          ↓
  继续处理              等待用户回答
                               ↓
                         生成 config.yaml
                               ↓
                         确认保存成功
                               ↓
                         继续处理
```

## 用户交互设计

### 1. 欢迎消息

```
🎬 欢迎使用 Video Minutes！

我是您的智能视频纪要助手，可以帮您：
• 自动提取视频语音并转文字
• 智能分类视频类型（会议/课程/访谈等）
• 生成结构化纪要文档
• 提取行动项并分发任务

首次使用需要一些基本配置，大约需要 1 分钟。
```

### 2. 配置问题 (AskUserQuestion)

**格式**: 使用 multiSelect/singleSelect 提高体验

```typescript
{
  questions: [
    {
      question: "请选择默认输出语言",
      header: "语言设置",
      options: [
        { label: "🌐 自动检测 (推荐)", description: "根据视频语音自动选择" },
        { label: "🇨🇳 中文", description: "固定输出中文" },
        { label: "🇺🇸 英文", description: "固定输出英文" },
        { label: "🇯🇵 日文", description: "固定输出日文" }
      ]
    },
    {
      question: "请选择 Whisper 转录模型",
      header: "转录精度",
      options: [
        { label: "⚡ Tiny (最快)", description: "1x 速度，适合快速预览" },
        { label: "🚀 Base (推荐)", description: "2x 速度，平衡质量" },
        { label: "🎯 Small", description: "4x 速度，更高精度" },
        { label: "🏆 Medium", description: "8x 速度，高精度" },
        { label: "💎 Large", description: "16x 速度，最佳质量，需 GPU" }
      ]
    },
    {
      question: "请选择输出格式",
      header: "文档格式",
      options: [
        { label: "📝 Markdown", description: "通用格式，兼容所有编辑器" },
        { label: "📔 Obsidian", description: "带双链和标签，适合知识库" },
        { label: "📊 Notion", description: "同步到 Notion 数据库" },
        { label: "🚀 飞书文档", description: "适合团队协作" }
      ]
    },
    {
      question: "请选择要包含的内容 (多选)",
      header: "内容选项",
      multiSelect: true,
      options: [
        { label: "✅ 内容摘要", description: "一句话总结" },
        { label: "✅ 核心要点", description: "分点列出关键信息" },
        { label: "✅ 详细时间线", description: "带时间戳的内容分段" },
        { label: "✅ 行动项追踪", description: "TODO 列表" },
        { label: "✅ 完整字幕", description: "可选折叠" },
        { label: "✅ 发言人识别", description: "区分不同说话人" }
      ]
    },
    {
      question: "是否启用任务分发确认？",
      header: "任务分发",
      options: [
        { label: "❓ 先问我确认 (推荐)", description: "展示提取的行动项，等待确认后分发" },
        { label: "🤖 自动分发", description: "自动发送到对应 skill 执行" },
        { label: "📋 仅列出", description: "汇总显示，不主动分发" }
      ]
    }
  ]
}
```

### 3. 处理用户回答

```python
def process_setup_answers(answers):
    """处理用户配置回答"""

    config = {
        "version": "1.1.0",
        "output": {
            "language": map_language(answers[0]),
            "format": map_format(answers[2]),
            "directory": "~/Documents/video-minutes",
            "filename_template": "{date}-{type}-{title}"
        },
        "content": {
            "include_summary": "内容摘要" in answers[3],
            "include_key_points": "核心要点" in answers[3],
            "include_timeline": "详细时间线" in answers[3],
            "include_action_items": "行动项追踪" in answers[3],
            "include_transcript": "完整字幕" in answers[3],
            "transcript_collapsed": True,
            "speaker_identification": "发言人识别" in answers[3],
            "max_summary_points": 10
        },
        "whisper": {
            "model": map_model(answers[1]),
            "device": "auto",
            "language": None
        },
        "classification": {
            "enabled": True,
            "confidence_threshold": 0.7
        },
        "dispatch": {
            "confirm_before_dispatch": answers[4] == "先问我确认",
            "auto_dispatch_tags": ["@reminder"]
        },
        "scanning": {
            "enabled": True,
            "interval_minutes": 60,
            "paths": detect_recording_paths()
        },
        "integrations": {
            "obsidian_vault": None,
            "notion_database_id": None,
            "lark_webhook": None
        }
    }

    # 保存配置
    save_config(config)

    return config
```

### 4. 确认消息

```
✅ 配置已保存到 ~/.opencode/skills/video-minutes/config.yaml

您的设置摘要:
• 🌐 语言: 自动检测
• 🚀 转录模型: Base (推荐)
• 📔 输出格式: Obsidian
• 📁 保存位置: ~/Documents/video-minutes
• ✅ 包含内容: 摘要, 要点, 时间线, 行动项
• ❓ 任务分发: 确认后分发

现在可以开始处理视频了！试试:
• 直接发送视频文件
• 或者说 "帮我总结这个会议录像"
```

## 配置文件生成

### 路径优先级

1. 项目级: `./.opencode/skills/video-minutes/config.yaml`
2. 用户级: `~/.opencode/skills/video-minutes/config.yaml` ⭐ 推荐
3. 旧版兼容: `~/.video-minutes-config.json` (自动迁移)

### 首次设置检查代码

```python
def check_first_time_setup():
    """检查是否需要首次设置"""

    # 检查项目级配置
    if os.path.exists(".opencode/skills/video-minutes/config.yaml"):
        return False, load_config(".opencode/skills/video-minutes/config.yaml")

    # 检查用户级配置
    if os.path.exists(os.path.expanduser("~/.opencode/skills/video-minutes/config.yaml")):
        return False, load_config("~/.opencode/skills/video-minutes/config.yaml")

    # 检查旧版配置 (需要迁移)
    if os.path.exists(os.path.expanduser("~/.video-minutes-config.json")):
        legacy = load_json("~/.video-minutes-config.json")
        migrated = migrate_legacy_config(legacy)
        save_config(migrated)
        return False, migrated

    # 需要首次设置
    return True, None
```

## 重新配置

用户可以通过以下方式重新配置:

```bash
# 命令行重新配置
python .opencode/skills/video-minutes/scripts/config_wizard.py --reset

# 或直接编辑配置文件
nano ~/.opencode/skills/video-minutes/config.yaml
```

## 配置验证

保存配置后，验证有效性:

```python
def validate_config(config):
    """验证配置有效性"""
    errors = []

    # 检查必填字段
    required = ["version", "output", "whisper"]
    for field in required:
        if field not in config:
            errors.append(f"缺少必填字段: {field}")

    # 检查输出目录可写
    output_dir = os.path.expanduser(config.get("output", {}).get("directory", ""))
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            errors.append(f"无法创建输出目录: {e}")

    # 检查模型名称有效性
    valid_models = ["tiny", "base", "small", "medium", "large"]
    model = config.get("whisper", {}).get("model", "")
    if model not in valid_models:
        errors.append(f"无效模型名称: {model}")

    return len(errors) == 0, errors
```
