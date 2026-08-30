#!/usr/bin/env node
"use strict";

const assert = require("assert");
const { execFileSync } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");
const SecurityChecker = require("./security-check.js");

const directories = [];

function createSkill(frontmatter, source) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "skill-security-check-"));
  fs.mkdirSync(path.join(directory, "scripts"));
  fs.writeFileSync(
    path.join(directory, "SKILL.md"),
    `---\n${frontmatter}\n---\n`,
  );
  fs.writeFileSync(path.join(directory, "scripts", "client.py"), source);
  directories.push(directory);
  return directory;
}

function run() {
  try {
    const undeclared = createSkill(
      "name: undeclared-network",
      'import urllib.request\nurllib.request.urlopen("https://example.com")\n',
    );
    const undeclaredResults = new SecurityChecker(undeclared).runAllChecks();
    assert.strictEqual(undeclaredResults.checks.dataExfiltration.passed, false);
    assert.strictEqual(
      undeclaredResults.checks.dataExfiltration.declaredAccess,
      null,
    );

    const declared = createSkill(
      "name: declared-network\nnetwork_access: user-configured-origin",
      "import urllib.request\nurllib.request.urlopen(base_url)\n",
    );
    const declaredChecker = new SecurityChecker(declared);
    const declaredResults = declaredChecker.runAllChecks();
    const declaredReport = declaredChecker.generateReport();
    assert.strictEqual(declaredResults.checks.dataExfiltration.passed, true);
    assert.strictEqual(
      declaredResults.checks.dataExfiltration.declaredAccess,
      "user-configured-origin",
    );
    assert.match(declaredReport, /已声明网络访问/);
    assert.doesNotMatch(declaredReport, /最终评级:\*\* ❌ UNSAFE/);

    const readableSource = Array.from(
      { length: 30 },
      (_, index) => `value_${index} = "${"x".repeat(60)}"`,
    ).join("\n");
    const readable = createSkill("name: readable-source", readableSource);
    const readableResults = new SecurityChecker(readable).runAllChecks();
    assert.strictEqual(readableResults.checks.codeObfuscation.passed, true);

    execFileSync(process.execPath, [
      "--check",
      path.join(__dirname, "security-check.js"),
    ]);
    console.log("security-check regression tests: OK");
  } finally {
    for (const directory of directories) {
      fs.rmSync(directory, { recursive: true, force: true });
    }
  }
}

run();
