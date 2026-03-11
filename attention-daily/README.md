# Attention Daily Scripts

自动化抓取 AttentionVC.ai 数据并生成日报的脚本集合。

## 安装

```bash
npm install
```

## 使用

### 1. 运行完整流程（推荐）

```bash
npm run daily
# 或
node main.js
```

### 2. 单独运行模块

```bash
# 仅抓取数据
npm run fetch

# 仅生成报告
npm run generate
```

## 文件结构

```
scripts/
├── package.json          # 依赖配置
├── config.js             # 全局配置
├── main.js               # 入口文件
├── browser-automation.js # 浏览器自动化
├── data-extractor.js     # 数据提取
├── report-generator.js   # 报告生成
└── output/               # 输出目录
    ├── daily-data-*.json # 原始数据
    └── daily-report-*.md # 生成的日报
```

## 配置

编辑 `config.js` 调整参数：

```javascript
module.exports = {
  // 时间范围: '24h', '7d', '14d', 'All'
  source: {
    timeRange: '24h',
    categories: ['AI', 'Crypto', 'Tech'],
  },
  
  // 浏览器设置
  browser: {
    headless: false,  // false = 显示浏览器窗口
    waitTime: 2000,   // 点击后等待时间
  },
  
  // 提取设置
  extraction: {
    maxArticlesPerCategory: 5, // 每类提取文章数
  }
};
```

## 跨设备使用

1. 复制整个 `attention-daily` 目录到新设备
2. 运行 `npm install` 安装依赖
3. 确保已安装 Chromium/Chrome
4. 运行 `npm run daily`

## 输出示例

运行后会生成：
- `output/daily-data-*.json` - 原始抓取数据
- `output/daily-report-*.md` - Markdown 格式日报

## 依赖

- Node.js >= 14
- Playwright >= 1.40.0
