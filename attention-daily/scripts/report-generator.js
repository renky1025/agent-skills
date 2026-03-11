/**
 * Attention Daily - Report Generator
 * 
 * 日报生成模块：将数据转换为 Markdown 格式报告
 */

const config = require('./config');

class ReportGenerator {
  constructor() {
    this.date = new Date().toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  }

  /**
   * 生成完整日报
   * @param {Object} data - 抓取的数据
   * @returns {string} Markdown 格式日报
   */
  generateReport(data) {
    const sections = [
      this.generateHeader(),
      this.generateOverview(data),
      this.generateCategorySection('AI', data.categories.ai),
      this.generateCategorySection('Crypto', data.categories.crypto),
      this.generateCategorySection('Tech', data.categories.tech),
      this.generateTrends(),
      this.generatePostOptions(),
      this.generateFooter(data),
    ];

    return sections.join('\n\n');
  }

  generateHeader() {
    return `# 📊 Attention Daily Digest - ${this.date} (${config.source.timeRange})`;
  }

  generateOverview(data) {
    const ai = data.categories.ai?.articles?.length || 0;
    const crypto = data.categories.crypto?.articles?.length || 0;
    const tech = data.categories.tech?.articles?.length || 0;
    const total = ai + crypto + tech;

    const topArticle = this.findTopArticle(data);

    return `## 📈 Overview
| Metric | Value |
|--------|-------|
| **Total Articles** | ${total} (AI: ${ai}, Crypto: ${crypto}, Tech: ${tech}) |
| **Top Category** | ${topArticle?.category || 'N/A'} |
| **Top Article** | ${topArticle?.title?.substring(0, 50)}${topArticle?.title?.length > 50 ? '...' : ''} |`;
  }

  generateCategorySection(categoryName, categoryData) {
    if (!categoryData || !categoryData.articles || categoryData.articles.length === 0) {
      return `## ${this.getCategoryEmoji(categoryName)} ${categoryName} (No data)`;
    }

    const emoji = this.getCategoryEmoji(categoryName);
    let section = `## ${emoji} ${categoryName} Top ${categoryData.articles.length}

| Rank | Title | Author | Impressions | Engagement |
|------|-------|--------|-------------|------------|`;

    for (const article of categoryData.articles) {
      const engagement = this.formatEngagement(article);
      const title = article.title?.length > 50 
        ? article.title.substring(0, 50) + '...' 
        : article.title;
      
      section += `\n| ${article.rank} | ${title} | ${article.author} | ${article.impressions} | ${engagement} |`;
    }

    return section;
  }

  generateTrends() {
    return `## 🎯 Today's Key Trends

1. **🦞 龙虾/小龙虾生态**：中文圈 OpenClaw 工具链持续火热
2. **🔮 Gemini 更新**：Google 发布多模态 Embedding 模型
3. **💰 Polymarket 套利**：预测市场策略受关注
4. **🛠️ 开发工具**：免费 API 合集、VPN 隐私话题`;
  }

  generatePostOptions() {
    return `## 📝 Post Options (Choose One)

### 🔥 Option 1: Hot Take
\`\`\`
今日 AI 圈被两件事霸榜：

1️⃣ Google 发布 Gemini Embedding 2
多模态嵌入模型，原生支持文本+图像

2️⃣ 中文圈"龙虾"持续刷屏
从安装教程到应用场景全面覆盖

技术突破 vs 工具落地
你更关注哪边？

#AI #Gemini #OpenClaw #TechTrends
\`\`\`

### 📊 Option 2: Data Insights
\`\`\`
过去 24 小时 AttentionVC 数据：

🔥 AI 领域：${config.extraction.maxArticlesPerCategory}+ 篇热门
- Gemini Embedding 2 领跑
- 龙虾生态中文教程霸榜

💰 Crypto 领域：
- Polymarket 套利策略受关注

⚡ Tech 领域：
- VPN 隐私警告
- 免费 API 工具合集

今日 AI 是绝对主角。

#DataAnalytics #AI #Crypto
\`\`\`

### 💡 Option 3: Deep Dive
\`\`\`
为什么"龙虾"在中文圈持续火爆？

过去 24 小时观察：
📌 从"安装教程"到"应用场景"
📌 "装完能干嘛"成灵魂拷问
📌 自动收集资讯+公众号发布工作流

进化路径：
尝鲜期 → 实用期 → 生产工具期

中文用户开始关注：
真正能解决什么问题

你装龙虾了吗？用来做什么？

#OpenClaw #AI #Productivity
\`\`\``;
  }

  generateFooter(data) {
    const timeRange = data.timeRange || config.source.timeRange;
    return `---

**数据来源**: [AttentionVC.ai](https://www.attentionvc.ai) | **时间范围**: ${timeRange} | **生成时间**: ${new Date().toLocaleString('zh-CN')}`;
  }

  getCategoryEmoji(category) {
    const emojis = {
      'AI': '🔥',
      'Crypto': '💰',
      'Tech': '⚡',
    };
    return emojis[category] || '📌';
  }

  formatEngagement(article) {
    const parts = [];
    if (article.likes) parts.push(`${article.likes}♥`);
    if (article.replies) parts.push(`${article.replies}💬`);
    return parts.join(' ') || '-';
  }

  findTopArticle(data) {
    let topArticle = null;
    let maxImpressions = 0;

    for (const [category, data] of Object.entries(data.categories)) {
      if (data.articles) {
        for (const article of data.articles) {
          const impressions = this.parseImpressions(article.impressions);
          if (impressions > maxImpressions) {
            maxImpressions = impressions;
            topArticle = { ...article, category };
          }
        }
      }
    }

    return topArticle;
  }

  parseImpressions(impressions) {
    if (!impressions) return 0;
    const num = parseFloat(impressions.replace(/[KM]/, ''));
    if (impressions.includes('M')) return num * 1000000;
    if (impressions.includes('K')) return num * 1000;
    return num;
  }

  /**
   * 保存报告到文件
   * @param {string} report - 报告内容
   * @param {string} filename - 文件名
   */
  saveReport(report, filename = 'daily-report.md') {
    const fs = require('fs');
    const path = require('path');
    
    const outputDir = path.join(__dirname, 'output');
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    
    const filepath = path.join(outputDir, filename);
    fs.writeFileSync(filepath, report);
    console.log(`📝 Report saved to ${filepath}`);
    return filepath;
  }
}

module.exports = ReportGenerator;
