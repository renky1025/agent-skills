---
title: Google 扔出王炸！一个命令搞定 Gmail、Drive、Calendar，AI 还能帮你回邮件
angle: 热点 + 效率爽点
structure: 场景故事 → 功能演示 → 情绪高潮
emotion: 爽感（终于不用手动操作了）
---

# Google 扔出王炸！一个命令搞定 Gmail、Drive、Calendar，AI 还能帮你回邮件

你有没有想过——

有一天，你只需要坐在终端前，敲下一行命令，就能：
- 发邮件
- 整理 Drive 文件
- 创建日历事件
- 更是——**让 AI 帮你回邮件**

就在昨天，Google 开源了一个命令行工具，**一天暴涨 13000+ Star**。

它叫 **gws**（Google Workspace CLI）。

---

## 01

我叫老王。

每天早上到公司，我得干这么几件事：

1. 打开 Gmail，看看有没有重要邮件（平均 50+ 未读）
2. 打开 Google Drive，找上周那个文档
3. 打开 Calendar，确认今天有啥会
4. 打开 Sheets，更新一下昨天的数据

一套下来，半小时没了。

关键是——**这些破事每天重复，做多了真的会吐。**

我相信你也好不到哪去。

---

## 02

gws 来了。

它把整个 Google 办公套件——Gmail、Drive、Docs、Sheets、Calendar、Chat、Admin——全部搬进了终端。

什么意思？

**你不需要再点来点去了。**

发个邮件？
```bash
gws gmail users messages create --json '{"subject": "Hello"}'
```

列个文件？
```bash
gws drive files list --params '{"pageSize": 10}'
```

建个表格？
```bash
gws sheets spreadsheets create --json '{"properties": {"title": "Q1 Budget"}}'
```

一行命令，完事。

---

## 03

但最让我爽到的，是它自带的 **AI Agent Skills**。

什么意思？

你可以让 AI 帮你**回邮件**。

不是那种智障的自动回复。是真真正正帮你读邮件、分析内容、然后帮你写回复。

> "帮我回了这封邮件，语气客气一点，顺便把附件存到 Drive 里。"

一行指令，AI 帮你干活。

**这感觉，就像雇了个 24 小时待命的助理。**

---

## 04

为什么这次这么火？

因为它解决了两个终极痛点：

**第一，麻烦。**
Google Workspace 很好，但操作成本太高。点点点，切换来切换去——一天下来，光操作软件就耗掉半条命。

**第二，重复。**
那些破事本来就不该人干。列文件、归邮件、填表格——这种脏活累活，交给命令行才是正途。

而 gws，直接把门槛砸到了地板。

> 不需要写 curl，不需要看 API 文档，敲命令就行。

---

## 05

当然，有人会问：

"这不就是个 CLI 吗？能有 GUI 好用？"

我的答案是：**对于重复性任务，CLI 才是 yyds。**

你想啊——

- 每天要发的固定报告，手一抖就完成了
- 每周要整理的文件，设定好脚本就行
- 甚至可以让 AI 自动处理邮件分类

**这些事，你用鼠标点一年，CLI 10 分钟搞定。**

而且，它还支持 MCP（Model Context Protocol），意味着你可以把它接到 Claude、GPT、VS Code——任何能跑 AI 的地方。

---

## 06

写到这里，我突然想到一个问题：

**我们到底是在 "用" 工具，还是被工具 "用"？**

每天花在操作软件上的时间，是不是太多了？

gws 或许给了一个答案：

**把操作留给机器，把时间留给人。**

---

如果你想试试，命令很简单：

```bash
npm install -g @googleworkspace/cli
gws auth setup
```

去玩吧。

**你会回来感谢我的。**

---

*本文作者：一个受够了点点点的打工人*