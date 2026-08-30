# Jira CLI Command Reference

This reference covers the bundled `scripts/jira_cli.py` command groups. Endpoint availability and permissions vary by Jira Server/Data Center version, installed applications, project configuration, and permission scheme.

## Configuration

Default config path:

```text
~/.config/jira-cli/config.json
```

Example without real credentials:

```json
{
  "base_url": "https://jira.example.com/jira",
  "api_version": "2",
  "ca_bundle": "/path/to/organization-ca.pem",
  "timeout": 30
}
```

Credential precedence:

1. Command-line option.
2. Environment variable.
3. Config file.

Supported environment variables:

```text
JIRA_CLI_CONFIG
JIRA_BASE_URL
JIRA_API_VERSION
JIRA_PAT
JIRA_COOKIE
JIRA_USERNAME
JIRA_PASSWORD
JIRA_CA_BUNDLE
JIRA_TIMEOUT
```

Prefer `JIRA_PAT` or a secret manager over placing a PAT in the config file. If a config contains secrets, create it with user-only permissions such as mode `0600`.

## Discovery and diagnostics

```bash
python3 scripts/jira_cli.py server-info
python3 scripts/jira_cli.py whoami
python3 scripts/jira_cli.py projects
python3 scripts/jira_cli.py project PROJ
python3 scripts/jira_cli.py issue-types PROJ
python3 scripts/jira_cli.py create-fields PROJ Bug
python3 scripts/jira_cli.py fields --query epic
python3 scripts/jira_cli.py priorities
python3 scripts/jira_cli.py statuses
python3 scripts/jira_cli.py components PROJ
python3 scripts/jira_cli.py versions PROJ
python3 scripts/jira_cli.py permissions --project PROJ --permission CREATE_ISSUES
python3 scripts/jira_cli.py users alice
python3 scripts/jira_cli.py assignable-users alice --project PROJ
```

`create-fields` uses the Jira 8.4+ granular create metadata endpoints. The CLI falls back only for issue-type discovery on older instances; it does not use the removed global `issue/createmeta` endpoint.

## Issue query and lifecycle

```bash
python3 scripts/jira_cli.py get PROJ-123 --fields summary,status,assignee
python3 scripts/jira_cli.py search "project = PROJ ORDER BY updated DESC" --limit 100
python3 scripts/jira_cli.py create PROJ Bug "Example summary" --description "Example description"
python3 scripts/jira_cli.py create PROJ Bug "Offline payload check" --issue-type-id 12345 --dry-run
python3 scripts/jira_cli.py update PROJ-123 --summary "Updated summary"
python3 scripts/jira_cli.py transitions PROJ-123 --expand-fields
python3 scripts/jira_cli.py transition PROJ-123 "In Progress" --comment "Starting work"
python3 scripts/jira_cli.py assign PROJ-123 alice
python3 scripts/jira_cli.py assign PROJ-123 -
python3 scripts/jira_cli.py delete PROJ-123 --yes
```

Custom fields use `FIELD=JSON` or a JSON object file:

```bash
python3 scripts/jira_cli.py create PROJ Task "Example" \
  --field 'customfield_12345="value"' \
  --field 'labels=["cli","automation"]'

python3 scripts/jira_cli.py update PROJ-123 --fields-file ./fields.json
```

Always discover issue type and custom field IDs from the target instance, and verify allowed fields with `create-fields` or Jira's `editmeta` endpoint before sending them. `--issue-type-id` exists for an offline dry-run or a previously discovered ID; it is not a portable default. Never assume that a custom field name or ID is portable across instances.

## Comments

```bash
python3 scripts/jira_cli.py comments PROJ-123
python3 scripts/jira_cli.py comment-add PROJ-123 "Review completed"
python3 scripts/jira_cli.py comment-update PROJ-123 10001 "Corrected comment"
python3 scripts/jira_cli.py comment-delete PROJ-123 10001 --yes
```

## Worklogs

```bash
python3 scripts/jira_cli.py worklogs PROJ-123
python3 scripts/jira_cli.py worklog-add PROJ-123 "1h 30m" --comment "Implementation"
python3 scripts/jira_cli.py worklog-update PROJ-123 10001 "2h" --comment "Corrected time"
python3 scripts/jira_cli.py worklog-delete PROJ-123 10001 --yes
```

Estimate adjustment behavior depends on Jira configuration. For non-default behavior, use `--adjust-estimate` with `--new-estimate` or `--reduce-by` as required by the selected mode.

## Attachments

```bash
python3 scripts/jira_cli.py attachments PROJ-123
python3 scripts/jira_cli.py attachment-add PROJ-123 ./artifact.zip
python3 scripts/jira_cli.py attachment-download 10001 ./downloads/artifact.zip
python3 scripts/jira_cli.py attachment-delete 10001 --yes
```

The upload command sets `X-Atlassian-Token: nocheck` and uses multipart form data. Jira attachment enablement, project permission, and maximum upload size still apply.

## Links, watchers, and votes

```bash
python3 scripts/jira_cli.py link-types
python3 scripts/jira_cli.py link-add Blocks PROJ-123 PROJ-456
python3 scripts/jira_cli.py link-delete 10001 --yes
python3 scripts/jira_cli.py watchers PROJ-123
python3 scripts/jira_cli.py watch PROJ-123
python3 scripts/jira_cli.py watch PROJ-123 alice
python3 scripts/jira_cli.py unwatch PROJ-123
python3 scripts/jira_cli.py vote PROJ-123
python3 scripts/jira_cli.py unvote PROJ-123
```

Watcher management may require the Manage Watchers permission. Voting may be disabled globally.

## Raw REST access

Use `request` for supported Jira resources not wrapped by a dedicated command:

```bash
python3 scripts/jira_cli.py request GET /rest/api/2/issue/PROJ-123/editmeta
python3 scripts/jira_cli.py request POST /rest/api/2/issue/PROJ-123/notify --body-file ./notify.json --yes
python3 scripts/jira_cli.py request GET /rest/agile/1.0/board --query startAt=0 --query maxResults=50
```

Raw `POST`, `PUT`, and `DELETE` requests require `--yes`. Use an absolute REST path and do not pass an external URL.

## Version-specific capability groups

Platform REST API commonly covers:

- Projects, users, groups, permissions, roles, priorities, resolutions, statuses, fields, versions, and components.
- Issue create/read/update/delete, transitions, comments, worklogs, attachments, links, watchers, votes, properties, remote links, notifications, and JQL search.
- Filters, dashboards, workflow metadata, issue security, and administration endpoints when the account has permission.

Jira Software REST API under `/rest/agile/1.0` commonly covers:

- Boards and board configuration.
- Backlogs and board issues.
- Sprints and moving issues into sprints.
- Epics and rank operations, depending on Jira Software version.

Jira Service Management REST APIs commonly cover:

- Service desks, customers, organizations, requests, request participants, approvals, queues, and SLA information.

These application-specific APIs are intentionally accessed through `request` rather than hardcoded into the core CLI because their paths and payloads vary more by installed product and version.
