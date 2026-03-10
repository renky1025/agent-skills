---
name: twitter-one-liner
description: Generate high-quality Twitter/X posts from a single sentence input. Use when users want to create engaging tweets, need tweet ideas, or say things like "一句话创建twitter帖子", "帮我写个推文", "create a tweet about X". Creates 3 different styles - Direct, Story-based, and Value-driven - with hashtags and engagement tips.
---

# Twitter One-Liner Post Generator

Transform a simple idea or topic into 3 engaging Twitter/X post options.

## Usage

When the user provides a topic/idea (one sentence), generate 3 tweet variations:

### 输出格式

```
🎯 **直击型** (Direct & Punchy)
[Tweet content]
#标签建议: #xxx #xxx #xxx
字符数: xxx | 预估engagement: 高/中/低
💡 **为什么有效**: [简短说明]

---

📖 **故事型** (Story-driven)
[Tweet content]
#标签建议: #xxx #xxx #xxx
字符数: xxx | 预估engagement: 高/中/低
💡 **为什么有效**: [简短说明]

---

💡 **价值型** (Value-driven)
[Tweet content]
#标签建议: #xxx #xxx #xxx
字符数: xxx | 预估engagement: 高/中/低
💡 **为什么有效**: [简短说明]
```

### 创作原则 (Twitter增长最佳实践)

1. **Hook要抓人** - 前3个词决定用户是否继续阅读
2. **善用换行** - 每1-2句话换行，增加可读性
3. **具体化** - 使用数字、例子、细节
4. **真实感** - 加入个人化表达，避免过度 polished
5. **互动引导** - 以问题或邀请评论结尾
6. **避免硬推销** - 提供价值，而非直接卖东西

### 三种风格定义

**🎯 直击型**
- 简短有力，直接表达核心观点
- 适合：金句、洞察、观点表达
- 长度：50-150字符
- 特点：一句话或两句话，冲击力强

**📖 故事型**
- 加入个人经历、情感或叙事
- 适合：分享教训、成长经历、背后故事
- 长度：150-250字符
- 特点：有起承转合，引发共鸣

**💡 价值型**
- 提供实用建议、技巧或insights
- 适合：教学、经验分享、 actionable tips
- 长度：150-280字符
- 特点：读者能带走具体价值

### Hashtag策略

- 2-3个相关标签
- 混合使用：1个热门大标签 + 1-2个精准小标签
- 避免过度使用标签（最多3个）
- 标签放在推文末尾或第一条回复

### 示例

**输入**: "关于早起的好处"

**输出**:

```
🎯 **直击型**
早起不是为了折磨自己。
是为了在世界的噪音开始前，
先听见自己的声音。

#早起 #自律人生 #清晨时光
字符数: 142 | 预估engagement: 高
💡 **为什么有效**: 打破"早起=自律"的刻板印象，提供情感共鸣

---

📖 **故事型**
一年前我开始6点起床。
起初很痛苦，现在离不开。

最神奇的变化不是效率，
而是我终于有了"属于自己的时间"。

在家人醒来前，我已经读完一章书。
这种感觉，会上瘾。

#早起改变 #个人成长 #晨间习惯
字符数: 218 | 预估engagement: 高
💡 **为什么有效**: 具体故事+情感转折+读者能想象画面

---

💡 **价值型**
早起的人都在做什么？

我观察了100个早起成功者，
发现他们的晨间都有这3件事：

1️⃣ 不碰手机（保护专注力）
2️⃣ 做一件让自己骄傲的小事
3️⃣ 花5分钟规划今天最重要的1件事

试试明天开始？

#早起方法 # productivity #晨间routine
字符数: 267 | 预估engagement: 高
💡 **为什么有效**: 提供具体可执行的步骤，读者有获得感
```

## 执行步骤

1. 分析用户输入的主题/想法
2. 提炼核心信息和潜在角度
3. 分别用3种风格创作推文
4. 为每个推文添加合适的hashtags
5. 计算字符数并评估engagement潜力
6. 解释每个推文为什么有效

## 注意事项

- 保持语气自然，不要太商业化
- 鼓励用户根据自己的风格调整
- 如果主题敏感或争议性，提供中性表达选项
- 提醒用户Twitter/X字符限制为280字符（中文约140字）
