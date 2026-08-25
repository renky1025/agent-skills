---
name: github-analyzer
description: |
  一键分析 GitHub 项目，搞清楚它是什么、有什么用、怎么用。
  触发词：分析 GitHub 项目、帮我看下这个项目、这个仓库是干啥的、分析开源项目、
  analyze repo、review this repo、这个项目有什么用。
  适用场景：用户提供 GitHub 仓库链接，需要快速理解项目的核心价值和上手方式。
agent_created: true
---

# GitHub 项目分析

## 概述

拿到 GitHub 仓库后，不搞面面俱到的评审，只回答用户真正关心的问题：
这个项目是干什么的、能解决什么问题、有什么亮点、怎么用。

默认读取环境变量 `https_proxy`/`http_proxy` 作为代理（若已设置，curl 自动走代理）；未设置则直连 GitHub。

## 分析流程

### 第 1 步：解析 URL

从用户输入提取 `owner/repo`。支持：
- `https://github.com/owner/repo`
- `github.com/owner/repo`
- `owner/repo`

含分支/tag 的 URL 忽略 fragment，只取仓库主体。

### 第 2 步：获取基础信息

获取仓库元数据和 README：

```bash
curl -s \
  "https://api.github.com/repos/{owner}/{repo}"
```

提取 Stars、语言、License、描述、创建/更新时间等基本字段，仅用于报告中一句话带过。

重点通过 WebFetch 获取 README 完整内容，从以下角度阅读和理解：
- 项目到底解决什么问题
- 核心功能是什么
- Quick Start / 安装方式
- 有哪些典型的用法和示例
- 相比同类方案有什么独到之处

### 第 3 步：深挖项目亮点

在理解 README 的基础上，进一步挖掘项目亮点：

1. 查看是否有独立的文档站点、Demo 链接
2. 关注项目描述中区别于竞品的独特卖点
3. 如果 README 提到具体性能数据、使用案例，重点记录
4. 结合项目所属领域，判断其解决的是真实痛点还是伪需求

### 第 4 步：输出报告

报告只包含以下 5 个章节，其他一律不写：

1. **这是什么** — 一句话说清楚项目定位，附 Stars/Language/License 基本卡片
2. **解决了什么问题** — 这个项目存在的理由，针对什么痛点
3. **有什么用** — 核心功能和典型使用场景
4. **怎么用** — Quick Start / 安装 / 上手方式，让读者看完就能行动
5. **亮点** — 区别于竞品的独特优势，为什么选它而不是别的

报告必须是实用导向的，读者看完能判断这个项目是否适合自己、以及如何开始使用。

**CRITICAL**：报告完成后必须：
1. 写入 `output/{repo-name}-analysis.md`
2. 调用 `present_files` 交付给用户
3. 同时在对话中给出简短摘要

## 注意事项

- 访问 GitHub API 自动使用 `https_proxy`/`http_proxy` 环境变量（若已设置）；未设置则直连。
- 当 API 遇到 rate limit (403)，提示用户可配置 GITHUB_TOKEN
- 保持客观，结合实际用途评价，不堆砌空洞的形容词
- 对于中国开发者关注的维度（中文支持、国内可用性）应额外注意
