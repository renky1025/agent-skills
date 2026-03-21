# 配置 Schema 参考

## 完整配置项说明

### version
- **类型**: string
- **描述**: 配置文件版本号
- **示例**: "1.1.0"

### output
| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| language | string | "auto" | 输出语言: auto/zh/en/ja/ko/fr/de/es |
| format | string | "markdown" | 输出格式: markdown/obsidian/notion/lark |
| directory | string | "~/video-minutes" | 输出目录路径 |
| filename_template | string | "{date}-{type}-{title}" | 文件名模板 |

### content
| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| include_summary | boolean | true | 包含内容摘要 |
| include_key_points | boolean | true | 包含核心要点 |
| include_timeline | boolean | true | 包含详细时间线 |
| include_action_items | boolean | true | 包含行动项 |
| include_transcript | boolean | true | 包含完整字幕 |
| transcript_collapsed | boolean | true | 字幕默认折叠 |
| speaker_identification | boolean | true | 识别说话人 |
| max_summary_points | number | 10 | 摘要要点最大数量 |

### whisper
| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| model | string | "base" | 模型: tiny/base/small/medium/large |
| device | string | "auto" | 设备: auto/cpu/cuda/mps |
| language | string | null | 语言: null=自动检测 |

### classification
| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| enabled | boolean | true | 启用自动分类 |
| confidence_threshold | number | 0.7 | 分类置信度阈值 |

### dispatch
| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| confirm_before_dispatch | boolean | true | 分发前确认 |
| auto_dispatch_tags | array | ["@reminder"] | 自动分发的标签 |

### scanning
| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| enabled | boolean | true | 启用自动扫描 |
| interval_minutes | number | 60 | 扫描间隔(分钟) |
| paths | array | [] | 扫描路径列表 |

### integrations
| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| obsidian_vault | string | null | Obsidian vault 路径 |
| notion_database_id | string | null | Notion 数据库 ID |
| lark_webhook | string | null | 飞书 webhook URL |

## 配置示例

```yaml
version: "1.1.0"

output:
  language: auto
  format: obsidian
  directory: "~/Documents/video-minutes"
  filename_template: "{date}-{type}-{title}"

content:
  include_summary: true
  include_key_points: true
  include_timeline: true
  include_action_items: true
  include_transcript: true
  transcript_collapsed: true
  speaker_identification: true
  max_summary_points: 10

whisper:
  model: base
  device: auto
  language: null

classification:
  enabled: true
  confidence_threshold: 0.7

dispatch:
  confirm_before_dispatch: true
  auto_dispatch_tags:
    - "@reminder"

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
