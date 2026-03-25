---
name: skill-security-check
description: 专门用于skill安装前的安全检查。支持多种编程语言(JavaScript/TypeScript, Python, Rust, Java, Go, C/C++, Ruby, PHP等)。在用户安装任何skill之前自动执行安全检查,检查数据外泄、凭证访问、文件系统越界、敏感文件访问、动态代码执行、权限提升、持久化机制、运行时安装、代码混淆、进程侦察、浏览器会话访问等安全风险。必须在安装任何第三方或社区skill之前使用此skill进行全面安全审查。
---

# Skill 安装前安全检查 (Multi-Language)

此skill用于在skill安装前进行全面的安全检查,确保待安装的skill不会对系统造成安全威胁。

**支持语言**: JavaScript/TypeScript, Python, Rust, Java, Go, C/C++, Ruby, PHP, Shell, PowerShell, Perl

## 何时使用

在以下情况下必须执行安全检查:
- 安装来自GitHub、npm、PyPI、Crates.io或其他源的第三方skill
- 安装社区贡献的skill
- 更新已安装的skill到新版本
- 对安全性有疑问时

## 安全检查流程

对于每个待检查的skill,按照以下清单逐项检查:

### 1. 数据外泄检查

**检查目标:** 确保skill不会将敏感数据传输到外部服务器

**检测模式 (按语言):**
- JavaScript: `fetch`, `axios`, `XMLHttpRequest`, `WebSocket`
- Python: `requests`, `urllib`, `http.client`, `aiohttp`, `httpx`
- Rust: `reqwest`, `hyper`, `ureq`, `curl`
- Java: `HttpClient`, `HttpURLConnection`, `OkHttp`, `Retrofit`
- Go: `http.Get`, `http.Post`, `net/http`
- Ruby: `Net::HTTP`, `open-uri`, `httparty`, `faraday`
- PHP: `curl_`, `file_get_contents`, `fsockopen`

**预期结果:** ✅ 无 - 无外部服务器通信(除非是skill的核心功能且已明确声明)

### 2. 凭证访问检查

**检查目标:** 确保skill安全地访问凭证和敏感配置

**检测模式 (按语言):**
- JavaScript: `process.env`, `dotenv`
- Python: `os.environ`, `os.getenv`
- Rust: `std::env`, `dotenv`
- Java: `System.getenv`, `System.getProperty`
- Go: `os.Getenv`, `os.LookupEnv`
- Ruby: `ENV[]`, `ENV.`
- PHP: `$_ENV`, `$_SERVER`, `getenv`

**预期结果:** ✅ 安全 - 仅读取配置型环境变量

### 3. 文件系统越界检查

**检查目标:** 确保skill只在预期目录内操作文件

**检测模式 (按语言):**
- JavaScript: `fs.writeFile`, `fs.readFile`, `fs.copyFile`
- Python: `open`, `pathlib`, `shutil.copy`, `shutil.move`
- Rust: `File::create`, `File::open`, `fs::write`, `std::fs`
- Java: `FileWriter`, `FileReader`, `Files.write`, `Files.read`
- Go: `os.WriteFile`, `os.ReadFile`, `os.Open`, `os.Create`
- Ruby: `File.open`, `File.write`, `FileUtils`
- PHP: `file_put_contents`, `file_get_contents`, `fopen`, `fwrite`

**预期结果:** ✅ 无 - 仅访问预期目录

### 4. 身份文件访问检查

**检查目标:** 确保skill不访问敏感的身份识别文件

**检测文件:**
- `MEMORY.md` - AI记忆文件
- `~/.ssh/*` - SSH密钥
- `~/.gitconfig` - Git配置
- `id_rsa`, `id_ed25519` - SSH私钥
- `known_hosts`, `authorized_keys`

**预期结果:** ✅ 无 - 不访问 MEMORY.md 等敏感文件

### 5. 动态代码执行检查

**检查目标:** 确保动态代码执行是可控且安全的

**检测模式 (按语言):**
- JavaScript: `eval()`, `new Function()`, `child_process`, `vm.runInNewContext`
- Python: `exec()`, `eval()`, `subprocess.call`, `os.system`, `os.popen`
- Rust: `Command::new`, `std::process::Command`, `libc::system`
- Java: `Runtime.exec`, `ProcessBuilder`, `ScriptEngine`
- Go: `exec.Command`, `os.Exec`, `syscall.Exec`
- Ruby: `eval`, `instance_eval`, `system`, ``, `Open3`
- PHP: `eval()`, `exec()`, `system()`, `shell_exec()`, `proc_open()`

