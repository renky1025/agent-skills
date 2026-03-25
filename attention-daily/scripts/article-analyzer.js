/**
 * Article Analyzer
 * 
 * 分析和点评文章，提供不同视角的解读
 */

class ArticleAnalyzer {
  constructor() {
    this.perspectives = {
      tech: {
        name: '技术视角',
        emoji: '💻',
        focus: '技术创新、实现方案、技术栈'
      },
      business: {
        name: '商业视角', 
        emoji: '💼',
        focus: '商业模式、市场机会、投资价值'
      },
      user: {
        name: '用户视角',
        emoji: '👥',
        focus: '用户体验、使用场景、痛点解决'
      },
      trend: {
        name: '趋势视角',
        emoji: '📈',
        focus: '行业趋势、未来方向、技术演进'
      }
    };
  }

  /**
   * 分析单篇文章
   * @param {Object} article - 文章数据
   * @returns {Object} 分析结果
   */
  analyzeArticle(article) {
    const title = article.title || '';
    const category = article.category || '';
    
    // 生成多视角点评
    const insights = this.generateInsights(article);
    
    // 生成简短总结
    const summary = this.generateSummary(article);
    
    // 判断文章热度
    const heatLevel = this.calculateHeatLevel(article);
    
    return {
      ...article,
      summary,
      insights,
      heatLevel,
      keywords: this.extractKeywords(title)
    };
  }

  /**
   * 批量分析文章
   * @param {Array} articles - 文章列表
   * @returns {Array} 分析后的文章列表
   */
  analyzeArticles(articles) {
    console.log(`🔍 Analyzing ${articles.length} articles...`);
    
    return articles.map(article => this.analyzeArticle(article));
  }

  /**
   * 生成文章总结
   * @param {Object} article - 文章数据
   * @returns {string} 总结文本
   */
  generateSummary(article) {
    const title = article.title || '';
    
    // 根据标题关键词生成智能总结
    const patterns = [
      {
        keywords: ['guide', 'tutorial', 'beginner', '入门', '教程'],
        summary: '这是一篇入门教程，帮助新手快速上手相关技术或工具。'
      },
      {
        keywords: ['update', 'release', 'new', '发布', '更新', '新版本'],
        summary: '介绍最新产品更新或版本发布，包含新功能和改进点。'
      },
      {
        keywords: ['analysis', 'research', 'study', '分析', '研究'],
        summary: '基于数据分析的深入研究报告，提供有价值的行业洞察。'
      },
      {
        keywords: ['comparison', 'vs', '对比', '比较'],
        summary: '多方案对比分析，帮助读者选择最适合的解决方案。'
      },
      {
        keywords: ['tool', 'app', 'platform', '工具', '应用'],
        summary: '介绍实用工具或应用，展示其功能和使用场景。'
      },
      {
        keywords: ['strategy', 'plan', 'method', '策略', '方法'],
        summary: '分享实用策略或方法论，可应用于实际工作或投资。'
      }
    ];
    
    const titleLower = title.toLowerCase();
    
    for (const pattern of patterns) {
      if (pattern.keywords.some(kw => titleLower.includes(kw.toLowerCase()))) {
        return pattern.summary;
      }
    }
    
    // 默认总结
    return '分享有价值的观点或信息，值得关注的行业动态。';
  }

  /**
   * 生成多视角点评
   * @param {Object} article - 文章数据
   * @returns {Object} 各视角点评
   */
  generateInsights(article) {
    const title = article.title || '';
    const category = article.category || '';
    const author = article.author || '';
    
    // 技术视角
    let techInsight = '';
    if (category === 'AI') {
      techInsight = 'AI技术持续演进，关注实际落地场景和技术突破。';
    } else if (category === 'TECH') {
      techInsight = '技术工具和方法论的创新，提升开发效率和用户体验。';
    } else {
      techInsight = '关注技术实现方案和创新点，评估技术可行性。';
    }
    
    // 商业视角
    let businessInsight = '';
    if (title.includes('raise') || title.includes('融资') || title.includes('$')) {
      businessInsight = '资本关注该领域，说明市场潜力和商业价值得到认可。';
    } else if (title.includes('market') || title.includes('market') || title.includes('市场')) {
      businessInsight = '市场动态变化，关注商业机会和竞争格局。';
    } else {
      businessInsight = '潜在商业机会，可进一步研究其变现模式和市场需求。';
    }
    
    // 用户视角
    let userInsight = '';
    if (title.includes('tutorial') || title.includes('guide') || title.includes('教程')) {
      userInsight = '用户学习需求旺盛，说明该工具/技术正在普及期。';
    } else if (title.includes('review') || title.includes('体验') || title.includes('测评')) {
      userInsight = '用户关注实际体验，产品成熟度和易用性是关键。';
    } else {
      userInsight = '解决用户痛点或满足用户需求，具有实用价值。';
    }
    
    // 趋势视角
    let trendInsight = '';
    if (category === 'AI') {
      trendInsight = 'AI 领域持续火热，从工具层到应用层都在快速发展。';
    } else if (category === 'TECH') {
      trendInsight = '技术生态不断完善，开发者工具和基础设施持续创新。';
    } else {
      trendInsight = '行业发展新动向，值得关注其长期影响和演进方向。';
    }
    
    return {
      tech: { ...this.perspectives.tech, insight: techInsight },
      business: { ...this.perspectives.business, insight: businessInsight },
      user: { ...this.perspectives.user, insight: userInsight },
      trend: { ...this.perspectives.trend, insight: trendInsight }
    };
  }

