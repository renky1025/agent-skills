/**
 * Attention Daily - Browser Automation
 * 
 * 浏览器自动化模块：处理页面导航和数据抓取
 */

const { chromium } = require('playwright');
const config = require('./config');
const DataExtractor = require('./data-extractor');

class BrowserAutomation {
  constructor() {
    this.browser = null;
    this.page = null;
    this.extractor = new DataExtractor();
  }

  /**
   * 初始化浏览器
   */
  async init() {
    this.browser = await chromium.launch({
      headless: config.browser.headless,
    });
    this.page = await this.browser.newPage();
    this.page.setDefaultTimeout(config.browser.timeout);
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
   * 检查页面是否正在加载
   * @returns {Promise<boolean>}
   */
  async isLoading() {
    try {
      const loadingText = await this.page.locator('text=Loading...').isVisible();
      return loadingText;
    } catch {
      return false;
    }
  }

  /**
   * 导航到数据源页面
   */
  async navigateToSource() {
    console.log(`🌐 Navigating to ${config.source.url}`);
    await this.page.goto(config.source.url);
    
    // 检查是否需要等待加载
    if (config.browser.checkLoading) {
      const isLoading = await this.isLoading();
      if (isLoading) {
        console.log('⏳ Waiting for content to load...');
        await this.page.waitForTimeout(config.browser.waitTime);
      }
    }
  }

  /**
   * 选择时间范围
   * @param {string} range - 时间范围 ('24h', '7d', '14d', 'All')
   */
  async selectTimeRange(range = config.source.timeRange) {
    console.log(`⏱️  Selecting time range: ${range}`);
    
    try {
      await this.page.getByRole('button', { name: range }).click();
      await this.page.waitForTimeout(config.browser.waitTime);
      console.log(`✅ Time range set to ${range}`);
    } catch (error) {
      console.warn(`⚠️  Could not select time range ${range}:`, error.message);
    }
  }

  /**
   * 点击类别按钮
   * @param {string} category - 类别名称
   */
  async selectCategory(category) {
    console.log(`🏷️  Selecting category: ${category}`);
    
    try {
      // 尝试匹配类别按钮（包含文章数量的按钮，如 "AI12", "Crypto2"）
      const categoryButton = this.page.locator('button', { 
        hasText: new RegExp(`${category}\\d+`, 'i')
      });
      
      if (await categoryButton.isVisible()) {
        await categoryButton.click();
        await this.page.waitForTimeout(config.browser.waitTime);
        console.log(`✅ Category ${category} selected`);
      } else {
        console.warn(`⚠️  Category button ${category} not found`);
      }
    } catch (error) {
      console.warn(`⚠️  Could not select category ${category}:`, error.message);
    }
  }

  /**
   * 获取单个类别的数据
   * @param {string} category - 类别名称
   * @returns {Promise<Object>} 类别数据
   */
  async fetchCategoryData(category) {
    await this.selectCategory(category);
    
    const articles = await this.extractor.extractArticles(this.page);
    const stats = await this.extractor.extractStats(this.page);
    
    return {
      category,
      articles,
      stats,
    };
  }

  /**
   * 获取所有类别的数据
   * @returns {Promise<Object>} 完整数据
   */
  async fetchAllData() {
    console.log('📊 Starting data fetch...');
    
    await this.navigateToSource();
    await this.selectTimeRange();
    
    const allData = {
      timestamp: new Date().toISOString(),
      timeRange: config.source.timeRange,
      categories: {},
    };

    for (const category of config.source.categories) {
      console.log(`\n📥 Fetching ${category}...`);
      const data = await this.fetchCategoryData(category);
      allData.categories[category.toLowerCase()] = data;
      console.log(`✅ ${category}: ${data.articles.length} articles fetched`);
    }

    return allData;
  }

  /**
   * 保存数据到文件
   * @param {Object} data - 要保存的数据
   * @param {string} filename - 文件名
   */
  async saveData(data, filename = 'daily-data.json') {
    const fs = require('fs');
    const path = require('path');
    
    const outputDir = path.join(__dirname, 'output');
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    
    const filepath = path.join(outputDir, filename);
    fs.writeFileSync(filepath, JSON.stringify(data, null, 2));
    console.log(`💾 Data saved to ${filepath}`);
    return filepath;
  }
}

module.exports = BrowserAutomation;
