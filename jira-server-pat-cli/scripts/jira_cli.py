#!/usr/bin/env python3
"""Dependency-free Jira Server/Data Center REST CLI."""

from __future__ import annotations

import argparse
import base64
import getpass
import json
import mimetypes
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any

DEFAULT_CONFIG = Path.home() / ".config" / "jira-cli" / "config.json"


class JiraError(RuntimeError):
    """Raised when Jira or local input rejects an operation."""


class JiraClient:
    def __init__(
        self,
        base_url: str,
        *,
        api_version: str = "2",
        pat: str | None = None,
        cookie: str | None = None,
        username: str | None = None,
        password: str | None = None,
        ca_bundle: str | None = None,
        insecure: bool = False,
        timeout: int = 30,
    ) -> None:
        if not base_url:
            raise JiraError("Jira base URL is required")
        if not (pat or cookie or (username and password)):
            raise JiraError("Authentication is required: PAT, cookie, or username/password")
        self.base_url = base_url.rstrip("/")
        self.platform_api = f"/rest/api/{api_version}"
        self.pat = pat
        self.cookie = cookie
        self.username = username
        self.password = password
        self.timeout = timeout
        self.ssl_context = ssl.create_default_context(cafile=ca_bundle)
        if insecure:
            self.ssl_context.check_hostname = False
            self.ssl_context.verify_mode = ssl.CERT_NONE

    def _auth_headers(self) -> dict[str, str]:
        if self.pat:
            return {"Authorization": f"Bearer {self.pat}"}
        if self.cookie:
            return {"Cookie": self.cookie}
        token = base64.b64encode(
            f"{self.username}:{self.password}".encode("utf-8")
        ).decode("ascii")
        return {"Authorization": f"Basic {token}"}

    def request(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, Any] | None = None,
        json_body: Any | None = None,
        data: bytes | None = None,
        headers: dict[str, str] | None = None,
        expect_json: bool = True,
    ) -> Any:
        if not path.startswith("/"):
            path = "/" + path
        url = self.base_url + path
        if query:
            encoded = urllib.parse.urlencode(
                {k: v for k, v in query.items() if v is not None}, doseq=True
            )
            url += ("&" if "?" in url else "?") + encoded

        request_headers = {"Accept": "application/json", **self._auth_headers()}
        if headers:
            request_headers.update(headers)
        if json_body is not None:
            data = json.dumps(json_body, ensure_ascii=False).encode("utf-8")
            request_headers["Content-Type"] = "application/json"

        req = urllib.request.Request(
            url, data=data, headers=request_headers, method=method.upper()
        )
        try:
            with urllib.request.urlopen(
                req, timeout=self.timeout, context=self.ssl_context
            ) as response:
                raw = response.read()
                if not raw:
                    return None
                if not expect_json:
                    return raw
                charset = response.headers.get_content_charset() or "utf-8"
                return json.loads(raw.decode(charset))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")
            try:
                payload = json.loads(detail)
                message = payload.get("errorMessages") or payload.get("errors") or payload
            except json.JSONDecodeError:
                message = detail or exc.reason
            raise JiraError(
                f"HTTP {exc.code} {method.upper()} {path}: {message}"
            ) from exc
        except urllib.error.URLError as exc:
            raise JiraError(f"Request failed for {path}: {exc.reason}") from exc

    def api(self, method: str, resource: str, **kwargs: Any) -> Any:
        return self.request(method, self.platform_api + resource, **kwargs)

    def paginate(
        self,
        resource: str,
        *,
        query: dict[str, Any] | None = None,
        item_key: str = "values",
        limit: int = 0,
        page_size: int = 50,
    ) -> list[Any]:
        items: list[Any] = []
        start_at = 0
        while True:
            page_query = dict(query or {})
            page_query.update({"startAt": start_at, "maxResults": page_size})
            payload = self.api("GET", resource, query=page_query)
            if isinstance(payload, list):
                items.extend(payload)
                break
            page_items = payload.get(item_key, [])
            items.extend(page_items)
            if limit and len(items) >= limit:
                return items[:limit]
            total = payload.get("total")
            if not page_items or (total is not None and len(items) >= total):
                break
            start_at += len(page_items)
        return items

    def search(
        self,
        jql: str,
        *,
        fields: str | None = None,
        expand: str | None = None,
        limit: int = 50,
        page_size: int = 50,
    ) -> list[Any]:
        issues: list[Any] = []
        start_at = 0
        while True:
            payload = self.api(
                "POST",
                "/search",
                json_body={
                    "jql": jql,
                    "fields": fields.split(",") if fields else None,
                    "expand": [expand] if expand else None,
                    "startAt": start_at,
                    "maxResults": page_size,
                },
            )
            page_issues = payload.get("issues", [])
            issues.extend(page_issues)
            if limit and len(issues) >= limit:
                return issues[:limit]
            total = payload.get("total")
            if not page_issues or (total is not None and len(issues) >= total):
                break
            start_at += len(page_issues)
        return issues

    def issue_types(self, project: str) -> list[dict[str, Any]]:
        try:
            payload = self.api("GET", f"/issue/createmeta/{quote(project)}/issuetypes")
            if isinstance(payload, list):
                return payload
            return payload.get("issueTypes") or payload.get("values") or []
        except JiraError as exc:
            if "HTTP 404" not in str(exc) and "HTTP 405" not in str(exc):
                raise
            project_data = self.api("GET", f"/project/{quote(project)}")
            return project_data.get("issueTypes", [])

    def resolve_issue_type(self, project: str, name_or_id: str) -> str:
        issue_types = self.issue_types(project)
        for issue_type in issue_types:
            if str(issue_type.get("id")) == name_or_id:
                return str(issue_type["id"])
            if str(issue_type.get("name", "")).casefold() == name_or_id.casefold():
                return str(issue_type["id"])
        available = [f"{item.get('name')} ({item.get('id')})" for item in issue_types]
        raise JiraError(
            f"Issue type not found: {name_or_id}. Available: {', '.join(available)}"
        )

    def create_fields(self, project: str, issue_type: str) -> dict[str, Any]:
        type_id = self.resolve_issue_type(project, issue_type)
        return self.api(
            "GET", f"/issue/createmeta/{quote(project)}/issuetypes/{quote(type_id)}"
        )

    def add_attachment(self, issue: str, file_path: Path) -> Any:
        if not file_path.is_file():
            raise JiraError(f"Attachment does not exist: {file_path}")
        boundary = "----jira-cli-" + uuid.uuid4().hex
        mime_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        body = bytearray()
        body.extend(f"--{boundary}\r\n".encode("ascii"))
        body.extend(
            (
                f'Content-Disposition: form-data; name="file"; '
                f'filename="{file_path.name}"\r\n'
            ).encode("utf-8")
        )
        body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode("ascii"))
        body.extend(file_path.read_bytes())
        body.extend(f"\r\n--{boundary}--\r\n".encode("ascii"))
        return self.api(
            "POST",
            f"/issue/{quote(issue)}/attachments",
            data=bytes(body),
            headers={
                "Content-Type": f"multipart/form-data; boundary={boundary}",
                "X-Atlassian-Token": "nocheck",
            },
        )


