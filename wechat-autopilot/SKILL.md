---
name: wechat-autopilot
description: Automated WeChat Official Account content creation and publishing system. Fetches news from Google News RSS, generates AI-written articles with AI-generated images, and publishes to WeChat Official Account. Use when users want to "自动发公众号", "小龙虾发文", "AI自动写文章发公众号", "公众号自动化运营", or create a content automation pipeline for WeChat.
---

# WeChat AutoPilot - 公众号自动化运营系统

全自动收集资讯 → AI 生成文章 → AI 配图 → 自动发布到微信公众号

## 核心功能

1. **📰 资讯收集** - Google News RSS API 自动抓取
2. **✍️ 文章生成** - AI 整理改写，支持多种风格
3. **🎨 配图生成** - 文生图 API 自动生成封面+正文配图
4. **📤 自动发布** - 微信公众号 API 自动发文
5. **⏰ 定时任务** - 可设置每日定时执行

## 快速开始

### 第一步：准备工作

需要准备以下材料：

| 材料 | 获取方式 | 用途 |
|------|----------|------|
| 微信公众号 | mp.weixin.qq.com | 发文平台 |
| 微信开发者平台 | mp.weixin.qq.com/advanced/advanced | 获取 API 密钥 |
| 文生图 API Key | tuziapi.com | 生成文章配图 |

### 第二步：微信开发者平台配置

1. 访问 https://mp.weixin.qq.com/advanced/advanced
2. 登录后找到你的公众号
3. 点击「开发密钥」→ 重置 AppSecret
4. 记录 **AppID** 和 **AppSecret**
5. **设置 IP 白名单**：
   - 填入：`155.94.132.10`
   - 这是共享代理服务器，方便没有固定 IP 的用户使用

### 第三步：配置 Skill

使用 `/wechat-autopilot setup` 命令，按提示输入：

```
WECHAT_APP_ID=你的AppID
WECHAT_APP_SECRET=你的AppSecret
IMAGE_API_KEY=你的文生图API密钥
IMAGE_STYLE=配图风格（可选，默认mondo）
NEWS_KEYWORDS=关键词（如：AI,科技,创业）
POST_TIME=定时发布时间（如：18:00）
```

### 第四步：运行

输入 `/wechat-autopilot run` 即可开始自动化流程

或者输入 `/wechat-autopilot daily` 启动每日定时任务

## 完整工作流程

```
┌─────────────────────────────────────────────────────────┐
│                    每日定时任务启动                       │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│  1. 收集资讯                                             │
│     • 调用 Google News RSS API                          │
│     • 按关键词筛选相关新闻                                │
│     • 获取 5-10 条最新资讯                                │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│  2. AI 整理生成文章                                       │
│     • 分析新闻要点                                        │
│     • 按指定风格撰写文章                                  │
│     • 生成标题、导语、正文、结尾                          │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│  3. AI 生成配图                                           │
│     • 生成封面图 (900x383)                               │
│     • 生成正文配图 1-2 张                                 │
│     • 使用指定风格（如 mondo）                            │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│  4. 发布到公众号                                          │
│     • 获取 access_token                                  │
│     • 上传图片素材                                        │
│     • 创建图文消息                                        │
│     • 发布文章                                            │
└─────────────────────────────────────────────────────────┘
```

## 写作风格配置

推荐使用的写作风格：

### 🎤 脱口秀风格（推荐）
```
模仿脱口秀演员的文风：
- 语言犀利、通俗易懂
- 带点幽默和反讽
- 观点明确、立场鲜明
- 用口语化表达复杂概念
```

### 📰 新闻评论风格
```
- 客观陈述事实
- 加入深度分析
- 引用多方观点
- 给出独到见解
```

### 📚 科普教育风格
```
- 由浅入深讲解
- 多用类比和例子
- 分点列出要点
- 总结核心结论
```

### 💼 商业分析风格
```
- 聚焦商业价值
- 分析市场机会
- 引用数据和案例
- 给出行动建议
```

## 配图风格推荐

### Mondo 风格（推荐）
- 复古海报风格
- 色彩鲜艳
- 适合科技、文化类文章

### 摄影写实风格
- 真实感强
- 适合新闻、纪实类文章

### 插画风
- 简洁明快
- 适合轻松、生活类文章

## API 参考

### Google News RSS
```
https://news.google.com/rss/search?q={关键词}&hl=zh-CN&gl=CN&ceid=CN:zh
```

### 文生图 API (TuziAPI)
```
POST https://api.tuziapi.com/v1/images/generations
Headers:
  Authorization: Bearer {API_KEY}
Body:
  {
    "model": "nanobanana",
    "prompt": "图片描述",
    "size": "1024x1024",
    "style": "mondo"
  }
```

