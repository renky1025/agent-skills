#!/usr/bin/env node
/**
 * Attention Daily - Main Entry Point (Enhanced Version)
 * 
 * 增强版日报生成主程序
 * - Part 1: GitHub Trending 热门项目
 * - Part 2: AttentionVC.ai 热门文章分析
 */

const GitHubTrendingFetcher = require('./github-trending');
const AttentionVCArticleFetcher = require('./attentionvc-fetcher');
const ArticleAnalyzer = require('./article-analyzer');
const ReportGenerator = require('./report-generator');

async function main() {
  console.log('🚀 Attention Daily Report Generator (Enhanced v2.0)');
  console.log('====================================================\n');

  const githubFetcher = new GitHubTrendingFetcher();
  const articleFetcher = new AttentionVCArticleFetcher();
  const analyzer = new ArticleAnalyzer();
  const generator = new ReportGenerator();

  try {
    // ========== Part 1: GitHub Trending ==========
    console.log('📦 Part 1: Fetching GitHub Trending Repos...');
    console.log('-'.repeat(50));
    
    const githubRepos = await githubFetcher.fetchTrendingRepos(10);
    const enrichedRepos = await githubFetcher.enrichRepoDetails(githubRepos);
    
    console.log(`✅ Fetched ${enrichedRepos.length} GitHub repos\n`);

    // ========== Part 2: AttentionVC Articles ==========
    console.log('📰 Part 2: Fetching AttentionVC Articles...');
    console.log('-'.repeat(50));
    
    // 获取 Tech 和 AI 分类的文章
    const articleCategories = ['tech', 'ai'];
    const attentionvcArticles = await articleFetcher.fetchMultipleCategories(
      articleCategories, 
      '1d',  // 24小时
      10     // 每个分类10篇
    );
    
    // 分析文章
    console.log('\n🔍 Analyzing articles...');
    let totalArticles = 0;
    
    Object.keys(attentionvcArticles).forEach(category => {
      if (attentionvcArticles[category].articles) {
        const analyzed = analyzer.analyzeArticles(
          attentionvcArticles[category].articles
        );
        attentionvcArticles[category].articles = analyzed;
        totalArticles += analyzed.length;
      }
    });
    
    console.log(`✅ Analyzed ${totalArticles} articles\n`);

    // ========== Generate Report ==========
    console.log('📝 Generating comprehensive report...');
    console.log('-'.repeat(50));
    
    const reportData = {
      timestamp: new Date().toISOString(),
      githubRepos: enrichedRepos,
      attentionvcArticles: {
        categories: attentionvcArticles,
        totalCount: totalArticles
      }
    };
    
    const report = generator.generateReport(reportData);
    
    // 保存报告
    const timestamp = new Date().toISOString().split('T')[0];
    const reportPath = generator.saveReport(report, `daily-report-${timestamp}.md`);
    
    console.log('\n✅ Report generation complete!');
    console.log(`📄 Report saved: ${reportPath}`);
    
    // 输出报告预览
    console.log('\n' + '='.repeat(60));
    console.log('REPORT PREVIEW:');
    console.log('='.repeat(60));
    console.log(report.substring(0, 2000) + '\n...');
    
    // 输出统计信息
    console.log('\n📊 Summary Statistics:');
    console.log('-'.repeat(60));
    console.log(`GitHub Projects: ${enrichedRepos.length}`);
    console.log(`Tech Articles: ${attentionvcArticles.tech?.articles?.length || 0}`);
    console.log(`AI Articles: ${attentionvcArticles.ai?.articles?.length || 0}`);
    console.log(`Total Articles: ${totalArticles}`);
    
  } catch (error) {
    console.error('\n❌ Error:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

// 运行主程序
main();