**预期结果:** ✅ 受控 - 仅用于 Chrome 自动化或明确的合法用途

### 6. 权限提升检查

**检查目标:** 确保skill不尝试提升系统权限

**检测模式 (按语言):**
- Shell: `sudo`, `chmod +x`, `chmod 777`, `chown`
- Python: `os.chmod`, `os.chown`, `shutil.copymode`
- Rust: `std::os::unix::fs::PermissionsExt`, `set_permissions`
- Java: `Runtime.exec("sudo")`, `ProcessBuilder`
- Go: `os.Chmod`, `os.Chown`, `syscall.Chmod`
- Ruby: `File.chmod`, `File.chown`, `system("sudo")`
- PHP: `chmod()`, `chown()`, `exec()`, `system()`

**预期结果:** ✅ 无 - 无特权操作

### 7. 持久化机制检查

**检查目标:** 确保skill不会在后台持续运行或保持驻留

**检测模式 (按语言):**
- Shell: `daemon`, `cron`, `crontab`, `systemctl`, `nohup`
- Python: `schedule`, `APScheduler`, `threading.Timer`, `daemon=True`
- Rust: `tokio::time`, `std::thread::spawn`
- Java: `TimerTask`, `ScheduledExecutorService`, `@Scheduled`
- Go: `time.Tick`, `time.NewTicker`
- Ruby: `whenever`, `rufus-scheduler`, `Thread.new`
- 开机启动: `/etc/init.d`, `/etc/systemd`, `Library/LaunchAgents`, Windows注册表Run键

**预期结果:** ✅ 无 - 无后台驻留

### 8. 运行时安装检查

**检查目标:** 确保依赖是预先声明的,运行时不会偷偷安装

**检测模式 (按语言):**
- JavaScript: `npm install`, `yarn add`, `pnpm add`
- Python: `pip install`, `pip3 install`, `subprocess.call("pip")`, `importlib`
- Rust: `Command::new("cargo")`
- Java: `Runtime.exec("mvn")`, `ProcessBuilder("gradle")`
- Go: `exec.Command("go get")`
- Ruby: `system("gem install")`

**预期结果:** ✅ 无 - 依赖预先声明

### 9. 代码混淆检查

**检查目标:** 确保源代码清晰可读,没有恶意混淆

**检测指标:**
- 单字母变量比例 > 50%
- 超长行数 (>500字符) > 5行
- 大量长字符串 (>50字符) > 5个
- Base64/Hex编码的可疑字符串 > 10个
- 检测语言: JavaScript, TypeScript, Python, Rust, Java, Go, Ruby, PHP, C/C++

**预期结果:** ✅ 无 - 源码清晰可读

### 10. 进程侦察检查

**检查目标:** 确保skill不会扫描或枚举系统进程

**检测模式 (按语言):**
- Shell: `ps`, `tasklist`, `wmic`, `/proc/`
- Python: `psutil`, `subprocess.call("ps")`, `os.listdir("/proc")`
- Rust: `sysinfo`, `psutil`, `std::process::Command("ps")`
- Java: `ProcessHandle.allProcesses`, `ManagementFactory`, `sigar`
- Go: `exec.Command("ps")`, `process.`
- Ruby: `Sys::ProcTable`, `` `ps` ``, `system("ps")`
- PHP: `proc_open`, `shell_exec("ps")`, `exec("ps")`

**预期结果:** ✅ 无 - 无系统扫描

### 11. 浏览器会话访问检查

**检查目标:** 确保浏览器自动化使用独立的配置文件

**检测模式 (按语言):**
- JavaScript: `puppeteer`, `playwright`, `selenium`, `--user-data-dir`
- Python: `selenium`, `playwright`, `pyppeteer`, `user_data_dir`
- Rust: `headless_chrome`, `thirtyfour`, `fantoccini`
- Java: `selenium`, `ChromeDriver`, `WebDriver`, `HtmlUnitDriver`
- Go: `chromedp`, `rod`, `playwright-go`
- Ruby: `selenium-webdriver`, `watir`, `capybara`
- PHP: `facebook/webdriver`, `php-webdriver`, `panther`

**预期结果:** ✅ 受控 - 使用独立 Chrome 配置文件

