#!/usr/bin/env python3
"""Offline contract tests for jira_cli.py."""

from __future__ import annotations

import argparse
import importlib.util
import json
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

MODULE_PATH = Path(__file__).with_name("jira_cli.py")
SPEC = importlib.util.spec_from_file_location("jira_cli", MODULE_PATH)
assert SPEC and SPEC.loader
jira_cli = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(jira_cli)


class JiraHandler(BaseHTTPRequestHandler):
    calls: list[dict[str, Any]] = []

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _body(self) -> Any:
        length = int(self.headers.get("Content-Length", "0"))
        if not length:
            return None
        raw = self.rfile.read(length)
        if "application/json" in self.headers.get("Content-Type", ""):
            return json.loads(raw.decode("utf-8"))
        return raw

    def _send(self, payload: Any = None, status: int = 200) -> None:
        self.send_response(status)
        if payload is None:
            self.end_headers()
            return
        raw = json.dumps(payload).encode("utf-8")
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        self.calls.append({"method": "GET", "path": self.path})
        if self.path == "/rest/api/2/myself":
            self._send({"name": "alice"})
            return
        if self.path == "/rest/api/2/issue/createmeta/PROJ/issuetypes":
            self._send([{"id": "7", "name": "Bug"}])
            return
        if self.path == "/rest/api/2/project/PROJ/versions":
            self._send([
                {"id": "1", "name": "Open", "archived": False},
                {"id": "2", "name": "Old", "archived": True},
            ])
            return
        if self.path == "/rest/api/2/issue/PROJ-1/transitions":
            self._send({"transitions": [{"id": "11", "name": "Start"}]})
            return
        self._send({"errorMessages": ["not found"]}, status=404)

    def do_POST(self) -> None:
        body = self._body()
        self.calls.append({"method": "POST", "path": self.path, "body": body})
        if self.path == "/rest/api/2/search":
            start = body["startAt"]
            pages = {
                0: {"issues": [{"key": "PROJ-1"}], "total": 3},
                1: {"issues": [{"key": "PROJ-2"}], "total": 3},
                2: {"issues": [{"key": "PROJ-3"}], "total": 3},
            }
            self._send(pages[start])
            return
        if self.path == "/rest/api/2/issue":
            self._send({"id": "100", "key": "PROJ-1"}, status=201)
            return
        if self.path == "/rest/api/2/issue/PROJ-1/transitions":
            self._send(None, status=204)
            return
        if self.path == "/rest/api/2/issue/PROJ-1/watchers":
            self._send(None, status=204)
            return
        self._send({"errorMessages": ["not found"]}, status=404)


class JiraCliContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        JiraHandler.calls = []
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), JiraHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.start()
        cls.client = jira_cli.JiraClient(
            f"http://127.0.0.1:{cls.server.server_port}", pat="test-token"
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.thread.join()
        cls.server.server_close()

    def test_issue_type_array_response_and_create(self) -> None:
        result = jira_cli.run(
            argparse.Namespace(
                command="create",
                project="PROJ",
                issue_type="Bug",
                summary="Example",
                issue_type_id=None,
                description=None,
                assignee=None,
                priority=None,
                parent=None,
                label=[],
                component=[],
                fix_version=[],
                field=[],
                fields_file=None,
                dry_run=False,
            ),
            self.client,
        )
        self.assertEqual(result["key"], "PROJ-1")
        create_call = next(
            item for item in reversed(JiraHandler.calls) if item["path"] == "/rest/api/2/issue"
        )
        self.assertEqual(create_call["body"]["fields"]["issuetype"]["id"], "7")

    def test_search_uses_post_and_paginates(self) -> None:
        issues = self.client.search("project = PROJ", limit=0, page_size=1)
        self.assertEqual([item["key"] for item in issues], ["PROJ-1", "PROJ-2", "PROJ-3"])
        search_calls = [item for item in JiraHandler.calls if item["path"] == "/rest/api/2/search"]
        self.assertEqual([item["method"] for item in search_calls[-3:]], ["POST", "POST", "POST"])

    def test_versions_filter_archived(self) -> None:
        result = jira_cli.run(
            argparse.Namespace(command="versions", project="PROJ", all=False),
            self.client,
        )
        self.assertEqual([item["name"] for item in result], ["Open"])

    def test_transition_resolves_name(self) -> None:
        result = jira_cli.run(
            argparse.Namespace(
                command="transition",
                issue="PROJ-1",
                target="Start",
                field=[],
                fields_file=None,
                comment="Begin",
                dry_run=False,
            ),
            self.client,
        )
        self.assertEqual(result["transition"], "Start")

    def test_watch_resolves_current_username(self) -> None:
        result = jira_cli.run(
            argparse.Namespace(command="watch", issue="PROJ-1", username=None),
            self.client,
        )
        self.assertIsNone(result)
        watch_call = next(
            item
            for item in reversed(JiraHandler.calls)
            if item["path"] == "/rest/api/2/issue/PROJ-1/watchers"
        )
        self.assertEqual(watch_call["body"], "alice")

    def test_destructive_action_requires_yes(self) -> None:
        with self.assertRaises(jira_cli.JiraError):
            jira_cli.require_confirmation(
                argparse.Namespace(yes=False), "delete example"
            )

    def test_raw_write_requires_yes(self) -> None:
        with self.assertRaises(jira_cli.JiraError):
            jira_cli.run(
                argparse.Namespace(
                    command="request",
                    method="POST",
                    path="/rest/api/2/example",
                    body_file=None,
                    query=[],
                    yes=False,
                ),
                self.client,
            )

    def test_config_does_not_require_secret_in_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text('{"base_url":"https://jira.example.com"}', encoding="utf-8")
            self.assertEqual(jira_cli.load_config(path)["base_url"], "https://jira.example.com")


if __name__ == "__main__":
    unittest.main()
