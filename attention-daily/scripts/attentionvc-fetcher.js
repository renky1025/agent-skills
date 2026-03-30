/**
 * AttentionVC Article Fetcher
 * 
 * 从 attentionvc.ai 获取指定分类的热门文章
 */

const { chromium } = require('playwright');

class AttentionVCArticleFetcher {
  constructor() {
    this.baseUrl = 'https://www.attentionvc.ai/article';
    this.browser = null;
    this.page = null;
  }

  /**
   * 初始化浏览器
   */
  async init(headless = true) {
    this.browser = await chromium.launch({
      headless: headless,
    });
    this.page = await this.browser.newPage();
    this.page.setDefaultTimeout(60000);
  }

  /**
   * 关闭浏览器
   */
  async close() {
    if (this.browser) {
      await this.browser.close();
    }
  }

  /**
   * 获取指定分类的文章
   * @param {string} category - 分类 (tech, ai)
   * @param {string} window - 时间窗口 (1d, 7d, 14d, all)
   * @param {number} limit - 获取文章数量
   * @returns {Promise<Array>} 文章列表
   */
  async fetchArticlesByCategory(category, window = '1d', limit = 10) {
    const url = `${this.baseUrl}?window=${window}&category=${category}&lang=en%2Czh`;
    console.log(`📰 Fetching ${category} articles from ${url}`);
    
    try {
      await this.page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });

      // 等待内容加载
      await this.page.waitForTimeout(5000);
      
      // 检查是否需要等待加载
      const isLoading = await this.page.locator('text=Loading...').isVisible().catch(() => false);
      if (isLoading) {
        console.log('⏳ Waiting for content to load...');
        await this.page.waitForTimeout(2000);
      }
      
      // 提取文章数据
      const articles = await this.page.evaluate(({ maxCount, categoryParam }) => {
        const rows = document.querySelectorAll('table tbody tr');
        const results = [];

        rows.forEach((row, index) => {
          if (results.length >= maxCount) return;

          const cells = row.querySelectorAll('td');
          if (cells.length >= 4) {
            // 提取标题
            const titleText = cells[1]?.textContent || '';
            const title = titleText.split('·')[0]?.trim() || titleText;

            // 提取作者信息
            const authorText = cells[2]?.textContent?.trim() || '';
            const author = authorText.split('@')[0]?.trim() || authorText;
            const authorHandle = authorText.match(/@([\w_]+)/)?.[0] || '';
            const location = authorText.match(/·\s*(.+)$/)?.[1]?.trim() || '';

            // 提取浏览量和互动数据
            const impressionsText = cells[3]?.textContent?.trim() || '';
            const impressions = impressionsText.split(' ')[0] || '';
            const likes = impressionsText.match(/(\d+\.?\d*[KM]?)\s*♥/)?.[1] || '';
            const replies = impressionsText.match(/(\d+\.?\d*[KM]?)\s*💬/)?.[1] || '';
            const reposts = impressionsText.match(/(\d+\.?\d*[KM]?)\s*🔁/)?.[1] || '';

            // 获取文章链接
            const linkEl = cells[1]?.querySelector('a');
            const articleUrl = linkEl?.href || '';

            if (title && author) {
              results.push({
                rank: results.length + 1,
                title: title.trim(),
                author: author.trim(),
                authorHandle,
                location,
                impressions,
                likes,
                replies,
                reposts,
                articleUrl,
                category: categoryParam.toUpperCase()
              });
            }
          }
        });

        return results;
      }, { maxCount: limit, categoryParam: category });
      
      console.log(`✅ Fetched ${articles.length} ${category} articles`);
      return articles;
      
    } catch (error) {
      console.error(`❌ Error fetching ${category} articles:`, error.message);
      return [];
    }
  }

  /**
   * 获取多个分类的文章
   * @param {Array} categories - 分类列表 ['tech', 'ai']
   * @param {string} window - 时间窗口
   * @param {number} limitPerCategory - 每个分类获取数量
   * @returns {Promise<Object>} 按分类组织的文章数据
   */
  async fetchMultipleCategories(categories = ['tech', 'ai'], window = '1d', limitPerCategory = 10) {
    console.log(`🚀 Fetching articles from ${categories.length} categories...`);
    
    try {
      await this.init();
      
      const results = {};
      
      for (const category of categories) {
        console.log(`\n📥 Fetching ${category}...`);
        const articles = await this.fetchArticlesByCategory(category, window, limitPerCategory);
        results[category] = {
          category: category.toUpperCase(),
          articles,
          count: articles.length
        };
      }
      
      return results;
      
    } catch (error) {
      console.error('❌ Error fetching multiple categories:', error.message);
      return {};
    } finally {
      await this.close();
    }
  }
}

module.exports = AttentionVCArticleFetcher;
