#!/usr/bin/env python3
import sys
import re
from pathlib import Path
sys.path.insert(0, '.opencode/skills/video-minutes')
from video_analyzer import VideoAnalyzer

# 读取转录内容
with open('C:/Users/kangyao.ren/Downloads/P7rP4auIOeJ3IRua.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取字幕段落
segments = []
pattern = r'\*\*\[(\d{2}:\d{2}:\d{2})\]\*\* (.+)'
matches = re.findall(pattern, content)

for timestamp, text in matches:
    parts = timestamp.split(':')
    seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    segments.append({
        'text': text,
        'timestamp': seconds,
        'timestamp_str': timestamp
    })

print(f"[OK] Loaded {len(segments)} segments")

# 进行深度分析
analyzer = VideoAnalyzer()
full_text = ' '.join([s['text'] for s in segments])
analysis = analyzer.analyze_structure(segments, full_text)

# 生成深度分析报告
video_name = "P7rP4auIOeJ3IRua.mp4"
video_duration = "0:25:40"
processed_time = "2026-03-16 13:30:00"

content_type_names = {
    'tutorial': '教学教程',
    'lecture': '知识讲解',
    'review': '评测分析',
    'story': '案例故事',
    'news': '资讯报道'
}

content_type = content_type_names.get(analysis['content_type'], '内容分享')
theme = analysis['main_theme']

md_content = f"""# 视频深度纪要：{video_name}

## 基本信息

| 项目 | 内容 |
|------|------|
| **视频文件** | `{video_name}` |
| **视频时长** | {video_duration} |
| **处理时间** | {processed_time} |
| **字幕语言** | zh |
| **内容类型** | {content_type} |

---

## 内容概述

### 主题与关键词

**核心主题**: {theme['description']}

**关键词**: {', '.join(theme['keywords'][:5])}

**开场白**: 
> {theme['opening_hint'][:150]}...

### 视频主旨

本视频围绕**{theme['keywords'][0] if theme['keywords'] else '核心主题'}**展开深度讲解，主要阐述以下内容：

视频以批判传统风水工具（罗盘）为切入点，提出了基于卫星地图的现代风水测量方法，并通过真实案例验证了这套方法的有效性。

---

## 核心论点与论据

"""

# 添加核心论点
if analysis['core_arguments']:
    main_arg = analysis['core_arguments'][0]['argument']
    md_content += f"主要阐述「{main_arg[:100]}」等重要观点。\n\n"

for i, arg in enumerate(analysis['core_arguments'], 1):
    md_content += f"### 论点 {i}: {arg['argument'][:70]}{'...' if len(arg['argument']) > 70 else ''}\n\n"
    md_content += f"**时间**: {arg['timestamp']} | **论据强度**: {'★' * min(arg['strength'], 5)}\n\n"
    
    if arg['evidence']:
        md_content += "**支持论据**:\n"
        for ev in arg['evidence']:
            md_content += f"- [{ev['timestamp']}] {ev['text'][:80]}{'...' if len(ev['text']) > 80 else ''}\n"
    md_content += "\n"

md_content += """---

## 内容结构分析

### 章节划分

| 章节 | 时间范围 | 核心内容 |
|------|----------|----------|
"""

for chapter in analysis['chapters']:
    title = chapter['title'] if chapter['title'] else f"段落 {chapter['index']}"
    time_range = chapter['time_range']
    summary = chapter['summary'][:60] + '...' if len(chapter['summary']) > 60 else chapter['summary']
    md_content += f"| {title} | {time_range} | {summary} |\n"

md_content += "\n### 各章节要点\n\n"

for chapter in analysis['chapters']:
    title = chapter['title'] if chapter['title'] else f"段落 {chapter['index']}"
    md_content += f"#### {chapter['index']}. {title}\n\n"
    
    if chapter['key_points']:
        for point in chapter['key_points']:
            md_content += f"- **[{point['timestamp']}]** {point['text']}\n"
    else:
        md_content += f"*{chapter['summary'][:120]}...*\n"
    md_content += "\n"

md_content += """---

## 实用价值提炼

### 核心方法论

**1. 风水测量的正确方法**
- 不要使用传统罗盘（磁偏角问题）
- 改用卫星地图测量（正北方向准确）
- 以楼门朝向为基准，而非阳台方向

**2. 房屋风水快速评估**
- 通过卫星地图确定精确朝向
- 观察周边环境和地形
- 结合罗盘软件验证（仅作参考）

**3. 选房实用技巧**
- 优先选择"纳气"好的户型
- 避免极端朝向（如正北）
- 注意楼层与朝向的配合

### 关键建议

"""

# 添加实用要点
if analysis['practical_value']:
    for i, item in enumerate(analysis['practical_value'][:8], 1):
        md_content += f"**{i}.** [{item['timestamp']}] {item['content'][:100]}{'...' if len(item['content']) > 100 else ''}\n\n"

md_content += """---

## 关键洞察总结

### 最重要的5个要点

"""

# 收集所有关键要点
all_key_points = []
for chapter in analysis['chapters']:
    all_key_points.extend(chapter['key_points'])

if all_key_points:
    all_key_points.sort(key=lambda x: x.get('score', 0), reverse=True)
    for i, point in enumerate(all_key_points[:5], 1):
        md_content += f"**{i}.** {point['text']}\n"
        md_content += f"   > 时间: [{point['timestamp']}]\n\n"

md_content += """### 核心结论

1. **罗盘不准是系统性问题** - 磁偏角随时间和地理位置变化，现代环境（钢筋、电器）进一步干扰
2. **卫星地图是可靠工具** - 基于正北方向，不受磁偏影响，符合古代风水师使用土圭日晷的原理
3. **实践验证有效性** - 通过真实案例（农村小伙变老板）验证了方法的实用性
4. **普通人也能掌握** - 不需要专业知识，用对工具即可达到95%风水师的水平
5. **科学与传统结合** - 用现代科技解决传统工具的缺陷，传承真正的风水智慧

---

## 内容评价

### 内容质量

- **逻辑性**: 视频包含"问题提出→分析原因→解决方案→案例验证"的完整逻辑链，结构清晰
- **层次感**: 内容分为"批判传统→介绍方法→实战案例→总结"四个层次，层层递进
- **实用性**: 提供了可直接操作的方法（卫星地图测量），实操性强
- **信息密度**: 25分钟内涵盖了理论、方法、案例，信息密度高
- **说服力**: 使用历史案例（朱棣皇陵）和现代案例双重论证，说服力强

### 创新点

1. **颠覆性观点** - 挑战千年传统（罗盘），提出新方法论
2. **科学解释** - 用磁偏角、地磁变化等科学原理解释为什么罗盘不准
3. **古今结合** - 指出古代风水师其实用土圭而非罗盘，还原历史真相
4. **民主化风水** - 让普通人也能掌握风水，打破专业垄断

### 适用人群

- 对风水感兴趣但无从下手的初学者
- 被风水师误导过、希望获得正确知识的受害者
- 准备买房租房、需要实用风水指导的实践者
- 对传统文化有批判精神的理性思考者

### 局限性

- 部分观点较激进（"95%风水师都是错的"），可能引发争议
- 案例样本较少（仅3个），统计显著性有限
- 缺乏对其他风水流派（如玄空、八宅）的具体回应

---

## 行动建议

基于本视频内容，建议采取以下行动：

1. **立即行动**
   - 下载卫星地图APP（如奥维互动地图）
   - 测量自己当前住所的精确朝向
   - 记录户型和楼层信息

2. **学习深化**
   - 了解"纳气"理论的基本概念
   - 学习不同朝向的风水特点
   - 研究周边地形对风水的影响

3. **实践应用**
   - 将方法应用于买房/租房决策
   - 帮助亲友评估房屋风水
   - 建立案例库验证方法有效性

---

## 备注

- 本纪要由 AI 深度分析生成，基于语音识别和智能内容理解
- 章节划分和要点提取基于算法分析，可能存在误差
- 建议结合原视频观看以获得最佳理解
- 风水属于传统文化范畴，内容仅供学习参考
- 如需引用内容，请核对原视频确认准确性

---

*Generated by Video Minutes Skill v2.0 - Deep Analysis Mode*
*Analysis includes: content structure, core arguments, practical value, and critical insights*
"""

# 保存文件
output_path = Path('C:/Users/kangyao.ren/Downloads/P7rP4auIOeJ3IRua_deep_analysis.md')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"[OK] Deep analysis report saved: {output_path}")
print(f"[INFO] Report includes:")
print(f"   - Content overview and theme analysis")
print(f"   - {len(analysis['core_arguments'])} core arguments with evidence")
print(f"   - {len(analysis['chapters'])} chapter structure breakdown")
print(f"   - Practical methodology extraction")
print(f"   - Critical insights and evaluation")
