#!/usr/bin/env node
/**
 * Attention Daily - Main Entry Point
 * 
 * 日报生成主程序
 */

const BrowserAutomation = require('./browser-automation');
const ReportGenerator = require('./report-generator');
const config = require('./config');

async function main() {
  console.log('🚀 Attention Daily Report Generator');
  console.log('=====================================\n');

  const browser = new BrowserAutomation();
  const generator = new ReportGenerator();

  try {
    // 初始化浏览器
    console.log('🔧 Initializing browser...');
    await browser.init();

    // 抓取数据
    console.log('\n📊 Fetching data from AttentionVC.ai...');
    const data = await browser.fetchAllData();

    // 保存原始数据
    if (config.cache.enabled) {
      await browser.saveData(data, `daily-data-${Date.now()}.json`);
    }

    // 生成报告
    console.log('\n📝 Generating report...');
    const report = generator.generateReport(data);

    // 保存报告
    const reportPath = generator.saveReport(report, `daily-report-${Date.now()}.md`);

    console.log('\n✅ Done!');
    console.log(`📄 Report: ${reportPath}`);

    // 输出报告预览
    console.log('\n' + '='.repeat(50));
    console.log('REPORT PREVIEW:');
    console.log('='.repeat(50));
    console.log(report.substring(0, 1500) + '\n...');

  } catch (error) {
    console.error('\n❌ Error:', error.message);
    console.error(error.stack);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

// 运行主程序
main();
