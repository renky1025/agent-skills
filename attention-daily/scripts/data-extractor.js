/**
 * Attention Daily - Data Extractor
 * 
 * 从页面提取文章数据
 */

const config = require('./config');

class DataExtractor {
  constructor() {
    this.selectors = config.extraction.selectors;
  }

  /**
   * 提取文章数据
   * @param {Page} page - Playwright page 对象
   * @returns {Promise<Array>} 文章列表
   */
  async extractArticles(page) {
    return await page.evaluate((selectors, maxCount) => {
      const rows = document.querySelectorAll(selectors.tableRows);
      const articles = [];
      
      rows.forEach((row, index) => {
        if (index >= maxCount) return;
        
        const cells = row.querySelectorAll('td');
        if (cells.length >= 4) {
          // 提取标题（去掉日期和字数信息）
          const titleText = cells[1]?.textContent || '';
          const title = titleText.split('·')[0]?.trim() || titleText;
          
          // 提取作者（去掉 @handle 和位置）
          const authorText = cells[2]?.textContent?.trim() || '';
          const author = authorText.split('@')[0]?.trim() || authorText;
          const authorHandle = authorText.match(/@(\w+)/)?.[0] || '';
          const location = authorText.match(/·\s*(.+)$/)?.[1]?.trim() || '';
          
          // 提取浏览量（第一个数字）
          const impressionsText = cells[3]?.textContent?.trim() || '';
          const impressionsParts = impressionsText.split(' ');
          const impressions = impressionsParts[0] || '';
          
          // 提取互动数据
          const engagementText = cells[3]?.textContent || '';
          const likes = engagementText.match(/(\d+\.?\d*[KM]?)\s*♥/)?.[1] || '';
          const replies = engagementText.match(/(\d+\.?\d*[KM]?)\s*💬/)?.[1] || '';
          const reposts = engagementText.match(/(\d+\.?\d*[KM]?)\s*🔁/)?.[1] || '';
          const quotes = engagementText.match(/(\d+\.?\d*[KM]?)\s*📊/)?.[1] || '';
          
          articles.push({
            rank: index + 1,
            title,
            author,
            authorHandle,
            location,
            impressions,
            likes,
            replies,
            reposts,
            quotes,
            rawEngagement: impressionsText
          });
        }
      });
      
      return articles;
    }, this.selectors, config.extraction.maxArticlesPerCategory);
  }

  /**
   * 提取页面统计信息
   * @param {Page} page - Playwright page 对象
   * @returns {Promise<Object>} 统计信息
   */
  async extractStats(page) {
    return await page.evaluate(() => {
      // 查找文章数量
      const articleCountText = document.querySelector('[class*="text-"]')?.textContent || '';
      const articleCount = articleCountText.match(/(\d+)\s+articles?/)?.[1] || '0';
      
      // 查找更新时间
      const updateText = document.querySelector('p')?.textContent || '';
      const updated = updateText.match(/Updated\s+(.+?)\s+ago/)?.[1] || 'unknown';
      
      return {
        articleCount: parseInt(articleCount) || 0,
        updated,
      };
    });
  }

  /**
   * 格式化 engagement 数据
   * @param {string} impressions - 浏览量
   * @param {string} likes - 点赞数
   * @param {string} replies - 回复数
   * @returns {string} 格式化后的互动数据
   */
  formatEngagement(impressions, likes, replies) {
    const parts = [];
    if (likes) parts.push(`${likes}♥`);
    if (replies) parts.push(`${replies}💬`);
    return parts.join(' ');
  }
}

module.exports = DataExtractor;