## 执行检查

当用户要求检查一个skill时,按照以下步骤执行:

1. **获取skill文件:** 如果skill是本地路径,直接读取;如果是远程链接,先下载
2. **静态代码分析:** 使用grep等工具搜索风险模式(支持多语言)
3. **逐项检查:** 按照上述11项检查清单逐一验证
4. **生成报告:** 创建结构化的安全检查报告

## 输出格式

生成安全检查报告,格式如下:

```markdown
# 安全审查完成 ✅

已完成对 **xxx** skill
的全面安全审查，并生成详细报告。

## 📊 审查结果

**风险等级:** 🟢 LOW / 🟡 MEDIUM / 🔴 HIGH
**最终评级:** ✅ SAFE / ⚠️ REVIEW_NEEDED / ❌ UNSAFE
**置信度:** HIGH / MEDIUM / LOW

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

### 🚨 安全风险（如果有）

1. **数据外泄** - [具体问题描述]
2. **权限提升** - [具体问题描述]
...

---

## 📋 详细检查项

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 数据外泄 | ✅ | 无外部服务器通信 |
| 凭证访问 | ✅ | 仅读取配置型环境变量 |
| ... | ... | ... |

## 💡 建议操作

- **安全等级:** ✅ 安全 / ⚠️ 需要注意 / ❌ 高风险
- **建议:** 可以安装 / 请仔细阅读需要用户知晓的点 / 不建议安装
```

## 风险评级标准

### 风险等级

- **🟢 LOW (低风险)** - 所有检查项通过,或仅有低风险问题且已明确说明用途
- **🟡 MEDIUM (中风险)** - 存在中风险问题,或需要用户确认某些功能
- **🔴 HIGH (高风险)** - 存在数据外泄、权限提升、恶意代码等高风险问题

### 最终评级

- **✅ SAFE** - 可以安全安装
- **⚠️ REVIEW_NEEDED** - 需要用户查看"需要用户知晓的点"后决定是否安装
- **❌ UNSAFE** - 不建议安装

### 置信度

- **HIGH** - 静态分析结果明确,无歧义
- **MEDIUM** - 部分情况需要人工确认
- **LOW** - 代码复杂或存在混淆,检测结果不确定

## 报告结构说明

报告分为三个主要部分:

1. **安全优势** - 展示该skill的安全亮点,让用户了解为什么它是安全的
2. **需要用户知晓的点** - 非漏洞,但用户需要了解的功能行为(如浏览器自动化、网络请求等)
3. **安全风险** - 真正的安全问题(如果有),会列出具体问题

## 常见模式搜索

在执行检查时,使用以下grep模式进行快速扫描:

```bash
# 网络请求 (多语言)
grep -r "fetch\|axios\|requests\.\|urllib\|reqwest\|http\.client" \
  --include="*.js" --include="*.ts" --include="*.py" --include="*.rs"

# 动态代码执行 (多语言)
grep -r "eval\|exec\s*(\|subprocess\|Command::new\|Runtime\.exec" \
  --include="*.js" --include="*.ts" --include="*.py" --include="*.rs" --include="*.java" --include="*.go"

# 文件系统访问
grep -r "fs\.\|open\s*(\|File::\|FileWriter\|os\.WriteFile" \
  --include="*.js" --include="*.ts" --include="*.py" --include="*.rs" --include="*.java" --include="*.go"

# 子进程 (多语言)
grep -r "child_process\|subprocess\|Command::new\|exec\.Command\|Runtime\.exec" \
  --include="*.js" --include="*.ts" --include="*.py" --include="*.rs" --include="*.java" --include="*.go"

# 环境变量 (多语言)
grep -r "process\.env\|os\.environ\|os\.Getenv\|System\.getenv\|std::env" \
  --include="*.js" --include="*.ts" --include="*.py" --include="*.go" --include="*.java" --include="*.rs"

# 敏感文件路径
grep -r "MEMORY\.md\|\.ssh\|\.gitconfig\|id_rsa" \
  --include="*.js" --include="*.ts" --include="*.py" --include="*.rs" --include="*.java" --include="*.go"
```

## 执行步骤

1. 询问用户要检查的skill路径或来源
2. 获取skill代码文件(支持多语言项目)
3. 执行上述11项安全检查(使用语言特定的检测模式)
4. 生成完整的安全检查报告(包含安全优势和注意事项)
5. 给出明确的安装建议