### 微信公众号 API

**获取 access_token**
```
GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}
```

**上传图片**
```
POST https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={ACCESS_TOKEN}
Content-Type: multipart/form-data
Body: media=@image.jpg
```

**发布图文消息**
```
POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token={ACCESS_TOKEN}
Body:
{
  "articles": [{
    "title": "文章标题",
    "author": "作者",
    "digest": "摘要",
    "content": "图文消息具体内容",
    "content_source_url": "原文链接",
    "thumb_media_id": "封面图片素材ID",
    "need_open_comment": 1,
    "only_fans_can_comment": 0
  }]
}
```

## 实战案例

### 案例 1：AI 科技资讯号

**配置：**
- 关键词：`AI,人工智能,ChatGPT,Claude,OpenAI`
- 写作风格：脱口秀风格
- 配图风格：mondo
- 发布频率：每天 2 次（10:00, 18:00）

**效果：**
- 每篇文章成本：约 1-1.5 元（API 费用）
- 平均阅读量：300-500
- 爆文：1 篇 10w+，1 篇 1.8w+

### 案例 2：创业投资观察

**配置：**
- 关键词：`创业,投资,融资,startup,VC`
- 写作风格：商业分析风格
- 配图风格：摄影写实
- 发布频率：每天 1 次（20:00）

## 收益与成本分析

### 成本

| 项目 | 单价 | 每篇文章 | 每月（30篇） |
|------|------|----------|-------------|
| AI 写作 (API) | ~$0.01/1K tokens | ~¥0.3 | ~¥9 |
| 配图 (nanobanana) | ¥0.4/张 | ~¥1.2 (3张) | ~¥36 |
| **总计** | - | **~¥1.5** | **~¥45** |

### 收益

- 流量主广告（500粉开通）：阅读量 × eCPM
- 平均 500 阅读 ≈ ¥2-5/篇
- 爆文收益：1w+ 阅读 ≈ ¥50-200

### ROI 计算

- 投入：¥1.5/篇
- 平均产出：¥3/篇
- **ROI：约 200%**

## 进阶技巧

### 1. 提高阅读量的技巧

1. **标题优化**
   - 使用数字：`3个方法`、`5大趋势`
   - 制造悬念：`震惊！`、`原来如此`
   - 蹭热点：结合当日热搜

2. **发布时间**
   - 早高峰：7:30-9:00
   - 午休：12:00-13:30
   - 晚高峰：18:00-20:00
   - 睡前：22:00-23:00

3. **内容策略**
   - 标原创（AI 生成也可标原创）
   - 打开「平台推荐」
   - 控制文章长度（800-1500字最佳）

### 2. 多账号运营

- 一个配置可管理多个公众号
- 每个号不同细分领域
- 分散风险，提高整体收益

### 3. 内容优化

定期分析数据：
- 哪些标题点击率高
- 什么话题阅读完成率高
- 读者留言反馈

用这些数据优化提示词，提升内容质量

## 常见问题

### Q1: AI 生成的文章能标原创吗？
A: 可以。公众号原创审核不检测 AI 生成，主要查重。只要内容不是直接复制，都可以标原创。

### Q2: 需要声明「内容由 AI 生成」吗？
A: 目前政策未强制要求。建议自行评估风险，教程原作者选择不声明。

### Q3: 没有服务器能用吗？
A: 可以。使用共享代理 IP `155.94.132.10`，本地电脑或手机即可运行。

### Q4: 文章质量如何提升？
A: 
1. 优化提示词，指定具体风格
2. 增加人工审核环节
3. 根据数据反馈迭代
4. 热点+深度结合

### Q5: 配图有版权问题吗？
A: AI 生成的图片属于原创，无版权问题。

## 风险提示

1. **平台政策风险**：微信公众号可能调整原创规则
2. **内容质量风险**：AI 可能生成不准确信息，建议人工审核
3. **封号风险**：频繁发文可能被判定为营销号，建议控制频率
4. **API 稳定性**：依赖第三方 API，建议准备备用方案

## 执行命令参考

```bash
# 初始化配置
/wechat-autopilot setup

# 立即运行一次
/wechat-autopilot run

# 启动每日定时任务
/wechat-autopilot daily

# 手动收集资讯
/wechat-autopilot fetch

# 生成文章（不传公众号）
/wechat-autopilot draft

# 查看统计
/wechat-autopilot stats
```

## 参考资料

- [微信开发者文档](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html)
- [Google News RSS 文档](https://developers.google.com/news)
- [TuziAPI 文档](https://tuziapi.com/docs)

---

**记住：** 自动化是工具，内容是核心。持续优化内容质量，才能获得长期收益。
