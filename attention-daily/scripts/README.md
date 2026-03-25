# Attention Daily Scripts (v2.0)

自动化抓取 **GitHub Trending** 和 **AttentionVC.ai** 数据，生成增强版科技情报日报。

## ✨ 新功能 (v2.0)

### 🔥 Part 1: GitHub 热门项目
- 自动获取 github.attentionvc.ai/trending/repos 的 Top 10 项目
- 包含项目名、语言、Stars、简介
- 项目亮点总结和趋势分析

### 📰 Part 2: 热门文章深度分析
- 从 AttentionVC.ai 获取 Tech 和 AI 分类的文章（各10篇）
- **多视角点评**: 技术、商业、用户、趋势四个视角
- **智能分析**: 关键词提取、热度计算、内容总结
- 每篇文章配有详细解读

### 🎯 智能总结
- GitHub 项目与社区讨论的关联分析
- 关键趋势和洞察自动生成
- 热门关键词统计

## 📋 报告结构

```
📊 Attention Daily Digest - {Date}
├── 📈 今日概览
├── 🔥 Part 1: GitHub 热门项目 (Top 10)
│   ├── 项目列表表格
│   └── 项目亮点总结
├── 📰 Part 2: 热门文章分析
│   ├── 💻 Tech 领域 (Top 10)
│   │   └── 每篇文章详情 + 多视角解读
│   ├── 🤖 AI 领域 (Top 10)
│   │   └── 每篇文章详情 + 多视角解读
│   └── 📊 总体分析
└── 🎯 今日总结
    ├── 两部分内容关联
    └── 关键洞察
```

## 🚀 使用方法

### 1. 安装依赖

```bash
cd scripts
npm install
```

### 2. 运行日报生成

```bash
npm run daily
# 或
node main.js
```

### 3. 查看报告

报告将保存到 `scripts/output/daily-report-{date}.md`

## 📊 数据流程

```
GitHub Trending (10 repos)    AttentionVC.ai (Tech + AI articles)
         │                              │
         ▼                              ▼
  github-trending.js           attentionvc-fetcher.js
         │                              │
         ▼                              ▼
  项目数据 (名称/语言/Stars)     文章数据 (标题/作者/浏览量)
         │                              │
         │                     article-analyzer.js
         │                              │
         │                     多视角分析/总结/关键词
         │                              │
         └───────────┬──────────────────┘
                     ▼
         ┌──────────────────────┐
         │   report-generator.js │
         │   整合生成完整报告    │
         └──────────┬───────────┘
                    ▼
         ┌──────────────────────┐
         │ output/daily-report-*.md │
         └──────────────────────┘
```

## 🔍 文章分析视角

每个热门文章都会从四个视角进行分析：

| 视角 | Emoji | 关注点 |
|------|-------|--------|
| **技术视角** | 💻 | 技术创新、实现方案、技术栈 |
| **商业视角** | 💼 | 商业模式、市场机会、投资价值 |
| **用户视角** | 👥 | 用户体验、使用场景、痛点解决 |
| **趋势视角** | 📈 | 行业趋势、未来方向、技术演进 |

## ⚙️ 配置

编辑 `config.js`:

```javascript
module.exports = {
  source: {
    github: {
      url: 'https://github.attentionvc.ai/trending/repos',
      maxRepos: 10,
    },
    attentionvc: {
      url: 'https://www.attentionvc.ai/article',
      categories: ['tech', 'ai'],
      window: '1d',  // '1d', '7d', '14d', 'all'
      maxArticlesPerCategory: 10,
    }
  },
  
  browser: {
    headless: true,  // true = 无头模式
    timeout: 30000,
    waitTime: 3000,
  },
  
  analysis: {
    enabled: true,
    perspectives: ['tech', 'business', 'user', 'trend'],
  },
  
  output: {
    format: 'markdown',
    includeGitHub: true,
    includeArticles: true,
    includeAnalysis: true,
  }
};
```

## 📁 文件结构

```
attention-daily/
├── SKILL.md                     # Skill 文档
├── scripts/
│   ├── package.json             # 依赖配置
│   ├── config.js                # 配置文件 (已更新)
│   ├── main.js                  # 主程序入口 (已更新)
│   ├── github-trending.js       # GitHub 数据获取 (新增)
│   ├── attentionvc-fetcher.js   # AttentionVC 数据获取 (新增)
│   ├── article-analyzer.js      # 文章分析模块 (新增)
│   ├── report-generator.js      # 报告生成器 (已更新)
│   ├── browser-automation.js    # 旧版浏览器自动化 (保留)
│   ├── data-extractor.js        # 旧版数据提取 (保留)
│   └── output/                  # 输出目录
└── references/
```

## 🔧 技术栈

- **Node.js** - 运行时环境
- **Playwright** - 浏览器自动化
- **Markdown** - 报告格式

## 📝 更新日志

### v2.0 (2026-03-25)
- ✨ 新增 GitHub Trending 项目获取
- ✨ 新增文章多视角分析功能
- ✨ 新增智能总结和洞察生成
- ✨ 增强报告格式和内容
- ✨ 支持 Tech 和 AI 分类文章
- ✨ 热度计算和关键词提取

### v1.0
- 基础版本：AttentionVC.ai 数据获取
- 支持 AI, Crypto, Tech 三个分类

## 🐛 故障排除

### 浏览器启动失败
```bash
# 安装 Playwright 浏览器
npx playwright install chromium
```

### 数据获取超时
- 检查网络连接
- 增加 config.js 中的 timeout 值
- 尝试使用 headless: false 查看浏览器行为

### 报告生成失败
- 检查 output 目录是否存在
- 检查磁盘空间

## 📄 License

MIT
