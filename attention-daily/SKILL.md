---
name: attention-daily
description: Daily tech intelligence report generator - automatically fetches GitHub trending repositories and AttentionVC.ai articles, analyzes content from multiple perspectives, and generates comprehensive daily digest reports. Use when users say "daily report", "tech digest", "GitHub trending", "attention vc articles", or want curated tech content with analysis.
---

# Attention Daily - Tech Intelligence Report

自动生成每日科技情报报告，整合 **GitHub Trending** 热门开源项目和 **AttentionVC.ai** 热门技术文章。

## What This Skill Does

1. **🔥 Fetches** GitHub trending repositories (Top 10)
   - From: https://github.attentionvc.ai/trending/repos
   - Includes: Project name, language, stars, description

2. **📰 Fetches** trending articles from AttentionVC.ai
   - Categories: Tech, AI
   - Time range: 24 hours
   - Quantity: 10 articles per category

3. **🔍 Analyzes** articles from multiple perspectives
   - 💻 Technical perspective
   - 💼 Business perspective
   - 👥 User perspective
   - 📈 Trend perspective

4. **📝 Generates** comprehensive daily report
   - GitHub projects summary
   - Article analysis with insights
   - Cross-reference summary
   - Key trends and insights

## Usage

Simply say: "生成今日日报" 或 "run attention daily"

The skill will:
1. Fetch top 10 GitHub trending repos
2. Fetch top 10 Tech articles from AttentionVC.ai
3. Fetch top 10 AI articles from AttentionVC.ai
4. Analyze all articles with multi-perspective insights
5. Generate comprehensive report with all findings

## Report Structure

### 📊 Part 1: GitHub 热门项目

```markdown
## 🔥 Part 1: GitHub 热门项目 (Top 10)

| 排名 | 项目 | 语言 | ⭐ Stars | 简介 |
|------|------|------|----------|------|
| 1 | **owner/repo** | Rust | 1.2K | Project description... |
| ... | ... | ... | ... | ... |

### 💡 项目亮点总结
- **热门语言**: Rust(3), Python(2), Go(2)
- **项目类型**: 涵盖 AI 工具、开发框架、实用工具
- **趋势观察**: 开源社区活跃，AI 相关项目持续热门
```

### 📰 Part 2: 热门文章分析

```markdown
## 📰 Part 2: 热门文章分析

### 💻 Tech 领域 (Top 10)

#### 1. 《文章标题》
- **作者**: Author Name @handle · Location
- **数据**: 538.5K 浏览 · 1.0K♥ · 45💬
- **热度**: 🔥🔥 热门
- **关键词**: API, Tool, Tutorial
- **简介**: 文章简短描述

**多视角解读**:
- 💻 **技术视角**: 技术创新、实现方案分析
- 💼 **商业视角**: 商业机会和市场价值
- 👥 **用户视角**: 用户体验和使用场景
- 📈 **趋势视角**: 行业趋势和发展方向

---

### 🤖 AI 领域 (Top 10)
[Similar structure...]

### 📊 总体分析
- 总文章数: 20 篇
- 热门关键词: Claude(5), AI(4), API(3)
- 趋势观察: [Key observations]
```

### 🎯 Part 3: 今日总结

```markdown
## 🎯 今日总结

### 🔗 两部分内容关联
**GitHub 项目观察**:
- 今日热门项目共 10 个，其中 4 个与 AI 相关
- 开源社区活跃，新工具和框架持续涌现

**社区讨论热点**:
- Tech 领域: 10 篇热门文章
- AI 领域: 10 篇热门文章
- 技术社区关注实用工具、最佳实践和行业动态

### 💡 关键洞察
1. **开源与社区并进**: GitHub 项目和社区讨论相互呼应
2. **AI 持续主导**: 无论是开源项目还是社区文章，AI 都是绝对主角
3. **实用性优先**: 教程、工具和实用方案最受欢迎
4. **技术生态活跃**: 新技术、新工具、新方法层出不穷
```

## Data Sources

