---
name: attention-daily
description: Daily Twitter/X content curation from AttentionVC.ai - automatically fetches trending AI, Crypto, and Tech articles, generates daily digest reports, and creates multiple high-engagement post angles for users to choose from. Use when users say "daily digest", "attention vc", "trending articles", "ai crypto tech news", or want curated content for social media posting.
---

# Attention Daily - Viral Content Curator

Automatically curate trending AI, Crypto, and Tech content from AttentionVC.ai and generate high-engagement social media posts.

## What This Skill Does

1. **Fetches** trending articles from AttentionVC.ai (AI, Crypto, Tech categories)
2. **Analyzes** engagement metrics (impressions, likes, replies, reposts)
3. **Generates** a daily digest report with tables
4. **Creates** 5 different post angles for user selection

## Usage

Simply say: "生成今日日报" 或 "run attention daily"

The skill will:
1. Fetch top 20 articles from each category (AI, Crypto, Tech)
2. Generate a formatted daily report
3. Create 5 post options with different angles

## Output Format

### 📊 Daily Digest Report

```
# Attention Daily Digest - {Date}

## 📈 Overview
- Total Articles: {N}
- Top Category: {Category}
- Highest Engagement: {Article Title}

## 🔥 AI (Top 5)
| Rank | Title | Author | Impressions | Engagement |
|------|-------|--------|-------------|------------|
| 1 | ... | @author | 31.2M | 2.9K♥ 781💬 |
| ... | ... | ... | ... | ... |

## 💰 Crypto (Top 5)
| Rank | Title | Author | Impressions | Engagement |
|------|-------|--------|-------------|------------|
| 1 | ... | @author | 545.5K | 14.8K♥ |
| ... | ... | ... | ... | ... |

## ⚡ Tech (Top 5)
| Rank | Title | Author | Impressions | Engagement |
|------|-------|--------|-------------|------------|
| 1 | ... | @author | 538.5K | 1.0K♥ |
| ... | ... | ... | ... | ... |

## 🎯 Key Trends
- {Trend 1}
- {Trend 2}
- {Trend 3}
```

### 📝 Post Options (Choose One)

#### Option 1: 🔥 Hot Take (热点追踪型)
聚焦最热门话题，引发讨论

#### Option 2: 📊 Data Insights (数据洞察型)
基于数据发现趋势，理性分析

#### Option 3: 💡 Deep Dive (深度解读型)
深入分析某个重要话题

#### Option 4: 🌐 Global View (全球视野型)
对比不同地区/领域的关注点

#### Option 5: 🎯 Opportunity Spotting (机会发现型)
发现潜在机会或早期信号

## Data Source

**AttentionVC.ai** - Tracks viral X (Twitter) articles across categories
- Categories: AI (155 articles), Crypto (28), Tech (17), and more
- Metrics: Impressions, Likes, Replies, Reposts, Quotes
- Time range: 24h / 7d / 14d / All
- Languages: English & Chinese

## Post Writing Guidelines

### 1. Hot Take Angle 🔥
- Hook: 用数据或惊人事实开头
- Body: 简要总结 + 个人观点
- CTA: 引发讨论的问题
- Tone: 犀利、有态度
- Length: 150-250 characters

### 2. Data Insights 📊
- Hook: 展示关键数据
- Body: 分析趋势/变化
- CTA: 问读者看法
- Tone: 专业、理性
- Length: 200-280 characters

### 3. Deep Dive 💡
- Hook: 提出一个值得思考的问题
- Body: 深入分析一个话题
- CTA: 邀请分享经验
- Tone: 深度、有见解
- Length: 200-280 characters

### 4. Global View 🌐
- Hook: 对比不同视角
- Body: 展示地区/领域差异
- CTA: 问本地情况
- Tone: 开阔、包容
- Length: 180-250 characters

### 5. Opportunity 🎯
- Hook: 指出被忽视的机会
- Body: 解释为什么值得关注
- CTA: 问谁在关注
- Tone: 前瞻、洞察
- Length: 180-250 characters

## Hashtag Strategy

Per post:
- 1 trending category tag: #AI #Crypto #Tech
- 1 niche tag: #ClaudeCode #OpenClaw #Web3
- 1 broad tag: #Startup #Innovation #Future

## Technical Implementation

### Required MCP Tools
- `playwright` - For browser automation

### Scripts Location
All automation scripts are located in `scripts/` directory:

```
scripts/
├── package.json          # Dependencies
├── config.js             # Configuration
├── main.js               # Entry point
├── browser-automation.js # Browser automation
├── data-extractor.js     # Data extraction
└── report-generator.js   # Report generation
```

### Execution Steps

1. Navigate to https://www.attentionvc.ai/article
2. Check if page shows "Loading..." - if yes, wait for content to load; if no, proceed immediately
3. Click on time range button "24h" to select current day's content
4. Click on category button "AI" to filter AI articles
5. Wait for table to load (if loading)
6. Extract article data from rows
7. Repeat steps 4-6 for "Crypto" and "Tech" categories
8. Process and format data
9. Generate report
10. Create 5 post variations

### Running the Scripts

```bash
# Install dependencies
cd scripts && npm install

# Run full workflow
npm run daily
# or
node main.js
```

### Browser Automation Flow

```javascript
// Use the scripts directly from skill directory
const BrowserAutomation = require('./scripts/browser-automation');
const ReportGenerator = require('./scripts/report-generator');

async function generateDaily() {
  const browser = new BrowserAutomation();
  const generator = new ReportGenerator();
  
  await browser.init();
  const data = await browser.fetchAllData();
  const report = generator.generateReport(data);
  
  console.log(report);
  await browser.close();
}
```

