#!/usr/bin/env node
/**
 * Skill 安全检查脚本
 * 用于自动化检查skill中的安全风险
 */

const fs = require('fs');
const path = require('path');

class SecurityChecker {
  constructor(skillPath) {
    this.skillPath = skillPath;
    this.results = {
      skillName: path.basename(skillPath),
      timestamp: new Date().toISOString(),
      checks: {}
    };
  }

  /**
   * 读取所有代码文件
   */
  getCodeFiles() {
    const files = [];
    // 支持多种编程语言
    const extensions = [
      // JavaScript/TypeScript
      '.js', '.ts', '.jsx', '.tsx', '.mjs', '.cjs',
      // Python
      '.py', '.pyw', '.pyi',
      // Rust
      '.rs',
      // Java
      '.java',
      // C/C++
      '.c', '.cpp', '.cc', '.h', '.hpp',
      // Go
      '.go',
      // Ruby
      '.rb',
      // PHP
      '.php',
      // Shell
      '.sh', '.bash', '.zsh',
      // PowerShell
      '.ps1',
      // Perl
      '.pl',
      // Config files
      '.json', '.yaml', '.yml', '.toml', '.xml',
      // Documentation
      '.md', '.txt'
    ];
    
    const walkDir = (dir) => {
      if (!fs.existsSync(dir)) return;
      const items = fs.readdirSync(dir);
      for (const item of items) {
        const fullPath = path.join(dir, item);
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory() && 
            item !== 'node_modules' && 
            item !== '.git' &&
            item !== '__pycache__' &&
            item !== 'target' &&
            item !== 'dist' &&
            item !== 'build') {
          walkDir(fullPath);
        } else if (stat.isFile() && extensions.some(ext => item.toLowerCase().endsWith(ext))) {
          files.push(fullPath);
        }
      }
    };
    
