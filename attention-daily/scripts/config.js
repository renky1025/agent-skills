/**
 * Attention Daily - Configuration (Enhanced)
 * 
 * 配置文件：包含所有可调整的参数
 */

module.exports = {
  // 数据源配置
  source: {
    // AttentionVC.ai 配置
    attentionvc: {
      url: 'https://www.attentionvc.ai/article',
      categories: ['tech', 'ai'], // 文章分类
      window: '7d', // 时间窗口: '1d', '7d', '14d', 'all'
      languages: 'en,zh',
      maxArticlesPerCategory: 10,
    },
    // GitHub Trending 配置
    github: {
      url: 'https://github.attentionvc.ai/trending/repos',
      maxRepos: 10,
    }
  },

  // 浏览器配置
  browser: {
    headless: true, // true = 无头模式，false = 可见浏览器
    timeout: 30000, // 页面加载超时时间 (ms)
    waitTime: 3000, // 点击后等待时间 (ms)
    checkLoading: true, // 是否检查 Loading 状态
  },

  // 数据提取配置
  extraction: {
    maxArticlesPerCategory: 10, // 每个类别提取的文章数
    selectors: {
      tableRows: 'table tbody tr',
      titleCell: 'td:nth-child(2)',
      authorCell: 'td:nth-child(3)',
      impressionsCell: 'td:nth-child(4)',
    }
  },

  // 文章分析配置
  analysis: {
    enabled: true,
    perspectives: ['tech', 'business', 'user', 'trend'], // 分析视角
    generateSummary: true,
    extractKeywords: true,
  },

  // 输出配置
  output: {
    format: 'markdown',
    includeGitHub: true,
    includeArticles: true,
    includeAnalysis: true,
    includeTrends: true,
  },

  // 缓存配置
  cache: {
    enabled: true,
    filePath: './cache/daily-cache.json',
    ttl: 3600000, // 缓存有效期 1小时 (ms)
  }
};