### Data Schema

```typescript
interface Article {
  rank: number;
  title: string;
  author: string;
  authorHandle: string;
  location: string;
  impressions: string;
  category: string;
  likes: string;
  replies: string;
  reposts: string;
  quotes: string;
  date: string;
  wordCount: string;
  readTime: string;
}
```

## Example Output

### Daily Report

```
# Attention Daily Digest - March 10, 2026

## 📈 Overview
- Total Tracked: 50 articles
- Hottest Category: AI (31.2M impressions top article)
- Trending: Claude Code, AI Agents, Tokenization

## 🔥 AI Top 3
1. "Grok 4.20 vs Woke AI" - 31.2M impressions, 2.9K likes
2. "The First Multi-Behavior Brain Upload" - 9.9M impressions
3. "The Ultimate Beginner's Guide to Claude" - 3.9M impressions

## 💰 Crypto Top 3
1. "Why Most On-Chain Yield Fails Institutional Due Diligence" - 545.5K
2. "Zcash Open Development Lab Raises $25M+" - 425.5K
3. "Stop trying to guess. Start Planning the next Cycle" - 335.9K

## ⚡ Tech Top 3
1. "An Update from the Anti-Cheat Team" - 538.5K
2. "The Death of Issue Tracking" - 318.1K
3. "Clash Mi的小白配置教程" - 148.8K

## 🎯 Today's Trends
- AI agents are getting personal (chief of staff narrative)
- Claude Code ecosystem growing rapidly
- On-chain yield facing institutional scrutiny
- Tokenization breaking traditional finance barriers
```

### Post Options

**🔥 Hot Take:**
```
AI 正在从工具变成「员工」。

过去一周，关于 AI Agent 的帖子获得了 5000万+ 浏览。
最火的话题？"Claude 成了我的 chief of staff"。

这说明什么？
人们不再满足于 ChatGPT 的问答，
他们想要的是能主动做事的 Agent。

你觉得 AI 会先替代哪个岗位？

#AI #ClaudeCode #FutureOfWork
```

**📊 Data Insights:**
```
过去 7 天数据告诉我：

🔥 AI 内容占据绝对主导
- Top 1 帖子浏览量：3120万
- Top 3 平均浏览量：1500万+
- 关键词：Claude Code, AI Agent, Personal AI

💰 Crypto 更垂直
- Top 1 仅 54万浏览
- 但互动率更高（机构级话题）
- 关键词：On-chain yield, Tokenization

结论：AI 是流量密码，Crypto 是深度话题。

你更关注哪个领域？

#DataAnalytics #AI #Crypto
```

**💡 Deep Dive:**
```
为什么 Claude Code 突然火了？

看了过去 7 天的热门文章，发现一个趋势：
人们正在把 Claude 从「聊天工具」变成「工作伙伴」。

几个信号：
✅ "My chief of staff, Claude Code"
✅ "Claude Cowork Masterclass for SEO"
✅ "Save 74% on Anthropic API Bills"

背后逻辑：
当大家还在卷模型能力时，
先行者已经在卷「落地效率」。

这不是炒作，是真实的 workflow 变革。

你已经在用 AI 写代码/做内容了吗？

#ClaudeCode #AI #Productivity
```

**🌐 Global View:**
```
全球 Tech 圈在看什么？

🇺🇸 美国：Claude Code, AI Agents, Institutional Crypto
🇨🇳 中文圈：龙虾军团 (OpenClaw), AI工具教程
🇪🇺 欧洲：Technical deep dives, Go patterns
🇸🇬 新加坡：AI出海, 博主合集

有趣的差异：
- 英文圈关注 AI 替代工作流
- 中文圈关注 AI 工具实操
- Crypto 是全球共同话题

你平时主要看哪个圈子的内容？

#GlobalTech #AI #Startup
```

**🎯 Opportunity:**
```
发现一个被低估的趋势：

「AI 成本控制」正在成为新赛道。

过去一周看到：
📌 "Save 74% on Anthropic API Bills"
📌 "How to set up Claude Cowork"
📌 OpenClaw + ClawRouter (5k stars)

当 AI 成为基础设施，
「省钱」就变成了刚需。

这和云计算的发展路径一模一样：
先用起来 → 发现贵 → 找省钱方案 → 形成生态

谁能解决 AI 成本问题，谁就能抓住下一波机会。

你现在的 AI 工具账单每月多少？

#AI #CostOptimization #StartupOpportunity
```

## Customization

Users can customize:
- Number of articles to fetch (default: top 5 per category)
- Categories to track (default: AI, Crypto, Tech)
- Post style preferences
- Hashtag sets

## Error Handling

If data fetch fails:
1. Try alternative URL endpoints
2. Use cached data from previous run
3. Notify user with partial data

## Cross-Device Usage

To use this skill on a new device:

1. Copy the entire `attention-daily/` directory to the new device
2. Navigate to `scripts/` directory
3. Run `npm install` to install Playwright dependencies
4. The skill will auto-download Chromium on first run
5. Execute `node main.js` or `npm run daily`

### Required Dependencies
- Node.js >= 14
- Playwright >= 1.40.0 (auto-installed via npm)
- Chromium/Chrome (auto-downloaded by Playwright)

### Configuration
Edit `scripts/config.js` to customize:
- Time range (24h/7d/14d/All)
- Categories to track
- Browser settings
- Output format

## Notes

- Data refreshes every ~21 minutes on source
- Impressions numbers are from X (Twitter) analytics
- Engagement rate = (likes + replies + reposts) / impressions
- Consider timezone when interpreting "24h" data
