---
name: jira-server-pat-cli
description: 通用 Jira Server / Data Center REST CLI 工作流。用于通过 Personal Access Token(PAT)、Cookie 或 Basic Auth 安全地查询和管理 Jira，包括实例探测、项目与字段元数据、JQL、issue CRUD、transition、指派、评论、工时、附件、issue link、watcher、vote、权限和用户查询。适用于自托管 Jira、2FA、SSO、内部 CA、自签证书、context path 和版本差异场景；禁止硬编码实例域名、内部路径、项目 Key、用户名、凭证、自定义字段 ID 或 issue type ID。
network_access: user-configured-origin
---

# Jira Server / Data Center CLI

## 目标

为任意 Jira Server / Data Center 实例提供可迁移、可审计、无环境隐私的命令行管理方案。优先使用 Jira 官方 REST API 和运行时元数据发现，不把单个组织的配置写进 Skill。

本 Skill 附带：

- `scripts/jira_cli.py`：纯 Python 标准库 CLI。
- `references/command-reference.md`：完整命令、配置和能力边界。

## 使用边界

使用本 Skill：

- 用户要求通过脚本或 CLI 管理 Jira Server / Data Center。
- 实例使用 PAT、2FA、SSO、Cookie、Basic Auth、内部 CA 或自签证书。
- 任务涉及项目、issue、JQL、transition、评论、工时、附件、链接、watcher、权限或元数据。

不要直接套用本 Skill：

- Jira Cloud。Cloud 的 API token、accountId、REST v3 和 Atlassian Document Format 语义不同。
- 用户只要求 Jira Web 页面操作且不需要 REST/CLI。
- 目标接口属于第三方 Jira 插件，且尚未核对插件文档和版本。

## 强制隐私规则

1. 不在 Skill、脚本、示例、测试或日志中写入真实域名、IP、用户名、邮箱、项目 Key、issue Key、PAT、Cookie、自定义字段 ID、issue type ID、transition ID 或内部目录。
2. 示例只使用 `jira.example.com`、`PROJ`、`PROJ-123`、`alice`、`customfield_12345` 等明确占位值。
3. 不要求用户把 PAT 发到聊天中。优先让用户在本机通过 `JIRA_PAT`、权限为 `0600` 的配置文件或 secret manager 注入。
4. 不输出请求头、Cookie、PAT 或包含凭证的配置全文。报错和 debug 输出必须脱敏。
5. 不把实例探测结果写回 Skill。实例元数据只用于当前执行。
6. destructive 命令必须显式确认。附带 CLI 对 issue、评论、工时、附件、链接删除和所有 raw `POST`/`PUT`/`DELETE` 使用 `--yes` 门禁。

## 执行流程

### 1. 确认产品与版本

先确认目标是 Jira Server / Data Center，而不是 Jira Cloud。优先调用：

```bash
python3 scripts/jira_cli.py server-info
```

记录但不持久化：

- Jira 版本与 build number。
- Base URL 是否包含 context path，例如 `/jira`。
- 已安装 Jira Software 或 Jira Service Management 与否。
- REST API version 和目标 endpoint 是否存在。

不要把 `/login.jsp` 当成 Server/DC 的唯一识别依据。

### 2. 选择鉴权

优先级：

1. OAuth 2.0：适用于需要委托授权的正式集成，但配置成本高于个人 CLI。
2. PAT Bearer：个人脚本和 CLI 的首选。Jira Core/Software 8.14+、Jira Service Management 4.15+ 支持 PAT。
3. Basic Auth：仅在实例明确允许且安全策略接受时使用。
4. 浏览器 Cookie：临时排障兜底，不作为长期自动化凭证。

PAT 使用方式：

```bash
export JIRA_BASE_URL="https://jira.example.com/jira"
export JIRA_PAT="<secret>"
python3 scripts/jira_cli.py whoami
```

PAT 通过 `Authorization: Bearer <token>` 发送，不附加用户名。

如果 `whoami` 返回 `401` 或 `403`，不要直接断言 PAT 被 SSO 接管。依次检查：

1. PAT 是否过期、被撤销或复制不完整。
2. Base URL 和 context path 是否正确。
3. 反向代理是否保留 `Authorization` header。
4. Jira 版本是否支持 PAT，管理员是否禁用 PAT。
5. 用户权限或账号状态是否限制当前资源。

### 3. 配置 TLS

优先顺序：

1. 使用系统信任链。
2. 通过 `JIRA_CA_BUNDLE` 或 `ca_bundle` 指定组织 CA PEM 文件。
3. 仅在临时诊断时使用 `--insecure`。

不要默认关闭证书验证。`--insecure` 会失去服务端身份校验，不适合作为长期配置。

配置示例见 `references/command-reference.md`。默认配置路径是：

```text
~/.config/jira-cli/config.json
```

### 4. 先探测，再写入

至少执行：

```bash
python3 scripts/jira_cli.py whoami
python3 scripts/jira_cli.py server-info
python3 scripts/jira_cli.py projects
python3 scripts/jira_cli.py permissions --project PROJ
```

创建或更新 issue 前，动态发现：

```bash
python3 scripts/jira_cli.py issue-types PROJ
python3 scripts/jira_cli.py create-fields PROJ Bug
python3 scripts/jira_cli.py fields --query epic
python3 scripts/jira_cli.py transitions PROJ-123 --expand-fields
python3 scripts/jira_cli.py request GET /rest/api/2/issue/PROJ-123/editmeta
```

禁止使用跨实例固定回退 ID。以下数据都不是通用常量：

- issue type ID。
- custom field ID，包括 Epic Name、Epic Link、Story Points。
- transition ID。
- priority、component、version、resolution ID。
- 用户标识和项目角色 ID。