### 1. GitHub Trending
- **URL**: https://github.attentionvc.ai/trending/repos
- **Content**: Daily trending repositories
- **Metrics**: Stars, language, description

### 2. AttentionVC.ai
- **Tech Articles**: https://www.attentionvc.ai/article?window=1d&category=tech&lang=en%2Czh
- **AI Articles**: https://www.attentionvc.ai/article?window=1d&category=ai&lang=en%2Czh
- **Metrics**: Impressions, likes, replies, reposts
- **Time Range**: 24 hours (1d)

## Technical Implementation

### Required MCP Tools
- `playwright` - For browser automation

### Scripts Structure

```
scripts/
├── package.json              # Dependencies
├── config.js                 # Configuration
├── main.js                   # Entry point (Enhanced)
├── github-trending.js        # GitHub data fetcher
├── attentionvc-fetcher.js    # AttentionVC data fetcher
├── article-analyzer.js       # Article analysis module
├── report-generator.js       # Report generation (Enhanced)
└── output/                   # Generated reports
```

### Execution Flow

1. **Initialize** browser
2. **Fetch GitHub** trending repos
   - Navigate to trending page
   - Extract top 10 repositories
   - Enrich with details
3. **Fetch AttentionVC** articles
   - Fetch Tech category (10 articles)
   - Fetch AI category (10 articles)
4. **Analyze** articles
   - Generate summary for each article
   - Multi-perspective insights
   - Extract keywords
   - Calculate heat level
5. **Generate** comprehensive report
6. **Save** report to file

### Running the Scripts

```bash
# Install dependencies
cd scripts && npm install

# Run full workflow
npm run daily
# or
node main.js
```

## Article Analysis Framework

### Analysis Perspectives

#### 1. 💻 Technical Perspective
Focus: Technology innovation, implementation, tech stack
- New technologies or methods introduced
- Technical architecture and design
- Code quality and best practices

#### 2. 💼 Business Perspective
Focus: Business model, market opportunity, investment value
- Commercial potential
- Market positioning
- Revenue models

#### 3. 👥 User Perspective
Focus: User experience, use cases, pain points
- Problem-solving capability
- User adoption barriers
- Practical value

#### 4. 📈 Trend Perspective
Focus: Industry trends, future direction, evolution
- Technology evolution path
- Industry impact
- Future predictions

### Heat Level Calculation

```
Heat Score = Impressions × 0.5 + Likes × 100 + Replies × 200 + Reposts × 150

Levels:
- 🔥🔥🔥 爆款: >= 10,000,000
- 🔥🔥 热门: >= 1,000,000
- 🔥 较热: >= 100,000
- 📌 普通: < 100,000
```

## Example Output

### Full Report Preview