def quote(value: str | int) -> str:
    return urllib.parse.quote(str(value), safe="")


def load_json_file(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    try:
        with open(path, encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise JiraError(f"Cannot read JSON file {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise JiraError(f"JSON file must contain an object: {path}")
    return value


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return load_json_file(str(path))


def parse_field(values: list[str]) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    for item in values:
        if "=" not in item:
            raise JiraError(f"Field must use FIELD=JSON syntax: {item}")
        key, raw = item.split("=", 1)
        try:
            fields[key] = json.loads(raw)
        except json.JSONDecodeError:
            fields[key] = raw
    return fields


def merge_fields(args: argparse.Namespace) -> dict[str, Any]:
    fields = load_json_file(getattr(args, "fields_file", None))
    fields.update(parse_field(getattr(args, "field", []) or []))
    return fields


def config_value(
    args: argparse.Namespace,
    config: dict[str, Any],
    arg_name: str,
    env_name: str,
    config_name: str | None = None,
) -> Any:
    value = getattr(args, arg_name, None)
    if value not in (None, ""):
        return value
    env_value = os.environ.get(env_name)
    if env_value not in (None, ""):
        return env_value
    return config.get(config_name or arg_name)


def build_client(args: argparse.Namespace) -> JiraClient:
    config_path = Path(
        args.config or os.environ.get("JIRA_CLI_CONFIG") or DEFAULT_CONFIG
    ).expanduser()
    config = load_config(config_path)
    base_url = config_value(args, config, "base_url", "JIRA_BASE_URL", "base_url")
    pat = config_value(args, config, "pat", "JIRA_PAT")
    cookie = config_value(args, config, "cookie", "JIRA_COOKIE")
    username = config_value(args, config, "username", "JIRA_USERNAME")
    password = config_value(args, config, "password", "JIRA_PASSWORD")
    if username and not password and args.prompt_password:
        password = getpass.getpass("Jira password: ")
    ca_bundle = config_value(args, config, "ca_bundle", "JIRA_CA_BUNDLE")
    api_version = str(
        config_value(args, config, "api_version", "JIRA_API_VERSION") or "2"
    )
    insecure = bool(args.insecure or config.get("insecure", False))
    timeout = int(config_value(args, config, "timeout", "JIRA_TIMEOUT") or 30)
    return JiraClient(
        base_url,
        api_version=api_version,
        pat=pat,
        cookie=cookie,
        username=username,
        password=password,
        ca_bundle=ca_bundle,
        insecure=insecure,
        timeout=timeout,
    )


def emit(value: Any, *, compact: bool = False) -> None:
    if value is None:
        return
    print(
        json.dumps(
            value,
            ensure_ascii=False,
            indent=None if compact else 2,
            separators=(",", ":") if compact else None,
        )
    )


def require_confirmation(args: argparse.Namespace, action: str) -> None:
    if not getattr(args, "yes", False):
        raise JiraError(f"Refusing destructive action '{action}' without --yes")


def add_issue_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("issue", help="Issue key or ID, for example PROJ-123")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Jira Server/Data Center REST CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--config", help="JSON config path")
    parser.add_argument("--base-url", help="Jira base URL, including any context path")
    parser.add_argument("--api-version", help="Platform API version")
    parser.add_argument("--pat", help="PAT; prefer JIRA_PAT or config file")
    parser.add_argument("--cookie", help="Full Cookie header value")
    parser.add_argument("--username", help="Basic Auth username")
    parser.add_argument("--password", help="Basic Auth password; prefer environment input")
    parser.add_argument("--prompt-password", action="store_true")
    parser.add_argument("--ca-bundle", help="Trusted PEM CA bundle")
    parser.add_argument("--insecure", action="store_true", help="Disable TLS verification")
    parser.add_argument("--timeout", type=int, help="HTTP timeout in seconds")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("server-info", help="Show Jira server metadata")
    sub.add_parser("whoami", help="Show authenticated user")

    projects = sub.add_parser("projects", help="List visible projects")
    projects.add_argument("--recent", type=int)

    project = sub.add_parser("project", help="Show one project")
    project.add_argument("project")

    issue_types = sub.add_parser("issue-types", help="List project issue types")
    issue_types.add_argument("project")

    create_fields = sub.add_parser("create-fields", help="Show fields allowed at create time")
    create_fields.add_argument("project")
    create_fields.add_argument("issue_type", help="Issue type name or ID")

    fields = sub.add_parser("fields", help="List fields or search by name")
    fields.add_argument("--query")

    priorities = sub.add_parser("priorities", help="List priorities")
    priorities.add_argument("--unused", action="store_true", help=argparse.SUPPRESS)

    statuses = sub.add_parser("statuses", help="List statuses")
    statuses.add_argument("--unused", action="store_true", help=argparse.SUPPRESS)

    components = sub.add_parser("components", help="List project components")
    components.add_argument("project")

    versions = sub.add_parser("versions", help="List project versions")
    versions.add_argument("project")
    versions.add_argument("--all", action="store_true", help="Include archived versions")

    permissions = sub.add_parser("permissions", help="Show current permissions")
    permissions.add_argument("--project")
    permissions.add_argument("--issue")
    permissions.add_argument("--permission", action="append", default=[])

    user_search = sub.add_parser("users", help="Search users")
    user_search.add_argument("query")
    user_search.add_argument("--max", type=int, default=50)

    assignable = sub.add_parser(
        "assignable-users", help="Search users assignable to a project or issue"
    )
    assignable.add_argument("query")
    assignable.add_argument("--project")
    assignable.add_argument("--issue")
    assignable.add_argument("--max", type=int, default=50)

    get_issue = sub.add_parser("get", help="Get an issue")
    add_issue_argument(get_issue)
    get_issue.add_argument("--fields")
    get_issue.add_argument("--expand")

    search = sub.add_parser("search", help="Run JQL with pagination")
    search.add_argument("jql")
    search.add_argument("--fields", default="key,summary,status,assignee,updated")
    search.add_argument("--expand")
    search.add_argument("--limit", type=int, default=50, help="0 means all results")
    search.add_argument("--page-size", type=int, default=50)

    create = sub.add_parser("create", help="Create an issue")
    create.add_argument("project")
    create.add_argument("issue_type", help="Issue type name or ID")
    create.add_argument("summary")
    create.add_argument(
        "--issue-type-id",
        help="Explicit ID for offline dry-run or pre-discovered metadata",
    )
    create.add_argument("--description")
    create.add_argument("--assignee")
    create.add_argument("--priority")
    create.add_argument("--parent")
    create.add_argument("--label", action="append", default=[])
    create.add_argument("--component", action="append", default=[])
    create.add_argument("--fix-version", action="append", default=[])
    create.add_argument("--field", action="append", default=[], metavar="FIELD=JSON")
    create.add_argument("--fields-file")
    create.add_argument("--dry-run", action="store_true")

    update = sub.add_parser("update", help="Update issue fields")
    add_issue_argument(update)
    update.add_argument("--summary")
    update.add_argument("--description")
    update.add_argument("--assignee")
    update.add_argument("--priority")
    update.add_argument("--field", action="append", default=[], metavar="FIELD=JSON")
    update.add_argument("--fields-file")
    update.add_argument("--notify-users", choices=("true", "false"))
    update.add_argument("--dry-run", action="store_true")

    delete_issue = sub.add_parser("delete", help="Delete an issue")
    add_issue_argument(delete_issue)
    delete_issue.add_argument("--delete-subtasks", action="store_true")
    delete_issue.add_argument("--yes", action="store_true")

    transitions = sub.add_parser("transitions", help="List available transitions")
    add_issue_argument(transitions)
    transitions.add_argument("--expand-fields", action="store_true")

    transition = sub.add_parser("transition", help="Run a transition by name or ID")
    add_issue_argument(transition)
    transition.add_argument("target")
    transition.add_argument("--field", action="append", default=[], metavar="FIELD=JSON")
    transition.add_argument("--fields-file")
    transition.add_argument("--comment")
    transition.add_argument("--dry-run", action="store_true")

    assign = sub.add_parser("assign", help="Assign or unassign an issue")
    add_issue_argument(assign)
    assign.add_argument("assignee", help="Username, '-1' for automatic, or '-' to unassign")

    comments = sub.add_parser("comments", help="List issue comments")
    add_issue_argument(comments)
    comments.add_argument("--limit", type=int, default=0)

    comment_add = sub.add_parser("comment-add", help="Add an issue comment")
    add_issue_argument(comment_add)
    comment_add.add_argument("body")

    comment_update = sub.add_parser("comment-update", help="Update an issue comment")
    add_issue_argument(comment_update)
    comment_update.add_argument("comment_id")
    comment_update.add_argument("body")

    comment_delete = sub.add_parser("comment-delete", help="Delete an issue comment")
    add_issue_argument(comment_delete)
    comment_delete.add_argument("comment_id")
    comment_delete.add_argument("--yes", action="store_true")

    worklogs = sub.add_parser("worklogs", help="List issue worklogs")
    add_issue_argument(worklogs)

    worklog_add = sub.add_parser("worklog-add", help="Add a worklog")
    add_issue_argument(worklog_add)
    worklog_add.add_argument("time_spent", help="Jira duration, for example 1h 30m")
    worklog_add.add_argument("--comment")
    worklog_add.add_argument(
        "--started",
        help="Jira datetime, for example 2026-08-30T09:00:00.000+0800",
    )
    worklog_add.add_argument(
        "--adjust-estimate",
        choices=("auto", "new", "manual", "leave"),
        default="auto",
    )
    worklog_add.add_argument("--new-estimate")
    worklog_add.add_argument("--reduce-by")

    worklog_update = sub.add_parser("worklog-update", help="Update a worklog")
    add_issue_argument(worklog_update)
    worklog_update.add_argument("worklog_id")
    worklog_update.add_argument("time_spent")
    worklog_update.add_argument("--comment")
    worklog_update.add_argument("--started")

    worklog_delete = sub.add_parser("worklog-delete", help="Delete a worklog")
    add_issue_argument(worklog_delete)
    worklog_delete.add_argument("worklog_id")
    worklog_delete.add_argument("--yes", action="store_true")

    attachments = sub.add_parser("attachments", help="List issue attachments")
    add_issue_argument(attachments)

    attachment_add = sub.add_parser("attachment-add", help="Upload an attachment")
    add_issue_argument(attachment_add)
    attachment_add.add_argument("file")

    attachment_download = sub.add_parser("attachment-download", help="Download an attachment by ID")
    attachment_download.add_argument("attachment_id")
    attachment_download.add_argument("output")

    attachment_delete = sub.add_parser("attachment-delete", help="Delete an attachment")
    attachment_delete.add_argument("attachment_id")
    attachment_delete.add_argument("--yes", action="store_true")

    link_types = sub.add_parser("link-types", help="List issue link types")
    link_types.add_argument("--unused", action="store_true", help=argparse.SUPPRESS)

    link_add = sub.add_parser("link-add", help="Link two issues")
    link_add.add_argument("link_type")
    link_add.add_argument("inward_issue")
    link_add.add_argument("outward_issue")
    link_add.add_argument("--comment")

    link_delete = sub.add_parser("link-delete", help="Delete an issue link by ID")
    link_delete.add_argument("link_id")
    link_delete.add_argument("--yes", action="store_true")

    watchers = sub.add_parser("watchers", help="List issue watchers")
    add_issue_argument(watchers)

    watch = sub.add_parser("watch", help="Add a watcher; omit username for current user")
    add_issue_argument(watch)
    watch.add_argument("username", nargs="?")

    unwatch = sub.add_parser("unwatch", help="Remove a watcher; omit username for current user")
    add_issue_argument(unwatch)
    unwatch.add_argument("username", nargs="?")

    vote = sub.add_parser("vote", help="Add current user's vote")
    add_issue_argument(vote)

    unvote = sub.add_parser("unvote", help="Remove current user's vote")
    add_issue_argument(unvote)

    raw = sub.add_parser("request", help="Call an arbitrary Jira REST resource")
    raw.add_argument("method", choices=("GET", "POST", "PUT", "DELETE"))
    raw.add_argument("path", help="Absolute REST path, for example /rest/api/2/myself")
    raw.add_argument("--query", action="append", default=[], metavar="KEY=VALUE")
    raw.add_argument("--body-file")
    raw.add_argument("--yes", action="store_true", help="Required for POST, PUT, and DELETE")

    return parser


def parse_query(values: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise JiraError(f"Query must use KEY=VALUE syntax: {value}")
        key, item = value.split("=", 1)
        result[key] = item
    return result


def resolve_transition(client: JiraClient, issue: str, target: str) -> dict[str, Any]:
    payload = client.api("GET", f"/issue/{quote(issue)}/transitions")
    transitions = payload.get("transitions", [])
    for transition in transitions:
        if str(transition.get("id")) == target:
            return transition
        if str(transition.get("name", "")).casefold() == target.casefold():
            return transition
    available = [f"{item.get('name')} ({item.get('id')})" for item in transitions]
    raise JiraError(f"Transition not found: {target}. Available: {', '.join(available)}")


def run(args: argparse.Namespace, client: JiraClient) -> Any:
    command = args.command
    if command == "server-info":
        return client.api("GET", "/serverInfo")
    if command == "whoami":
        return client.api("GET", "/myself")
    if command == "projects":
        query = {"recent": args.recent} if args.recent is not None else None
        return client.api("GET", "/project", query=query)
    if command == "project":
        return client.api("GET", f"/project/{quote(args.project)}")
    if command == "issue-types":
        return client.issue_types(args.project)
    if command == "create-fields":
        return client.create_fields(args.project, args.issue_type)
    if command == "fields":
        fields = client.api("GET", "/field")
        if args.query:
            needle = args.query.casefold()
            fields = [
                field
                for field in fields
                if needle in str(field.get("name", "")).casefold()
                or needle in str(field.get("id", "")).casefold()
            ]
        return fields
    if command == "priorities":
        return client.api("GET", "/priority")
    if command == "statuses":
        return client.api("GET", "/status")
    if command == "components":
        return client.api("GET", f"/project/{quote(args.project)}/components")
    if command == "versions":
        versions = client.api("GET", f"/project/{quote(args.project)}/versions")
        if args.all:
            return versions
        return [version for version in versions if not version.get("archived", False)]
    if command == "permissions":
        query: dict[str, Any] = {}
        if args.project:
            query["projectKey"] = args.project
        if args.issue:
            query["issueKey"] = args.issue
        if args.permission:
            query["permissions"] = ",".join(args.permission)
        return client.api("GET", "/mypermissions", query=query)
    if command == "users":
        return client.api(
            "GET", "/user/picker", query={"query": args.query, "maxResults": args.max}
        )
    if command == "assignable-users":
        query = {"username": args.query, "maxResults": args.max}
        if args.project:
            query["project"] = args.project
        if args.issue:
            query["issueKey"] = args.issue
        return client.api("GET", "/user/assignable/search", query=query)
    if command == "get":
        query = {"fields": args.fields, "expand": args.expand}
        return client.api("GET", f"/issue/{quote(args.issue)}", query=query)
    if command == "search":
        return client.search(
            args.jql,
            fields=args.fields,
            expand=args.expand,
            limit=args.limit,
            page_size=args.page_size,
        )
    if command == "create":
        fields = merge_fields(args)
        issue_type_id = args.issue_type_id or client.resolve_issue_type(
            args.project, args.issue_type
        )
        fields.update(
            {
                "project": {"key": args.project},
                "issuetype": {"id": issue_type_id},
                "summary": args.summary,
            }
        )
        optional = {
            "description": args.description,
            "assignee": {"name": args.assignee} if args.assignee else None,
            "priority": {"name": args.priority} if args.priority else None,
            "parent": {"key": args.parent} if args.parent else None,
            "labels": args.label or None,
            "components": [{"name": item} for item in args.component] or None,
            "fixVersions": [{"name": item} for item in args.fix_version] or None,
        }
        fields.update({key: value for key, value in optional.items() if value is not None})
        payload = {"fields": fields}
        return payload if args.dry_run else client.api("POST", "/issue", json_body=payload)
    if command == "update":
        fields = merge_fields(args)
        optional = {
            "summary": args.summary,
            "description": args.description,
            "assignee": {"name": args.assignee} if args.assignee else None,
            "priority": {"name": args.priority} if args.priority else None,
        }
        fields.update({key: value for key, value in optional.items() if value is not None})
        if not fields:
            raise JiraError("No update fields were provided")
        payload = {"fields": fields}
        if args.dry_run:
            return payload
        query = {"notifyUsers": args.notify_users}
        client.api("PUT", f"/issue/{quote(args.issue)}", query=query, json_body=payload)
        return {"updated": args.issue}
    if command == "delete":
        require_confirmation(args, f"delete issue {args.issue}")
        client.api(
            "DELETE",
            f"/issue/{quote(args.issue)}",
            query={"deleteSubtasks": str(args.delete_subtasks).lower()},
        )
        return {"deleted": args.issue}
    if command == "transitions":
        expand = "transitions.fields" if args.expand_fields else None
        return client.api(
            "GET", f"/issue/{quote(args.issue)}/transitions", query={"expand": expand}
        )
    if command == "transition":
        transition = resolve_transition(client, args.issue, args.target)
        fields = merge_fields(args)
        payload: dict[str, Any] = {"transition": {"id": transition["id"]}}
        if fields:
            payload["fields"] = fields
        if args.comment:
            payload["update"] = {"comment": [{"add": {"body": args.comment}}]}
        if args.dry_run:
            return payload
        client.api("POST", f"/issue/{quote(args.issue)}/transitions", json_body=payload)
        return {"transitioned": args.issue, "transition": transition["name"]}
    if command == "assign":
        name = None if args.assignee == "-" else args.assignee
        client.api("PUT", f"/issue/{quote(args.issue)}/assignee", json_body={"name": name})
        return {"assigned": args.issue, "assignee": name}
    if command == "comments":
        return client.paginate(
            f"/issue/{quote(args.issue)}/comment",
            item_key="comments",
            limit=args.limit,
        )
    if command == "comment-add":
        return client.api(
            "POST",
            f"/issue/{quote(args.issue)}/comment",
            json_body={"body": args.body},
        )
    if command == "comment-update":
        return client.api(
            "PUT",
            f"/issue/{quote(args.issue)}/comment/{quote(args.comment_id)}",
            json_body={"body": args.body},
        )
    if command == "comment-delete":
        require_confirmation(args, f"delete comment {args.comment_id}")
        client.api("DELETE", f"/issue/{quote(args.issue)}/comment/{quote(args.comment_id)}")
        return {"deleted_comment": args.comment_id}
    if command == "worklogs":
        return client.api("GET", f"/issue/{quote(args.issue)}/worklog")
    if command == "worklog-add":
        payload = {"timeSpent": args.time_spent}
        if args.comment:
            payload["comment"] = args.comment
        if args.started:
            payload["started"] = args.started
        query = {
            "adjustEstimate": args.adjust_estimate,
            "newEstimate": args.new_estimate,
            "reduceBy": args.reduce_by,
        }
        return client.api(
            "POST",
            f"/issue/{quote(args.issue)}/worklog",
            query=query,
            json_body=payload,
        )
    if command == "worklog-update":
        payload = {"timeSpent": args.time_spent}
        if args.comment:
            payload["comment"] = args.comment
        if args.started:
            payload["started"] = args.started
        return client.api(
            "PUT",
            f"/issue/{quote(args.issue)}/worklog/{quote(args.worklog_id)}",
            json_body=payload,
        )
    if command == "worklog-delete":
        require_confirmation(args, f"delete worklog {args.worklog_id}")
        client.api("DELETE", f"/issue/{quote(args.issue)}/worklog/{quote(args.worklog_id)}")
        return {"deleted_worklog": args.worklog_id}
    if command == "attachments":
        issue = client.api("GET", f"/issue/{quote(args.issue)}", query={"fields": "attachment"})
        return issue.get("fields", {}).get("attachment", [])
    if command == "attachment-add":
        return client.add_attachment(args.issue, Path(args.file).expanduser())
    if command == "attachment-download":
        metadata = client.api("GET", f"/attachment/{quote(args.attachment_id)}")
        content_url = metadata.get("content")
        if not content_url:
            raise JiraError("Attachment metadata does not include a content URL")
        parsed = urllib.parse.urlparse(content_url)
        if parsed.netloc and not content_url.startswith(client.base_url):
            raise JiraError("Refusing attachment download from a different host")
        if content_url.startswith(client.base_url):
            path = content_url[len(client.base_url):]
        else:
            path = content_url
        data = client.request("GET", path, expect_json=False)
        output = Path(args.output).expanduser()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(data)
        return {"downloaded": str(output), "bytes": len(data)}
    if command == "attachment-delete":
        require_confirmation(args, f"delete attachment {args.attachment_id}")
        client.api("DELETE", f"/attachment/{quote(args.attachment_id)}")
        return {"deleted_attachment": args.attachment_id}
    if command == "link-types":
        return client.api("GET", "/issueLinkType")
    if command == "link-add":
        payload: dict[str, Any] = {
            "type": {"name": args.link_type},
            "inwardIssue": {"key": args.inward_issue},
            "outwardIssue": {"key": args.outward_issue},
        }
        if args.comment:
            payload["comment"] = {"body": args.comment}
        client.api("POST", "/issueLink", json_body=payload)
        return {"linked": [args.inward_issue, args.outward_issue], "type": args.link_type}
    if command == "link-delete":
        require_confirmation(args, f"delete issue link {args.link_id}")
        client.api("DELETE", f"/issueLink/{quote(args.link_id)}")
        return {"deleted_link": args.link_id}
    if command == "watchers":
        return client.api("GET", f"/issue/{quote(args.issue)}/watchers")
    if command == "watch":
        username = args.username
        if not username:
            username = client.api("GET", "/myself").get("name")
        if not username:
            raise JiraError("Current Jira username is unavailable; provide username explicitly")
        return client.api(
            "POST",
            f"/issue/{quote(args.issue)}/watchers",
            data=json.dumps(username).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
    if command == "unwatch":
        username = args.username
        if not username:
            username = client.api("GET", "/myself").get("name")
        if not username:
            raise JiraError("Current Jira username is unavailable; provide username explicitly")
        client.api("DELETE", f"/issue/{quote(args.issue)}/watchers", query={"username": username})
        return {"unwatched": args.issue, "username": username}
    if command == "vote":
        client.api("POST", f"/issue/{quote(args.issue)}/votes", data=b"")
        return {"voted": args.issue}
    if command == "unvote":
        client.api("DELETE", f"/issue/{quote(args.issue)}/votes")
        return {"unvoted": args.issue}
    if command == "request":
        if args.method != "GET":
            require_confirmation(args, f"{args.method} {args.path}")
        body = load_json_file(args.body_file) if args.body_file else None
        return client.request(args.method, args.path, query=parse_query(args.query), json_body=body)
    raise JiraError(f"Unsupported command: {command}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        client = build_client(args)
        emit(run(args, client), compact=args.compact)
        return 0
    except JiraError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("error: interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
