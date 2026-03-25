/**
 * GitHub Trending Fetcher
 * 
 * 从 github.attentionvc.ai/trending/repos 获取当天最热的 GitHub 项目
 */

const { chromium } = require('playwright');

class GitHubTrendingFetcher {
  constructor() {
    this.url = 'https://github.attentionvc.ai/trending/repos';
    this.browser = null;
    this.page = null;
  }

  /**
   * 初始化浏览器
   */
  async init() {
    this.browser = await chromium.launch({
      headless: true,
    });
    this.page = await this.browser.newPage();
    this.page.setDefaultTimeout(30000);
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
   * 获取 GitHub Trending 数据
   * @param {number} limit - 获取项目数量，默认10个
   * @returns {Promise<Array>} 项目列表
   */
  async fetchTrendingRepos(limit = 10) {
    console.log('🚀 Fetching GitHub trending repos...');
    
    try {
      await this.init();
      
      console.log(`🌐 Navigating to ${this.url}`);
      await this.page.goto(this.url, { waitUntil: 'networkidle' });
      
      // 等待页面加载
      await this.page.waitForTimeout(3000);
      
      // 提取项目数据
      const repos = await this.page.evaluate((maxCount) => {
        const repoCards = document.querySelectorAll('[class*="repo-card"], .repo-item, [data-testid*="repo"], tr');
        const results = [];
        
        repoCards.forEach((card, index) => {
          if (results.length >= maxCount) return;
          
          // 尝试多种选择器获取数据
          const nameEl = card.querySelector('h3 a, .repo-name a, [class*="name"] a, td a');
          const descEl = card.querySelector('p, .description, [class*="desc"]');
          const starsEl = card.querySelector('[class*="star"], .stars, [class*="count"]');
          const langEl = card.querySelector('[class*="language"], .lang, [class*="programming"]');
          
          if (nameEl) {
            const name = nameEl.textContent?.trim() || '';
            const description = descEl?.textContent?.trim() || '';
            const stars = starsEl?.textContent?.trim() || '';
            const language = langEl?.textContent?.trim() || 'N/A';
            const url = nameEl.href || `https://github.com/${name}`;
            
            if (name && name.includes('/')) {
              results.push({
                rank: results.length + 1,
                name,
                description,
                stars,
                language,
                url
              });
            }
          }
        });
        
        return results;
      }, limit);
      
      console.log(`✅ Fetched ${repos.length} trending repos`);
      return repos;
      
    } catch (error) {
      console.error('❌ Error fetching GitHub trending:', error.message);
      return [];
    } finally {
      await this.close();
    }
  }

  /**
   * 获取项目详细信息
   * @param {Array} repos - 项目列表
   * @returns {Promise<Array>} 带详细信息的项目列表
   */
  async enrichRepoDetails(repos) {
    console.log('🔍 Enriching repo details...');
    
    const enriched = [];
    
    for (const repo of repos) {
      try {
        // 解析项目名称
        const [owner, projectName] = repo.name.split('/');
        
        if (owner && projectName) {
          // 构建 GitHub API URL
          const apiUrl = `https://api.github.com/repos/${owner.trim()}/${projectName.trim()}`;
          
          // 这里可以添加 API 调用获取更多信息
          // 由于可能有 rate limit，暂时跳过
          
          enriched.push({
            ...repo,
            owner: owner.trim(),
            projectName: projectName.trim(),
            simpleDescription: this.summarizeDescription(repo.description)
          });
        } else {
          enriched.push({
            ...repo,
            simpleDescription: this.summarizeDescription(repo.description)
          });
        }
      } catch (error) {
        enriched.push({
          ...repo,
          simpleDescription: this.summarizeDescription(repo.description)
        });
      }
    }
    
    return enriched;
  }

  /**
   * 简化项目描述
   * @param {string} description - 原始描述
   * @returns {string} 简化描述
   */
  summarizeDescription(description) {
    if (!description) return '暂无描述';
    
    // 限制长度并清理
    const cleanDesc = description
      .replace(/\n/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
    
    if (cleanDesc.length > 100) {
      return cleanDesc.substring(0, 100) + '...';
    }
    
    return cleanDesc;
  }
}

module.exports = GitHubTrendingFetcher;
