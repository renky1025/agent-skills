/**
 * Attention Daily - Enhanced Report Generator
 * 
 * 增强版日报生成模块：整合 GitHub Trending 和 AttentionVC 文章分析
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
   * 生成完整日报（包含 GitHub Trending 和文章分析）
   * @param {Object} data - 抓取的数据
   * @returns {string} Markdown 格式日报
   */
  generateReport(data) {
    const sections = [
      this.generateHeader(),
      this.generateOverview(data),
      
      // Part 1: GitHub Trending
      this.generateGitHubSection(data.githubRepos),
      
      // Part 2: AttentionVC Articles with Analysis
      this.generateArticlesSection(data.attentionvcArticles),
      
      // Summary
      this.generateSummary(data),
      
      this.generateFooter(data),
    ];

    return sections.join('\n\n');
  }

  generateHeader() {
    return `# 📊 Attention Daily Digest - ${this.date}

> 🤖 自动生成的每日科技情报报告  
> 📌 数据来源: GitHub Trending + AttentionVC.ai  
> ⏰ 生成时间: ${new Date().toLocaleString('zh-CN')}`;
  }

  generateOverview(data) {
    const githubCount = data.githubRepos?.length || 0;
    const articleCount = data.attentionvcArticles?.totalCount || 0;
    
    return `## 📈 今日概览

| 指标 | 数值 |
|------|------|
| **GitHub 热门项目** | ${githubCount} 个 |
| **热门文章** | ${articleCount} 篇 |
| **覆盖领域** | AI, Tech, Crypto |
| **数据来源** | GitHub + AttentionVC.ai |`;
  }

  /**
   * 生成 GitHub Trending 部分
   */
  generateGitHubSection(repos) {
    if (!repos || repos.length === 0) {
      return `## 🔥 Part 1: GitHub 热门项目

> 暂无数据`;
    }

    let section = `## 🔥 Part 1: GitHub 热门项目 (Top ${repos.length})

来自 [github.attentionvc.ai/trending/repos](https://github.attentionvc.ai/trending/repos) 的今日热门开源项目：

| 排名 | 项目 | 语言 | ⭐ Stars | 简介 |
|------|------|------|----------|------|`;

    for (const repo of repos) {
      const name = repo.name?.length > 35 
        ? repo.name.substring(0, 35) + '...' 
        : repo.name;
      const desc = repo.simpleDescription || repo.description || '暂无描述';
      const shortDesc = desc.length > 50 ? desc.substring(0, 50) + '...' : desc;
      
      section += `\n| ${repo.rank} | **${name}** | ${repo.language || 'N/A'} | ${repo.stars || '-'} | ${shortDesc} |`;
    }

    section += `\n\n### 💡 项目亮点总结\n\n`;
    
    // 生成项目总结
    const languages = {};
    repos.forEach(repo => {
      const lang = repo.language || 'Unknown';
      languages[lang] = (languages[lang] || 0) + 1;
    });
    
    const topLangs = Object.entries(languages)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3)
      .map(([lang, count]) => `${lang}(${count})`)
      .join(', ');
    
    section += `- **热门语言**: ${topLangs}\n`;
    section += `- **项目类型**: 涵盖 AI 工具、开发框架、实用工具等多个领域\n`;
    section += `- **趋势观察**: 开源社区活跃，AI 相关项目持续热门\n`;

    return section;
  }

  /**
   * 生成文章部分（带分析）
   */
  generateArticlesSection(articleData) {
    if (!articleData || !articleData.categories) {
      return `## 📰 Part 2: 热门文章分析

> 暂无数据`;
    }

    let section = `## 📰 Part 2: 热门文章分析

来自 AttentionVC.ai 的热门技术文章（24小时内）：\n`;

    const categories = articleData.categories;
    
    // Tech 分类
    if (categories.tech && categories.tech.articles) {
      section += this.generateCategoryWithAnalysis('Tech', categories.tech.articles);
    }
    
    // AI 分类
    if (categories.ai && categories.ai.articles) {
      section += this.generateCategoryWithAnalysis('AI', categories.ai.articles);
    }

    // 总体分析
    section += this.generateOverallAnalysis(articleData);

    return section;
  }

  /**
   * 生成带分析的单个分类
   */
  generateCategoryWithAnalysis(categoryName, articles) {
    if (!articles || articles.length === 0) return '';

    const emoji = categoryName === 'AI' ? '🤖' : '💻';
    
    let section = `\n### ${emoji} ${categoryName} 领域 (Top ${articles.length})\n\n`;

    for (const article of articles) {
      section += `#### ${article.rank}. 《${article.title}》\n\n`;
      section += `- **作者**: ${article.author} ${article.authorHandle} ${article.location ? `· ${article.location}` : ''}\n`;
      section += `- **数据**: ${article.impressions} 浏览 · ${article.likes || 0}♥ · ${article.replies || 0}💬\n`;
      section += `- **热度**: ${article.heatLevel || '📌 普通'}\n`;
      
      if (article.keywords && article.keywords.length > 0) {
        section += `- **关键词**: ${article.keywords.join(', ')}\n`;
      }
      
      section += `- **简介**: ${article.summary || '暂无描述'}\n\n`;
      
      // 多视角点评
      if (article.insights) {
        section += `**多视角解读**:\n`;
        Object.entries(article.insights).forEach(([key, insight]) => {
          section += `- ${insight.emoji} **${insight.name}**: ${insight.insight}\n`;
        });
        section += `\n`;
      }
      
      section += `---\n\n`;
    }

    return section;
  }

  /**
   * 生成总体分析
   */
  generateOverallAnalysis(articleData) {
    let section = `\n### 📊 总体分析\n\n`;
    
    // 统计信息
    let totalArticles = 0;
    const allArticles = [];
    
    Object.values(articleData.categories || {}).forEach(cat => {
      if (cat.articles) {
        totalArticles += cat.articles.length;
        allArticles.push(...cat.articles);
      }
    });
    
    // 热门关键词
    const allKeywords = [];
    allArticles.forEach(article => {
      if (article.keywords) allKeywords.push(...article.keywords);
    });
    
    const keywordCount = {};
    allKeywords.forEach(kw => {
      keywordCount[kw] = (keywordCount[kw] || 0) + 1;
    });
    
    const topKeywords = Object.entries(keywordCount)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([kw, count]) => `${kw}(${count})`);
    
    section += `**数据概览**:\n`;
    section += `- 总文章数: ${totalArticles} 篇\n`;
    section += `- 热门关键词: ${topKeywords.join(', ') || '暂无'}\n\n`;
    
    // 趋势观察
    section += `**趋势观察**:\n`;
    
    const hasClaude = allKeywords.some(kw => kw.toLowerCase().includes('claude'));
    const hasAI = allKeywords.some(kw => kw.toLowerCase().includes('ai'));
    const hasCrypto = allKeywords.some(kw => 
      ['crypto', 'bitcoin', 'web3', 'blockchain'].includes(kw.toLowerCase())
    );
    
    if (hasClaude) {
      section += `- Claude 相关话题持续火热，开发者和用户都在积极探索应用场景\n`;
    }
    if (hasAI) {
      section += `- AI 工具和框架层出不穷，技术生态快速演进\n`;
    }
    if (hasCrypto) {
      section += `- Crypto 领域关注技术实现和合规进展\n`;
    }
    
    section += `- 技术内容以实用工具、教程和最新动态为主\n`;

    return section;
  }

  /**
   * 生成总结部分
   */
  generateSummary(data) {
    let section = `\n## 🎯 今日总结\n\n`;
    
    section += `### 🔗 两部分内容关联\n\n`;
    
    // GitHub 项目总结
    if (data.githubRepos && data.githubRepos.length > 0) {
      const aiRepos = data.githubRepos.filter(r => 
        r.description?.toLowerCase().includes('ai') ||
        r.description?.toLowerCase().includes('llm') ||
        r.description?.toLowerCase().includes('ml')
      );
      
      section += `**GitHub 项目观察**:\n`;
      section += `- 今日热门项目共 ${data.githubRepos.length} 个`;
      if (aiRepos.length > 0) {
        section += `，其中 ${aiRepos.length} 个与 AI 相关`;
      }
      section += `\n`;
      section += `- 开源社区活跃，新工具和框架持续涌现\n\n`;
    }
    
    // 文章总结
    if (data.attentionvcArticles && data.attentionvcArticles.categories) {
      const techCount = data.attentionvcArticles.categories.tech?.articles?.length || 0;
      const aiCount = data.attentionvcArticles.categories.ai?.articles?.length || 0;
      
      section += `**社区讨论热点**:\n`;
      section += `- Tech 领域: ${techCount} 篇热门文章\n`;
      section += `- AI 领域: ${aiCount} 篇热门文章\n`;
      section += `- 技术社区关注实用工具、最佳实践和行业动态\n\n`;
    }
    
    section += `### 💡 关键洞察\n\n`;
    section += `1. **开源与社区并进**: GitHub 项目和社区讨论相互呼应，技术热点从代码到讨论全面覆盖\n`;
    section += `2. **AI 持续主导**: 无论是开源项目还是社区文章，AI 都是绝对主角\n`;
    section += `3. **实用性优先**: 教程、工具和实用方案最受欢迎\n`;
    section += `4. **技术生态活跃**: 新技术、新工具、新方法层出不穷\n\n`;

    return section;
  }

  generateFooter(data) {
    return `---

**数据来源**: 
- GitHub Trending: [github.attentionvc.ai](https://github.attentionvc.ai/trending/repos)
- AttentionVC.ai: [www.attentionvc.ai](https://www.attentionvc.ai)

**生成时间**: ${new Date().toLocaleString('zh-CN')} | **报告版本**: v2.0`;
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