  /**
   * 计算文章热度等级
   * @param {Object} article - 文章数据
   * @returns {string} 热度等级
   */
  calculateHeatLevel(article) {
    const impressions = this.parseNumber(article.impressions);
    const likes = this.parseNumber(article.likes);
    const replies = this.parseNumber(article.replies);
    const reposts = this.parseNumber(article.reposts);
    
    // 计算综合热度分
    const heatScore = impressions * 0.5 + likes * 100 + replies * 200 + reposts * 150;
    
    if (heatScore >= 10000000) return '🔥🔥🔥 爆款';
    if (heatScore >= 1000000) return '🔥🔥 热门';
    if (heatScore >= 100000) return '🔥 较热';
    return '📌 普通';
  }

  /**
   * 提取关键词
   * @param {string} title - 文章标题
   * @returns {Array} 关键词列表
   */
  extractKeywords(title) {
    const commonKeywords = [
      'AI', 'Claude', 'GPT', 'OpenAI', 'LLM', 'Agent', 'Crypto', 'Bitcoin', 'Web3',
      'Blockchain', 'DeFi', 'NFT', 'Startup', 'SaaS', 'API', 'Cloud', 'DevOps',
      'Python', 'JavaScript', 'Rust', 'Go', 'React', 'Vue', 'Node.js', 'Docker',
      'Kubernetes', 'AWS', 'Azure', 'GCP', 'Database', 'AI Agent', 'RAG'
    ];
    
    const found = commonKeywords.filter(kw => 
      title.toLowerCase().includes(kw.toLowerCase())
    );
    
    return found.slice(0, 3); // 最多返回3个关键词
  }

  /**
   * 解析数字（处理 K, M 后缀）
   * @param {string} numStr - 数字字符串
   * @returns {number} 数值
   */
  parseNumber(numStr) {
    if (!numStr) return 0;
    const clean = numStr.toString().replace(/,/g, '');
    const num = parseFloat(clean.replace(/[KM]/gi, ''));
    
    if (clean.toUpperCase().includes('M')) return num * 1000000;
    if (clean.toUpperCase().includes('K')) return num * 1000;
    return num;
  }

  /**
   * 生成文章比较分析
   * @param {Array} articles - 文章列表
   * @returns {string} 比较分析文本
   */
  generateComparison(articles) {
    if (articles.length === 0) return '';
    
    // 按热度排序
    const sorted = [...articles].sort((a, b) => {
      const heatA = this.parseNumber(a.impressions);
      const heatB = this.parseNumber(b.impressions);
      return heatB - heatA;
    });
    
    const topArticle = sorted[0];
    const categories = {};
    
    articles.forEach(article => {
      const cat = article.category || 'Other';
      if (!categories[cat]) categories[cat] = [];
      categories[cat].push(article);
    });
    
    let analysis = `## 📊 文章对比分析\n\n`;
    analysis += `**最热门文章**: 《${topArticle.title}》 - ${topArticle.impressions} 浏览\n\n`;
    analysis += `**分类分布**:\n`;
    
    Object.entries(categories).forEach(([cat, items]) => {
      analysis += `- ${cat}: ${items.length} 篇\n`;
    });
    
    return analysis;
  }

  /**
   * 生成趋势总结
   * @param {Array} articles - 文章列表
   * @returns {string} 趋势总结
   */
  generateTrendSummary(articles) {
    const allKeywords = [];
    articles.forEach(article => {
      if (article.keywords) {
        allKeywords.push(...article.keywords);
      }
    });
    
    // 统计关键词频率
    const keywordCount = {};
    allKeywords.forEach(kw => {
      keywordCount[kw] = (keywordCount[kw] || 0) + 1;
    });
    
    // 获取热门关键词
    const topKeywords = Object.entries(keywordCount)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([kw]) => kw);
    
    if (topKeywords.length === 0) {
      return '暂无明确趋势关键词';
    }
    
    return `热门关键词: ${topKeywords.join(', ')}`;
  }
}

module.exports = ArticleAnalyzer;
