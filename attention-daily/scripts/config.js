/**
 * Attention Daily - Configuration
 * 
 * 配置文件：包含所有可调整的参数
 */

module.exports = {
  // 数据源配置
  source: {
    url: 'https://www.attentionvc.ai/article',
    timeRange: '24h', // 可选: '24h', '7d', '14d', 'All'
    categories: ['AI', 'Crypto', 'Tech'],
    languages: 'en,zh', // English & Chinese
  },

  // 浏览器配置
  browser: {
    headless: false, // true = 无头模式，false = 可见浏览器
    timeout: 30000, // 页面加载超时时间 (ms)
    waitTime: 2000, // 点击后等待时间 (ms)
    checkLoading: true, // 是否检查 Loading 状态
  },

  // 数据提取配置
  extraction: {
    maxArticlesPerCategory: 5, // 每个类别提取的文章数
    selectors: {
      tableRows: 'table tbody tr',
      titleCell: 'td:nth-child(2)',
      authorCell: 'td:nth-child(3)',
      impressionsCell: 'td:nth-child(4)',
      categoryButtons: '[role="button"]', 
      timeRangeButtons: {
        '24h': 'button:has-text("24h")',
        '7d': 'button:has-text("7d")',
        '14d': 'button:has-text("14d")',
        'All': 'button:has-text("All")',
      }
    }
  },

  // 输出配置
  output: {
    format: 'markdown', // 可选: 'markdown', 'json', 'html'
    includeTrends: true,
    includePostOptions: true,
    postOptionsCount: 5,
  },

  // 缓存配置
  cache: {
    enabled: true,
    filePath: './cache/daily-cache.json',
    ttl: 3600000, // 缓存有效期 1小时 (ms)
  }
};