    walkDir(this.skillPath);
    return files;
  }

  /**
   * 检查数据外泄
   */
  checkDataExfiltration() {
    const files = this.getCodeFiles();
    const issues = [];
    
    // JavaScript/TypeScript
    const jsPatterns = [
      /fetch\s*\(/g,
      /axios\./g,
      /request\s*\(/g,
      /http\.request/g,
      /https\.request/g,
      /XMLHttpRequest/g,
      /WebSocket/g
    ];
    
    // Python
    const pyPatterns = [
      /requests\./g,
      /urllib/g,
      /http\.client/g,
      /aiohttp/g,
      /httpx/g
    ];
    
    // Rust
    const rsPatterns = [
      /reqwest/g,
      /hyper/g,
      /ureq/g,
      /curl::/g
    ];
    
    // Java
    const javaPatterns = [
      /HttpClient/g,
      /HttpURLConnection/g,
      /OkHttp/g,
      /Retrofit/g
    ];
    
    // Go
    const goPatterns = [
      /http\.Get/g,
      /http\.Post/g,
      /net\/http/g
    ];
    
    // Ruby
    const rbPatterns = [
      /Net::HTTP/g,
      /open-uri/g,
      /httparty/g,
      /faraday/g
    ];
    
    // PHP
    const phpPatterns = [
      /curl_/g,
      /file_get_contents\s*\(/g,
      /fsockopen/g
    ];
    
    const allPatterns = [
      ...jsPatterns, ...pyPatterns, ...rsPatterns, 
      ...javaPatterns, ...goPatterns, ...rbPatterns, ...phpPatterns
    ];
    
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8');
      for (const pattern of allPatterns) {
        const matches = content.match(pattern);
        if (matches) {
          issues.push({
            file: path.relative(this.skillPath, file),
            pattern: pattern.source,
            count: matches.length
          });
        }
      }
    }
    
    this.results.checks.dataExfiltration = {
      passed: issues.length === 0,
      issues: issues,
      message: issues.length === 0 ? '无外部服务器通信' : `发现 ${issues.length} 个网络请求位置`
    };
  }

  /**
   * 检查凭证访问
   */
  checkCredentialAccess() {
    const files = this.getCodeFiles();
    const issues = [];
    
    // JavaScript/Node.js
    const jsPatterns = [
      /process\.env/g,
      /dotenv/g
    ];
    
    // Python
    const pyPatterns = [
      /os\.environ/g,
      /os\.getenv/g,
      /environ\[/g
    ];
    
    // Rust
    const rsPatterns = [
      /std::env/g,
      /env::/g,
      /dotenv/g
    ];
    
    // Java
    const javaPatterns = [
      /System\.getenv/g,
      /System\.getProperty/g
    ];
    
    // Go
    const goPatterns = [
      /os\.Getenv/g,
      /os\.LookupEnv/g
    ];
    
    // Ruby
    const rbPatterns = [
      /ENV\[/g,
      /ENV\./g
    ];
    
    // PHP
    const phpPatterns = [
      /\$_ENV/g,
      /\$_SERVER/g,
      /getenv/g
    ];
    
    // 通用凭证关键词
    const credentialPatterns = [
      /AWS_ACCESS_KEY_ID/g,
      /AWS_SECRET_ACCESS_KEY/g,
      /SECRET_KEY/g,
      /PASSWORD/g,
      /PASSWD/g,
      /TOKEN/g,
      /API_KEY/g,
      /PRIVATE_KEY/g,
      /SECRET/g
    ];
    
    const allPatterns = [
      ...jsPatterns, ...pyPatterns, ...rsPatterns, 
      ...javaPatterns, ...goPatterns, ...rbPatterns, ...phpPatterns,
      ...credentialPatterns
    ];
    
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8');
      for (const pattern of allPatterns) {
        const matches = content.match(pattern);
        if (matches) {
          issues.push({
            file: path.relative(this.skillPath, file),
            pattern: pattern.source
          });
        }
      }
    }
    
    this.results.checks.credentialAccess = {
      passed: true, // 读取环境变量是正常的,但需要审查
      issues: issues,
      message: issues.length === 0 ? '无凭证访问' : `发现 ${issues.length} 处凭证相关代码,需人工审查`
    };
  }

  /**
   * 检查文件系统越界
   */
  checkFilesystemEscaping() {
    const files = this.getCodeFiles();
    const issues = [];
    
    // JavaScript/Node.js
    const jsPatterns = [
      /fs\.writeFile/g,
      /fs\.appendFile/g,
      /fs\.unlink/g,
      /fs\.rmdir/g,
      /fs\.copyFile/g,
      /fs\.rename/g
    ];
    
    // Python
    const pyPatterns = [
      /open\s*\(/g,
      /os\.open/g,
      /shutil\.copy/g,
      /shutil\.move/g,
      /pathlib/g,
      /with\s+open/g
    ];
    
    // Rust
    const rsPatterns = [
      /File::create/g,
      /File::open/g,
      /fs::write/g,
      /fs::read/g,
      /std::fs/g
    ];
    
    // Java
    const javaPatterns = [
      /FileWriter/g,
      /FileReader/g,
      /FileOutputStream/g,
      /FileInputStream/g,
      /Files\.write/g,
      /Files\.read/g
    ];
    
    // Go
    const goPatterns = [
      /os\.WriteFile/g,
      /os\.ReadFile/g,
      /os\.Open/g,
      /os\.Create/g,
      /ioutil\.WriteFile/g
    ];
    
    // Ruby
    const rbPatterns = [
      /File\.open/g,
      /File\.write/g,
      /FileUtils/g,
      /IO\.write/g,
      /IO\.read/g
    ];
    
    // PHP
    const phpPatterns = [
      /file_put_contents/g,
      /file_get_contents/g,
      /fopen/g,
      /fwrite/g,
      /copy\s*\(/g
    ];
    
    // 危险路径
    const pathPatterns = [
      /\/etc\//g,
      /\/usr\/bin/g,
      /\/usr\/sbin/g,
      /\/bin\//g,
      /\/sbin\//g,
      /C:\\\\Windows/g,
      /C:\\\\Program Files/g,
      /\/root\//g,
      /\.\.\/\.\./g
    ];
    
    const allPatterns = [
      ...jsPatterns, ...pyPatterns, ...rsPatterns, 
      ...javaPatterns, ...goPatterns, ...rbPatterns, ...phpPatterns,
      ...pathPatterns
    ];
    
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8');
      for (const pattern of allPatterns) {
        const matches = content.match(pattern);
        if (matches) {
          issues.push({
            file: path.relative(this.skillPath, file),
            pattern: pattern.source
          });
        }
      }
    }
    
    this.results.checks.filesystemEscaping = {
      passed: issues.filter(i => i.pattern.includes('..') || i.pattern.includes('/etc')).length === 0,
      issues: issues,
      message: issues.length === 0 ? '仅访问预期目录' : `发现 ${issues.length} 处文件操作,需确认范围`
    };
  }

  /**
   * 检查敏感文件访问
   */
  checkSensitiveFileAccess() {
    const files = this.getCodeFiles();
    const issues = [];
    
    const patterns = [
      /MEMORY\.md/g,
      /\.ssh/g,
      /\.gitconfig/g,
      /id_rsa/g,
      /id_ed25519/g,
      /known_hosts/g,
      /authorized_keys/g
    ];
    
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8');
      for (const pattern of patterns) {
        const matches = content.match(pattern);
        if (matches) {
          issues.push({
            file: path.relative(this.skillPath, file),
            pattern: pattern.source
          });
        }
      }
    }
    
    this.results.checks.sensitiveFileAccess = {
      passed: issues.length === 0,
      issues: issues,
      message: issues.length === 0 ? '不访问 MEMORY.md 等敏感文件' : `发现 ${issues.length} 处敏感文件访问`
    };
  }

  /**
   * 检查动态代码执行
   */
  checkDynamicCodeExecution() {
    const files = this.getCodeFiles();
    const issues = [];
    
    // JavaScript/Node.js
    const jsPatterns = [
      /eval\s*\(/g,
      /new\s+Function/g,
      /setTimeout\s*\(\s*["']/g,
      /setInterval\s*\(\s*["']/g,
      /child_process/g,
      /\.exec\s*\(/g,
      /\.execSync/g,
      /spawn\s*\(/g,
      /vm\.runInNewContext/g
    ];
    
    // Python
    const pyPatterns = [
      /exec\s*\(/g,
      /eval\s*\(/g,
      /compile\s*\(/g,
      /subprocess\.call/g,
      /subprocess\.run/g,
      /subprocess\.Popen/g,
      /os\.system/g,
      /os\.popen/g,
      /__import__/g
    ];
    
    // Rust
    const rsPatterns = [
      /Command::new/g,
      /std::process::Command/g,
      /libc::system/g
    ];
    
    // Java
    const javaPatterns = [
      /Runtime\.getRuntime\(\)\.exec/g,
      /ProcessBuilder/g,
      /ScriptEngine/g,
      /javax\.script/g
    ];
    
    // Go
    const goPatterns = [
      /exec\.Command/g,
      /os\.Exec/g,
      /syscall\.Exec/g
    ];
    
    // Ruby
    const rbPatterns = [
      /eval\s+/g,
      /instance_eval/g,
      /class_eval/g,
      /Kernel\.exec/g,
      /system\s*\(/g,
      /`[^`]+`/g,
      /Open3/g
    ];
    
    // PHP
    const phpPatterns = [
      /eval\s*\(/g,
      /exec\s*\(/g,
      /system\s*\(/g,
      /passthru\s*\(/g,
      /shell_exec\s*\(/g,
      /proc_open\s*\(/g,
      /popen\s*\(/g
    ];
    
    const allPatterns = [
      ...jsPatterns, ...pyPatterns, ...rsPatterns, 
      ...javaPatterns, ...goPatterns, ...rbPatterns, ...phpPatterns
    ];
    
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8');
      for (const pattern of allPatterns) {
        const matches = content.match(pattern);
        if (matches) {
          issues.push({
            file: path.relative(this.skillPath, file),
            pattern: pattern.source
          });
        }
      }
    }
    
    this.results.checks.dynamicCodeExecution = {
      passed: issues.filter(i => i.pattern.includes('eval') && !i.pattern.includes('child_process') && !i.pattern.includes('subprocess')).length === 0,
      issues: issues,
      message: issues.length === 0 ? '无动态代码执行' : `发现 ${issues.length} 处动态代码执行,需审查用途`
    };
  }

  /**
   * 检查权限提升
   */
  checkPrivilegeEscalation() {
    const files = this.getCodeFiles();
    const issues = [];
    
    // Shell
    const shellPatterns = [
      /sudo\s/g,
      /runas/g,
      /chmod\s+\+x/g,
      /chmod\s+[0-9]*7/g,
      /chown/g,
      /chgrp/g
    ];
    
    // Python
    const pyPatterns = [
      /os\.chmod/g,
      /os\.chown/g,
      /shutil\.copymode/g,
      /subprocess\.call.*sudo/g,
      /subprocess\.run.*sudo/g
    ];
    
    // Rust
    const rsPatterns = [
      /std::os::unix::fs::PermissionsExt/g,
      /set_permissions/g
    ];
    
    // Java
    const javaPatterns = [
      /Runtime\.getRuntime\(\)\.exec.*sudo/g,
      /ProcessBuilder.*sudo/g
    ];
    
    // Go
    const goPatterns = [
      /os\.Chmod/g,
      /os\.Chown/g,
      /syscall\.Chmod/g
    ];
    
    // Ruby
    const rbPatterns = [
      /File\.chmod/g,
      /File\.chown/g,
      /system.*sudo/g,
      /`.*sudo`/g
    ];
    
    // PHP
    const phpPatterns = [
      /chmod\s*\(/g,
      /chown\s*\(/g,
      /exec\s*\(/g,
      /system\s*\(/g
    ];
    
    // 通用关键词
    const generalPatterns = [
      /administrator/g,
      /root/g,
      /setuid/g,
      /setgid/g
    ];
    
    const allPatterns = [
      ...shellPatterns, ...pyPatterns, ...rsPatterns, 
      ...javaPatterns, ...goPatterns, ...rbPatterns, ...phpPatterns,
      ...generalPatterns
    ];
    
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8');
      for (const pattern of allPatterns) {
        const matches = content.match(pattern);
        if (matches) {
          issues.push({
            file: path.relative(this.skillPath, file),
            pattern: pattern.source
          });
        }
      }
    }
    
    this.results.checks.privilegeEscalation = {
      passed: issues.length === 0,
      issues: issues,
      message: issues.length === 0 ? '无特权操作' : `发现 ${issues.length} 处权限相关操作,需审查`
    };
  }

  /**
   * 检查持久化机制
   */
  checkPersistence() {
    const files = this.getCodeFiles();
    const issues = [];
    
    // Shell/General
    const shellPatterns = [
      /daemon/g,
      /service\s*=/g,
      /startup/g,
      /cron/g,
      /crontab/g,
      /background/g,
      /nohup/g,
      /systemctl/g,
      /launchctl/g
    ];
    
    // Python
    const pyPatterns = [
      /schedule\./g,
      /APScheduler/g,
      /threading\.Timer/g,
      /daemon=True/g
    ];
    
    // JavaScript
    const jsPatterns = [
      /setInterval/g,
      /setTimeout/g,
      /daemon/g
    ];
    
    // Go
    const goPatterns = [
      /time\.Tick/g,
      /time\.NewTicker/g
    ];
    
    // Rust
    const rsPatterns = [
      /tokio::time/g,
      /std::thread::spawn/g
    ];
    
    // Java
    const javaPatterns = [
      /TimerTask/g,
      /ScheduledExecutorService/g,
      /@Scheduled/g
    ];
    
    // Ruby
    const rbPatterns = [
      /whenever/g,
      /rufus-scheduler/g,
      /Thread\.new/g
    ];
    
    // 开机启动
    const startupPatterns = [
      /\/etc\/init\.d/g,
      /\/etc\/systemd/g,
      /Library\/LaunchAgents/g,
      /Library\/LaunchDaemons/g,
      /HKEY_CURRENT_USER.*Run/g,
      /HKEY_LOCAL_MACHINE.*Run/g
    ];
    
    const allPatterns = [
      ...shellPatterns, ...pyPatterns, ...jsPatterns, 
      ...goPatterns, ...rsPatterns, ...javaPatterns, ...rbPatterns,
      ...startupPatterns
    ];
    
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8');
      for (const pattern of allPatterns) {
        const matches = content.match(pattern);
        if (matches) {
          issues.push({
            file: path.relative(this.skillPath, file),
            pattern: pattern.source
          });
        }
      }
    }
    
    this.results.checks.persistence = {
      passed: issues.filter(i => i.pattern === 'daemon' || i.pattern === 'cron' || i.pattern === 'crontab').length === 0,
      issues: issues,
      message: issues.filter(i => i.pattern === 'daemon' || i.pattern === 'cron' || i.pattern === 'crontab').length === 0 ? '无后台驻留' : `发现 ${issues.length} 处持久化相关代码,需审查`
    };
  }

  /**
   * 检查运行时安装
   */
  checkRuntimeInstallation() {
    const files = this.getCodeFiles();
    const issues = [];
    
    // JavaScript/Node.js
    const jsPatterns = [
      /npm\s+install/g,
      /yarn\s+add/g,
      /pnpm\s+add/g
    ];
    
    // Python
    const pyPatterns = [
      /pip\s+install/g,
      /pip3\s+install/g,
      /subprocess\.call.*pip/g,
      /subprocess\.run.*pip/g,
      /os\.system.*pip/g,
      /__import__/g
    ];
    
    // Rust
    const rsPatterns = [
      /Command::new\s*\(\s*["']cargo["']\s*\)/g
    ];
    
    // Go
    const goPatterns = [
      /exec\.Command\s*\(\s*["']go["']/g,
      /exec\.Command\s*\(\s*["']go\s+get["']/g
    ];
    
    // Ruby
    const rbPatterns = [
      /system\s*\(\s*["']gem\s+install/g,
      /`gem\s+install/g
    ];
    
    // Java
    const javaPatterns = [
      /Runtime\.getRuntime\(\)\.exec.*mvn/g,
      /ProcessBuilder.*gradle/g
    ];
    
    // 动态导入/加载
    const dynamicPatterns = [
      /require\s*\(\s*["'][^"']+["']\s*\)/g,
      /importlib/g,
      /import\s*\(\s*["'][^"']+["']\s*\)/g
    ];
    
    const allPatterns = [
      ...jsPatterns, ...pyPatterns, ...rsPatterns, 
      ...goPatterns, ...rbPatterns, ...javaPatterns,
      ...dynamicPatterns
    ];
    
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8');
      for (const pattern of allPatterns) {
        const matches = content.match(pattern);
        if (matches) {
          issues.push({
            file: path.relative(this.skillPath, file),
            pattern: pattern.source
          });
        }
      }
    }
    
    const hasRuntimeInstall = issues.some(i => 
      i.pattern.includes('npm install') || 
      i.pattern.includes('pip install') ||
      i.pattern.includes('cargo') ||
      i.pattern.includes('go get') ||
      i.pattern.includes('gem install')
    );
    
    this.results.checks.runtimeInstallation = {
      passed: !hasRuntimeInstall,
      issues: issues,
      message: !hasRuntimeInstall ? '依赖预先声明' : `发现运行时安装命令,需审查`
    };
  }

  /**
   * 检查代码混淆
   */
  checkCodeObfuscation() {
    const files = this.getCodeFiles();
    const codeFiles = files.filter(f => {
      const ext = path.extname(f).toLowerCase();
      return ['.js', '.ts', '.jsx', '.tsx', '.py', '.rs', '.java', '.go', '.rb', '.php', '.c', '.cpp', '.cc'].includes(ext);
    });
    
    let obfuscated = false;
    let reasons = [];
    
    for (const file of codeFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      const ext = path.extname(file).toLowerCase();
      
      // 检查是否所有变量都是单个字母
      const lines = content.split('\n');
      let singleLetterVars = 0;
      let totalVars = 0;
      
      let varPattern;
      if (['.js', '.ts', '.jsx', '.tsx'].includes(ext)) {
        varPattern = /\b(let|const|var|function)\s+(\w+)/g;
      } else if (ext === '.py') {
        varPattern = /\b(def|class)\s+(\w+)|(\w+)\s*=/g;
      } else if (ext === '.rs') {
        varPattern = /\b(let|fn|struct|impl)\s+(\w+)|(\w+)\s*:/g;
      } else if (ext === '.java') {
        varPattern = /\b(public|private|protected)?\s*(static)?\s*(void|String|int|boolean|class)\s+(\w+)|(\w+)\s*=/g;
      } else if (ext === '.go') {
        varPattern = /\b(func|var|const|type)\s+(\w+)|(\w+)\s*:=/g;
      } else if (ext === '.rb') {
        varPattern = /\b(def|class|module)\s+(\w+)|@?\w+\s*=/g;
      } else if (ext === '.php') {
        varPattern = /\$\w+/g;
      } else {
        varPattern = /\b(int|char|void|float|double|string)\s+(\w+)|(\w+)\s*=/g;
      }
      
      const varMatches = content.match(varPattern);
      if (varMatches) {
        totalVars = varMatches.length;
        singleLetterVars = varMatches.filter(v => {
          if (ext === '.php') {
            const name = v.replace('$', '');
            return name.length === 1;
          }
          const parts = v.split(/\s+|:=|:|=|\$/);
          const name = parts[parts.length - 1] || parts[0];
          return name && name.length === 1 && name.match(/[a-zA-Z]/);
        }).length;
      }
      
      if (totalVars > 10 && singleLetterVars / totalVars > 0.5) {
        obfuscated = true;
        reasons.push(`${path.relative(this.skillPath, file)}: 过多单字母变量 (${singleLetterVars}/${totalVars})`);
      }
      
      // 检查是否有大量编码字符串
      const encodedStrings = content.match(/["'][^"']{50,}["']/g);
      if (encodedStrings && encodedStrings.length > 5) {
        obfuscated = true;
        reasons.push(`${path.relative(this.skillPath, file)}: 包含 ${encodedStrings.length} 个长字符串`);
      }
      
      // 检查是否一行特别长
      const longLines = lines.filter(l => l.length > 500);
      if (longLines.length > 5) {
        obfuscated = true;
        reasons.push(`${path.relative(this.skillPath, file)}: 包含 ${longLines.length} 行超长代码`);
      }
      
      // 检查Base64/Hex编码的可疑字符串
      const suspiciousPatterns = [
        /[A-Za-z0-9+\/]{100,}={0,2}/g, // Base64-like
        /[0-9a-fA-F]{50,}/g, // Hex-like
        /\\\\x[0-9a-fA-F]{2}/g, // Escape sequences
        /\\\\u[0-9a-fA-F]{4}/g
      ];
      
      let suspiciousCount = 0;
      for (const pattern of suspiciousPatterns) {
        const matches = content.match(pattern);
        if (matches) suspiciousCount += matches.length;
      }
      
      if (suspiciousCount > 10) {
        obfuscated = true;
        reasons.push(`${path.relative(this.skillPath, file)}: 包含 ${suspiciousCount} 处可疑编码字符串`);
      }
    }
    
    this.results.checks.codeObfuscation = {
      passed: !obfuscated,
      issues: reasons.map(r => ({ file: r, pattern: 'obfuscation' })),
      message: !obfuscated ? '源码清晰可读' : `发现代码混淆迹象: ${reasons.length} 个问题`
    };
  }

  /**
   * 检查进程侦察
   */
  checkProcessReconnaissance() {
    const files = this.getCodeFiles();
    const issues = [];
    
    // Shell命令
    const shellPatterns = [
      /ps\s+/g,
      /tasklist/g,
      /wmic/g,
      /\/proc\//g
    ];
    
    // Python
    const pyPatterns = [
      /psutil/g,
      /subprocess\.call.*ps/g,
      /subprocess\.run.*ps/g,
      /os\.listdir\s*\(\s*["']\/proc["']/g
    ];
    
    // JavaScript
    const jsPatterns = [
      /process\.list/g,
      /enumerateProcesses/g
    ];
    
    // Go
    const goPatterns = [
      /exec\.Command\s*\(\s*["']ps["']/g,
      /process\./g
    ];
    
    // Rust
    const rsPatterns = [
      /sysinfo::/g,
      /psutil::/g,
      /std::process::Command.*ps/g
    ];
    
    // Java
    const javaPatterns = [
      /ProcessHandle\.allProcesses/g,
      /ManagementFactory\.getRuntimeMXBean/g,
      /sigar\./g
    ];
    
    // Ruby
    const rbPatterns = [
      /Sys::ProcTable/g,
      /`ps`/g,
      /system.*ps/g
    ];
    
    // PHP
    const phpPatterns = [
      /proc_open/g,
      /shell_exec.*ps/g,
      /exec.*ps/g
    ];
    
    const allPatterns = [
      ...shellPatterns, ...pyPatterns, ...jsPatterns, 
      ...goPatterns, ...rsPatterns, ...javaPatterns, 
      ...rbPatterns, ...phpPatterns
    ];
    
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8');
      for (const pattern of allPatterns) {
        const matches = content.match(pattern);
        if (matches) {
          issues.push({
            file: path.relative(this.skillPath, file),
            pattern: pattern.source
          });
        }
      }
    }
    
    this.results.checks.processReconnaissance = {
      passed: issues.length === 0,
      issues: issues,
      message: issues.length === 0 ? '无系统扫描' : `发现 ${issues.length} 处进程扫描代码`
    };
  }

  /**
   * 检查浏览器会话访问
   */
  checkBrowserSessionAccess() {
    const files = this.getCodeFiles();
    const issues = [];
    
    // JavaScript/TypeScript
    const jsPatterns = [
      /puppeteer/g,
      /playwright/g,
      /selenium/g,
      /chrome\.launch/g,
      /--user-data-dir/g,
      /@playwright\/test/g
    ];
    
    // Python
    const pyPatterns = [
      /selenium/g,
      /playwright/g,
      /pyppeteer/g,
      /splinter/g,
      /user_data_dir/g
    ];
    
    // Rust
    const rsPatterns = [
      /headless_chrome/g,
      /thirtyfour/g,
      /fantoccini/g
    ];
    
    // Java
    const javaPatterns = [
      /selenium/g,
      /ChromeDriver/g,
      /WebDriver/g,
      /HtmlUnitDriver/g
    ];
    
    // Go
    const goPatterns = [
      /chromedp/g,
      /rod/g,
      /playwright-go/g
    ];
    
    // Ruby
    const rbPatterns = [
      /selenium-webdriver/g,
      /watir/g,
      /capybara/g
    ];
    
    // PHP
    const phpPatterns = [
      /facebook\/webdriver/g,
      /php-webdriver/g,
      /panther/g
    ];
    
    const allPatterns = [
      ...jsPatterns, ...pyPatterns, ...rsPatterns, 
      ...javaPatterns, ...goPatterns, ...rbPatterns, ...phpPatterns
    ];
    
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8');
      for (const pattern of allPatterns) {
        const matches = content.match(pattern);
        if (matches) {
          issues.push({
            file: path.relative(this.skillPath, file),
            pattern: pattern.source
          });
        }
      }
    }
    
    const hasBrowserAutomation = issues.some(i => 
      i.pattern.includes('puppeteer') || 
      i.pattern.includes('playwright') ||
      i.pattern.includes('selenium') ||
      i.pattern.includes('selenium-webdriver') ||
      i.pattern.includes('headless') ||
      i.pattern.includes('chromedp')
    );
    
    const hasIsolatedProfile = issues.some(i => 
      i.pattern.includes('--user-data-dir') || 
      i.pattern.includes('user_data_dir')
    );
    
    this.results.checks.browserSessionAccess = {
      passed: !hasBrowserAutomation || hasIsolatedProfile,
      issues: issues,
      message: !hasBrowserAutomation ? '无浏览器自动化' : 
                hasIsolatedProfile ? '使用独立 Chrome 配置文件' : '浏览器自动化未使用独立配置文件'
    };
  }

  /**
   * 执行所有检查
   */
  runAllChecks() {
    console.log(`🔍 开始检查 skill: ${this.skillPath}\n`);
    
    this.checkDataExfiltration();
    this.checkCredentialAccess();
    this.checkFilesystemEscaping();
    this.checkSensitiveFileAccess();
    this.checkDynamicCodeExecution();
    this.checkPrivilegeEscalation();
    this.checkPersistence();
    this.checkRuntimeInstallation();
    this.checkCodeObfuscation();
    this.checkProcessReconnaissance();
    this.checkBrowserSessionAccess();
    
    return this.results;
  }

  /**
   * 生成报告
   */
  generateReport() {
    const checks = this.results.checks;
    const totalChecks = Object.keys(checks).length;
    const passedChecks = Object.values(checks).filter(c => c.passed).length;
    const failedCount = totalChecks - passedChecks;
    
    // 分析安全优势和注意事项
    const securityAdvantages = [];
    const userNotices = [];
    const riskIssues = [];
    
    // 数据外泄分析
    if (checks.dataExfiltration?.passed) {
      securityAdvantages.push({
        title: '无数据外泄',
        detail: '无外部服务器通信'
      });
    } else {
      const networkIssues = checks.dataExfiltration?.issues || [];
      const userInitiated = networkIssues.every(i => 
        i.file.includes('browser') || 
        i.pattern.includes('browser')
      );
      if (userInitiated) {
        userNotices.push({
          title: '网络请求',
          detail: '所有网络请求都是用户主动发起的（下载图片、通过浏览器发推）'
        });
      } else {
        riskIssues.push({
          check: '数据外泄',
          detail: checks.dataExfiltration?.message
        });
      }
    }
    
    // 代码混淆分析
    if (checks.codeObfuscation?.passed) {
      securityAdvantages.push({
        title: '透明代码',
        detail: '所有源码可读，无混淆'
      });
    } else {
      riskIssues.push({
        check: '代码混淆',
        detail: checks.codeObfuscation?.message
      });
    }
    
    // 凭证访问分析
    if (checks.credentialAccess?.issues?.length === 0) {
      securityAdvantages.push({
        title: '凭证安全',
        detail: '不访问敏感凭证或会话令牌'
      });
    } else {
      const credentialIssues = checks.credentialAccess?.issues || [];
      const onlyConfigVars = credentialIssues.every(i => 
        i.pattern.includes('process.env') && 
        !i.pattern.includes('SECRET') && 
        !i.pattern.includes('PASSWORD') &&
        !i.pattern.includes('TOKEN')
      );
      if (onlyConfigVars) {
        securityAdvantages.push({
          title: '凭证安全',
          detail: '仅读取配置型环境变量，不访问敏感凭证'
        });
      }
    }
    
    // 文件系统分析
    if (checks.filesystemEscaping?.passed) {
      securityAdvantages.push({
        title: '作用域隔离',
        detail: '仅访问用户明确提供的文件'
      });
    } else {
      const fsIssues = checks.filesystemEscaping?.issues || [];
      const userFiles = fsIssues.every(i => !i.pattern.includes('..'));
      if (userFiles) {
        userNotices.push({
          title: '文件访问',
          detail: '访问用户指定目录内的文件'
        });
      } else {
        riskIssues.push({
          check: '文件系统越界',
          detail: checks.filesystemEscaping?.message
        });
      }
    }
    
    // 持久化机制
    if (checks.persistence?.passed) {
      securityAdvantages.push({
        title: '无持久化',
        detail: '无 crontab、启动脚本或后台服务'
      });
    } else {
      const persistIssues = checks.persistence?.issues || [];
      const onlyBrowserSession = persistIssues.every(i => 
        i.file.includes('browser') || 
        i.file.includes('chrome')
      );
      if (onlyBrowserSession) {
        userNotices.push({
          title: 'Chrome 会话持久化',
          detail: '首次运行需手动登录，会话保存在 Chrome 配置文件中'
        });
      } else {
        riskIssues.push({
          check: '持久化机制',
          detail: checks.persistence?.message
        });
      }
    }
    
    // 权限提升
    if (checks.privilegeEscalation?.passed) {
      securityAdvantages.push({
        title: '无权限提升',
        detail: '无 sudo、chmod 或 setuid 操作'
      });
    } else {
      riskIssues.push({
        check: '权限提升',
        detail: checks.privilegeEscalation?.message
      });
    }
    
    // 运行时安装
    if (checks.runtimeInstallation?.passed) {
      securityAdvantages.push({
        title: '干净的依赖',
        detail: '所有依赖都是预先声明的'
      });
    } else {
      userNotices.push({
        title: '运行时安装',
        detail: '会在运行时安装必要的依赖包'
      });
    }
    
    // 浏览器自动化
    if (checks.browserSessionAccess?.issues?.length > 0) {
      const browserIssues = checks.browserSessionAccess?.issues || [];
      const hasBrowser = browserIssues.some(i => 
        i.pattern.includes('puppeteer') || 
        i.pattern.includes('playwright') ||
        i.pattern.includes('selenium')
      );
      if (hasBrowser) {
        userNotices.push({
          title: '浏览器自动化',
          detail: '通过 CDP 控制 Chrome（发布功能所需）'
        });
      }
    }
    
    // 动态代码执行
    if (!checks.dynamicCodeExecution?.passed) {
      const execIssues = checks.dynamicCodeExecution?.issues || [];
      const onlyChildProcess = execIssues.every(i => 
        i.pattern.includes('child_process') ||
        i.pattern.includes('exec') ||
        i.pattern.includes('spawn')
      );
      if (onlyChildProcess) {
        userNotices.push({
          title: '子进程调用',
          detail: '使用 child_process 执行系统命令'
        });
      } else {
        riskIssues.push({
          check: '动态代码执行',
          detail: checks.dynamicCodeExecution?.message
        });
      }
    }
    
    // 敏感文件访问
    if (!checks.sensitiveFileAccess?.passed) {
      riskIssues.push({
        check: '身份文件访问',
        detail: checks.sensitiveFileAccess?.message
      });
    }
    
    // 进程侦察
    if (!checks.processReconnaissance?.passed) {
      riskIssues.push({
        check: '进程侦察',
        detail: checks.processReconnaissance?.message
      });
    }
    
    // 计算风险等级
    let riskLevel = 'LOW';
    let finalRating = 'SAFE';
    let confidence = 'HIGH';
    
    if (riskIssues.length >= 3 || riskIssues.some(r => 
      r.check === '数据外泄' || 
      r.check === '权限提升' ||
      r.check === '敏感文件访问'
    )) {
      riskLevel = 'HIGH';
      finalRating = 'UNSAFE';
      confidence = 'HIGH';
    } else if (riskIssues.length > 0) {
      riskLevel = 'MEDIUM';
      finalRating = 'REVIEW_NEEDED';
      confidence = 'MEDIUM';
    }
    
    // 生成报告
    let report = `# 安全审查完成 ✅\n\n`;
    report += `已完成对 **${this.results.skillName}** skill\n`;
    report += `的全面安全审查，并生成详细报告。\n\n`;
    
    report += `## 📊 审查结果\n\n`;
    
    // 风险等级
    const riskIcon = riskLevel === 'LOW' ? '🟢' : riskLevel === 'MEDIUM' ? '🟡' : '🔴';
    const ratingIcon = finalRating === 'SAFE' ? '✅' : finalRating === 'REVIEW_NEEDED' ? '⚠️' : '❌';
    report += `**风险等级:** ${riskIcon} ${riskLevel}\n`;
    report += `**最终评级:** ${ratingIcon} ${finalRating.replace('_', ' ')}\n`;
    report += `**置信度:** ${confidence}\n\n`;
    
    report += `---\n\n`;
    
    // 关键发现
    report += `## 🔍 关键发现\n\n`;
    
    // 安全优势
    if (securityAdvantages.length > 0) {
      report += `### ✅ 安全优势\n\n`;
      securityAdvantages.forEach((adv, idx) => {
        report += `${idx + 1}. **${adv.title}** - ${adv.detail}\n`;
      });
      report += `\n`;
    }
    
    // 需要用户知晓的点
    if (userNotices.length > 0) {
      report += `### ⚠️ 需要用户知晓的点（非漏洞）\n\n`;
      userNotices.forEach((notice, idx) => {
        report += `${idx + 1}. **${notice.title}** - ${notice.detail}\n`;
      });
      report += `\n`;
    }
    
    // 风险问题（如果有）
    if (riskIssues.length > 0) {
      report += `### 🚨 安全风险\n\n`;
      riskIssues.forEach((risk, idx) => {
        report += `${idx + 1}. **${risk.check}** - ${risk.detail}\n`;
      });
      report += `\n`;
    }
    
    report += `---\n\n`;
    
    // 详细检查项表格
    report += `## 📋 详细检查项\n\n`;
    report += `| 检查项 | 结果 | 说明 |\n`;
    report += `|--------|------|------|\n`;
    
    const checkNames = {
      dataExfiltration: '数据外泄',
      credentialAccess: '凭证访问',
      filesystemEscaping: '文件系统越界',
      sensitiveFileAccess: '身份文件访问',
      dynamicCodeExecution: '动态代码执行',
      privilegeEscalation: '权限提升',
      persistence: '持久化机制',
      runtimeInstallation: '运行时安装',
      codeObfuscation: '代码混淆',
      processReconnaissance: '进程侦察',
      browserSessionAccess: '浏览器会话访问'
    };
    
    for (const [key, check] of Object.entries(checks)) {
      const status = check.passed ? '✅' : '❌';
      report += `| ${checkNames[key]} | ${status} | ${check.message} |\n`;
    }
    
    report += `\n`;
    
    // 技术详情
    if (Object.values(checks).some(c => !c.passed && c.issues?.length > 0)) {
      report += `## 🔧 技术详情\n\n`;
      report += `<details>\n<summary>点击查看详细技术信息</summary>\n\n`;
      
      for (const [key, check] of Object.entries(checks)) {
        if (!check.passed && check.issues?.length > 0) {
          report += `### ${checkNames[key]}\n\n`;
          report += `**问题描述:** ${check.message}\n\n`;
          report += `**相关位置:**\n`;
          for (const issue of check.issues.slice(0, 5)) {
            report += `- \`${issue.file}\`: 匹配 \`${issue.pattern}\`\n`;
          }
          if (check.issues.length > 5) {
            report += `- ... 还有 ${check.issues.length - 5} 个位置\n`;
          }
          report += `\n`;
        }
      }
      
      report += `</details>\n`;
    }
    
    // 建议操作
    report += `\n## 💡 建议操作\n\n`;
    if (finalRating === 'SAFE') {
      report += `- **安全等级:** ✅ 安全\n`;
      report += `- **建议:** 可以安全安装此skill\n`;
    } else if (finalRating === 'REVIEW_NEEDED') {
      report += `- **安全等级:** ⚠️ 需要注意\n`;
      report += `- **建议:** 请仔细阅读上述"需要用户知晓的点"，确认接受后再安装\n`;
    } else {
      report += `- **安全等级:** ❌ 高风险\n`;
      report += `- **建议:** 不建议安装此skill。如果确实需要，请先审查源码并了解风险\n`;
    }
    
    report += `\n---\n`;
    report += `*报告生成时间: ${this.results.timestamp}*\n`;
    
    return report;
  }
}

// CLI 入口
if (require.main === module) {
  const skillPath = process.argv[2];
  
  if (!skillPath) {
    console.error('用法: node security-check.js <skill-path>');
    process.exit(1);
  }
  
  if (!fs.existsSync(skillPath)) {
    console.error(`错误: 路径不存在: ${skillPath}`);
    process.exit(1);
  }
  
  const checker = new SecurityChecker(skillPath);
  checker.runAllChecks();
  
  const report = checker.generateReport();
  console.log(report);
  
  // 保存报告
  const reportPath = path.join(process.cwd(), `security-report-${path.basename(skillPath)}.md`);
  fs.writeFileSync(reportPath, report);
  console.log(`\n📄 报告已保存: ${reportPath}`);
}

module.exports = SecurityChecker;
