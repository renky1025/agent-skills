# Skill 安全检查工具 (Multi-Language)

一个支持多种编程语言的skill安装前安全检查工具。

## 支持的编程语言

✅ **JavaScript/TypeScript** - .js, .ts, .jsx, .tsx, .mjs, .cjs  
✅ **Python** - .py, .pyw, .pyi  
✅ **Rust** - .rs  
✅ **Java** - .java  
✅ **Go** - .go  
✅ **C/C++** - .c, .cpp, .cc, .h, .hpp  
✅ **Ruby** - .rb  
✅ **PHP** - .php  
✅ **Shell** - .sh, .bash, .zsh  
✅ **PowerShell** - .ps1  
✅ **Perl** - .pl  

## 功能

对skill进行11项安全检查:

1. ✅ **数据外泄** - 检查是否有外部服务器通信 (requests, urllib, reqwest, http.client等)
2. ✅ **凭证访问** - 检查是否安全地访问凭证 (process.env, os.environ, std::env等)
3. ✅ **文件系统越界** - 检查是否仅访问预期目录 (fs, open, File::create等)
4. ✅ **身份文件访问** - 检查是否访问 MEMORY.md 等敏感文件
5. ✅ **动态代码执行** - 检查动态代码执行风险 (eval, exec, subprocess, Command::new等)
6. ✅ **权限提升** - 检查是否有特权操作 (sudo, chmod, chown等)
7. ✅ **持久化机制** - 检查是否有后台驻留 (cron, daemon, 开机启动等)
8. ✅ **运行时安装** - 检查依赖是否预先声明 (pip install, npm install, cargo等)
9. ✅ **代码混淆** - 检查源码是否清晰可读
10. ✅ **进程侦察** - 检查是否有系统扫描 (ps, tasklist, psutil等)
11. ✅ **浏览器会话访问** - 检查是否使用独立配置文件 (puppeteer, selenium, playwright等)

## 报告格式

检查完成后会生成类似以下格式的报告：

```markdown
# 安全审查完成 ✅

已完成对 **xxx** skill
的全面安全审查，并生成详细报告。

## 📊 审查结果

**风险等级:** 🟢 LOW
**最终评级:** ✅ SAFE
**置信度:** HIGH

---

## 🔍 关键发现

### ✅ 安全优势

1. **无数据外泄** - 无外部服务器通信
2. **透明代码** - 所有源码可读，无混淆
3. **凭证安全** - 不访问敏感凭证或会话令牌
4. **作用域隔离** - 仅访问用户明确提供的文件
5. **无持久化** - 无 crontab、启动脚本或后台服务
6. **无权限提升** - 无 sudo、chmod 或 setuid 操作
7. **干净的依赖** - 所有依赖都是预先声明的

### ⚠️ 需要用户知晓的点（非漏洞）

1. **Chrome 会话持久化** - 首次运行需手动登录，会话保存在 Chrome 配置文件中
2. **网络图片下载** - 如果 Markdown 包含外部图片 URL，skill 会下载
3. **浏览器自动化** - 通过 CDP 控制 Chrome（发布功能所需）

## 💡 建议操作

- **安全等级:** ✅ 安全
- **建议:** 可以安全安装此skill
```

## 风险等级

- **🟢 LOW + ✅ SAFE** - 通过所有检查或仅有低风险问题
- **🟡 MEDIUM + ⚠️ REVIEW_NEEDED** - 存在中风险问题，需人工审查
- **🔴 HIGH + ❌ UNSAFE** - 存在严重安全问题，不建议安装

## 使用方法

### 命令行使用

```bash
node scripts/security-check.js <skill-path>
```

示例:
```bash
# 检查 Python skill
node scripts/security-check.js ~/.opencode/skills/python-skill

# 检查 Rust skill
node scripts/security-check.js ~/.opencode/skills/rust-skill

# 检查 Java skill
node scripts/security-check.js ~/.opencode/skills/java-skill
```

### 程序化使用

```javascript
const SecurityChecker = require('./scripts/security-check');

const checker = new SecurityChecker('/path/to/skill');
const results = checker.runAllChecks();
const report = checker.generateReport();

console.log(report);
```

### 作为 Skill 使用

当 Claude 检测到要安装skill时,会自动触发安全检查:

```
用户: 安装 skill-xxx
Claude: 我将先对这个skill进行安全检查...
[生成安全检查报告]
```

## 输出

检查完成后会生成一份 Markdown 格式的安全检查报告，包含:

- **审查结果** - 风险等级、最终评级、置信度
- **关键发现** - 安全优势、需要用户知晓的点、安全风险
- **详细检查项** - 11项检查的完整结果表格
- **技术详情** - 具体的问题代码位置（可展开查看）
- **建议操作** - 明确的安装建议

报告会保存到当前目录,文件名为 `security-report-<skill-name>.md`。

## 多语言支持说明

每个安全检查项都针对不同编程语言实现了特定的检测模式：

| 检查项 | JavaScript | Python | Rust | Java | Go | Ruby | PHP |
|--------|-----------|--------|------|------|-----|------|-----|
| 数据外泄 | fetch, axios | requests, urllib | reqwest, hyper | HttpClient, OkHttp | http.Get, Post | Net::HTTP, httparty | curl, file_get_contents |
| 凭证访问 | process.env | os.environ, getenv | std::env | System.getenv | os.Getenv | ENV[] | $_ENV |
| 文件操作 | fs.readFile | open, pathlib | File::open, fs::read | FileReader, Files.read | os.ReadFile, os.Open | File.open | fopen, file_get_contents |
| 动态执行 | eval, child_process | exec, subprocess | Command::new | Runtime.exec | exec.Command | eval, system | eval, exec |
| 进程扫描 | process.list | psutil, subprocess | std::process | ProcessHandle | exec.Command | Sys::ProcTable | proc_open |
| 浏览器 | puppeteer, playwright | selenium, playwright | headless_chrome, thirtyfour | selenium, ChromeDriver | chromedp, rod | selenium-webdriver, watir | facebook/webdriver |

## 注意事项

本工具使用静态代码分析,可以检测大部分常见的安全风险模式,但:

1. 不能替代完整的安全审计
2. 对于高度混淆的代码检测能力有限
3. 某些语言特定的库可能未被完全覆盖
4. 建议对重要skill进行人工代码审查

## License

MIT