```markdown
# 📊 Attention Daily Digest - 2026年3月25日

> 🤖 自动生成的每日科技情报报告
> 📌 数据来源: GitHub Trending + AttentionVC.ai
> ⏰ 生成时间: 2026/3/25 10:30:00

## 📈 今日概览

| 指标 | 数值 |
|------|------|
| **GitHub 热门项目** | 10 个 |
| **热门文章** | 20 篇 |
| **覆盖领域** | AI, Tech, Crypto |
| **数据来源** | GitHub + AttentionVC.ai |

## 🔥 Part 1: GitHub 热门项目 (Top 10)

| 排名 | 项目 | 语言 | ⭐ Stars | 简介 |
|------|------|------|----------|------|
| 1 | **openai/openai-go** | Go | 2.1K | OpenAI Go SDK |
| 2 | **anthropics/claude-code** | TypeScript | 1.8K | Claude Code editor |
| ... | ... | ... | ... | ... |

### 💡 项目亮点总结
- **热门语言**: Go(3), TypeScript(2), Rust(2)
- **项目类型**: 涵盖 AI SDK、开发工具、基础设施
- **趋势观察**: AI 相关项目持续热门，开发工具受关注

## 📰 Part 2: 热门文章分析

### 💻 Tech 领域 (Top 10)

#### 1. 《An Update from the Anti-Cheat Team》
- **作者**: John Doe @johndoe · USA
- **数据**: 538.5K 浏览 · 1.0K♥ · 45💬
- **热度**: 🔥🔥 热门
- **关键词**: Gaming, Security
- **简介**: 游戏反作弊团队的最新进展和技术更新

**多视角解读**:
- 💻 **技术视角**: 介绍了新的反作弊技术和检测方法
- 💼 **商业视角**: 游戏行业安全问题日益重要，技术投入增加
- 👥 **用户视角**: 玩家对公平游戏环境的期待
- 📈 **趋势视角**: 游戏安全将成为长期技术竞争点

---

### 🤖 AI 领域 (Top 10)

#### 1. 《The Ultimate Beginner's Guide to Claude》
- **作者**: Jane Smith @janesmith · UK
- **数据**: 3.9M 浏览 · 12.5K♥ · 892💬
- **热度**: 🔥🔥🔥 爆款
- **关键词**: Claude, Tutorial, AI
- **简介**: Claude AI 的完整入门教程，从安装到高级用法

**多视角解读**:
- 💻 **技术视角**: 详细介绍了 Claude 的技术特性和使用方法
- 💼 **商业视角**: Claude 生态快速发展，用户教育需求大
- 👥 **用户视角**: 降低 AI 工具使用门槛，实用价值高
- 📈 **趋势视角**: AI 助手正从早期采用者向大众普及

---

### 📊 总体分析

**数据概览**:
- 总文章数: 20 篇
- 热门关键词: Claude(6), AI(8), Tutorial(4)

**趋势观察**:
- Claude 相关话题持续火热，开发者和用户都在积极探索
- AI 工具和框架层出不穷，技术生态快速演进
- 技术内容以实用工具、教程和最新动态为主

## 🎯 今日总结

### 🔗 两部分内容关联

**GitHub 项目观察**:
- 今日热门项目共 10 个，其中 4 个与 AI 相关
- 开源社区活跃，新工具和框架持续涌现

**社区讨论热点**:
- Tech 领域: 10 篇热门文章
- AI 领域: 10 篇热门文章
- 技术社区关注实用工具、最佳实践和行业动态

### 💡 关键洞察

1. **开源与社区并进**: GitHub 项目和社区讨论相互呼应，技术热点从代码到讨论全面覆盖
2. **AI 持续主导**: 无论是开源项目还是社区文章，AI 都是绝对主角
3. **实用性优先**: 教程、工具和实用方案最受欢迎
4. **技术生态活跃**: 新技术、新工具、新方法层出不穷

---

**数据来源**:
- GitHub Trending: github.attentionvc.ai
- AttentionVC.ai: www.attentionvc.ai

**生成时间**: 2026/3/25 10:30:00 | **报告版本**: v2.0
```

## Customization

Edit `scripts/config.js` to customize:

```javascript
module.exports = {
  source: {
    // GitHub 配置
    github: {
      maxRepos: 10,  // 获取项目数量
    },
    // AttentionVC 配置
    attentionvc: {
      categories: ['tech', 'ai'],  // 文章分类
      window: '1d',  // 时间窗口
      maxArticlesPerCategory: 10,  // 每分类文章数
    }
  },
  
  // 分析配置
  analysis: {
    enabled: true,
    perspectives: ['tech', 'business', 'user', 'trend'],
  },
  
  // 输出配置
  output: {
    format: 'markdown',
    includeGitHub: true,
    includeArticles: true,
    includeAnalysis: true,
  }
};
```

## Error Handling

If data fetch fails:
1. Retry with timeout
2. Skip failed sources, continue with available data
3. Log errors for debugging
4. Generate partial report if some data available

## Dependencies

```json
{
  "dependencies": {
    "playwright": "^1.40.0"
  }
}
```

## Notes

- Report generation may take 30-60 seconds due to browser automation
- Data accuracy depends on source websites
- GitHub trending data refreshes daily
- AttentionVC.ai data refreshes every ~21 minutes