字段应优先用 ID 提交，但 ID 必须来自当前实例运行时发现。名称匹配只用于交互便利，并应处理本地化和同名歧义。

### 5. 处理版本差异

Jira 平台 REST API 的稳定根路径通常是 `/rest/api/2`。`latest` 便于人工探索，但自动化应固定已验证版本。

Create metadata 规则：

- Jira 8.4+ 使用 `/issue/createmeta/{projectIdOrKey}/issuetypes`。
- Jira 8.4+ 使用 `/issue/createmeta/{projectIdOrKey}/issuetypes/{issueTypeId}` 获取字段。
- 旧的全局 `/issue/createmeta` 在 Jira 9 被移除，且在大型实例可能产生高负载，不应作为通用实现。

用户字段兼容：

- 较老 Server/DC API 常使用 `name` 或 `username`。
- 不要把 Jira Cloud 的 `accountId` 逻辑直接复制到 Server/DC。
- 具体 payload 以目标版本 API 文档和 endpoint 返回的 schema 为准。

描述与评论格式：

- Jira Server/DC 平台 API v2 通常接收字符串或 Jira wiki renderer 内容。
- 不要默认使用 Jira Cloud REST v3 的 Atlassian Document Format。

### 6. 分页和输出

所有列表与 JQL 搜索都要处理 `startAt`、`maxResults`、`total`，不能假设一次返回全部结果。

附带 CLI 的 `search` 支持分页：

```bash
python3 scripts/jira_cli.py search \
  "project = PROJ ORDER BY updated DESC" \
  --fields key,summary,status,assignee,updated \
  --limit 200
```

默认输出 JSON，便于 `jq`、脚本和 Agent 做确定性解析。不要依赖面向人的表格文本作为程序输入。

### 7. 写操作先 dry-run 或读后写

创建、更新和 transition 支持 `--dry-run`：

```bash
python3 scripts/jira_cli.py create PROJ Bug "Example" --dry-run
python3 scripts/jira_cli.py create PROJ Bug "Offline payload" --issue-type-id 12345 --dry-run
python3 scripts/jira_cli.py update PROJ-123 --summary "Updated" --dry-run
python3 scripts/jira_cli.py transition PROJ-123 "In Progress" --dry-run
```

`--issue-type-id` 只用于离线 payload 检查或复用刚从当前实例发现的 ID，不得把该 ID 写成跨实例默认值。

执行真实写入前验证：

1. 当前用户身份。
2. 项目与 issue 是否正确。
3. 权限是否满足。
4. 字段是否在 create metadata 或 edit metadata 中。
5. transition 是否在当前 issue 的可用 transition 列表中。
6. destructive 操作是否得到用户明确确认。

## 核心能力

附带 CLI 已覆盖：

- 实例信息、当前用户、项目、issue types、字段、优先级、状态、组件、版本、权限。
- 用户搜索和可指派用户搜索。
- JQL 搜索和 issue 查询。
- issue 创建、更新、删除、指派和 transition。
- 评论增删改查。
- 工时增删改查与剩余估时调整参数。
- 附件列出、上传、下载和删除。
- issue link 创建、删除和 link type 查询。
- watcher 查询、添加和移除。
- vote 添加和移除。
- 任意 REST 路径的受控 `request` 命令。

完整示例读取 `references/command-reference.md`。

## 应补充但不宜硬编码的能力

通过 `request` 暴露以下平台或产品能力，执行前核对目标版本官方文档：

- Issue properties、remote links、notifications、bulk create、archive/restore、move、clone 等版本相关能力。
- Project roles、versions、components、filters、dashboards、workflow、screens、permission schemes 等管理能力。
- Jira Software `/rest/agile/1.0`：boards、backlog、sprints、epics、rank。
- Jira Service Management：service desks、customers、organizations、requests、participants、approvals、queues、SLA。
- 插件自定义 REST endpoints。

通用 CLI 不应假设 Jira Software 或 Jira Service Management 已安装，也不应假设当前用户有管理员权限。

## 常见失败诊断

- `400`：字段格式错误、字段不在 screen、必填字段缺失、transition payload 不满足条件。
- `401`：凭证缺失、失效，或反向代理丢弃鉴权 header。
- `403`：已认证但权限不足、XSRF header 缺失、管理员策略限制。
- `404`：资源不存在，或 Jira 为避免泄露资源存在性而隐藏无权限资源。
- `405`：当前 Jira 版本不支持该方法或 endpoint。
- `409`：并发状态变化或资源冲突，读取最新状态后再判断，不要盲重试写操作。
- `413`：附件超过实例限制。
- `415`：Content-Type 错误；附件必须用 multipart/form-data。
- `429` 或 `5xx`：只对幂等读操作做有上限的退避重试。创建、评论、工时等非幂等写操作必须先确认服务端是否已成功落库。

## 验证清单

交付或修改 Jira CLI 后必须完成：

```bash
python3 -m py_compile scripts/jira_cli.py
python3 scripts/jira_cli.py --help
python3 scripts/jira_cli.py create --help
python3 scripts/jira_cli.py request --help
```

有可用测试实例时，再做只读 smoke test：

```bash
python3 scripts/jira_cli.py server-info
python3 scripts/jira_cli.py whoami
python3 scripts/jira_cli.py projects
```

真实写入测试必须使用专用测试项目和无敏感内容的临时 issue。完成后按用户确认清理测试数据，不把真实结果写回 Skill。

## 官方依据

- Jira Data Center REST API reference：按目标 Jira 版本选择文档。
- Jira REST API examples：create、edit、comment、search 和 create metadata。
- Atlassian Personal Access Tokens 文档：PAT 支持版本、创建、Bearer 使用与撤销。
- Atlassian attachment REST 文档：multipart upload、`X-Atlassian-Token: nocheck`、权限和大小限制。
