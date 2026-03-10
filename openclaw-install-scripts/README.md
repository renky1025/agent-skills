# OpenClaw 本地部署脚本

本目录包含 OpenClaw 的一键安装脚本，支持 Windows、macOS 和 Linux 三大平台。

## 📋 使用说明

### Windows 11

1. **右键点击** `openclaw-install-windows.bat`
2. 选择 **"以管理员身份运行"**
3. 按提示完成安装

### macOS 12+

```bash
# 1. 赋予执行权限
chmod +x openclaw-install-macos.sh

# 2. 运行安装脚本
bash openclaw-install-macos.sh
```

### Linux (Ubuntu 20.04+)

```bash
# 1. 赋予执行权限
chmod +x openclaw-install-linux.sh

# 2. 运行安装脚本（建议加 sudo）
sudo bash openclaw-install-linux.sh
```

## ✅ 安装内容

所有脚本将自动完成以下安装和配置：

| 组件 | Windows | macOS | Linux |
|------|---------|-------|-------|
| Node.js 22.x | ✓ | ✓ | ✓ |
| Git | ✓ | ✓ | ✓ |
| npm 国内镜像 | ✓ | ✓ | ✓ |
| OpenClaw CLI | ✓ | ✓ | ✓ |
| 工作空间初始化 | ✓ | ✓ | ✓ |

## 🚀 安装后操作

### 启动 Gateway 服务

```bash
# 前台启动（调试使用）
openclaw gateway start

# 后台启动（推荐日常使用）
# Windows:
Start-Job -ScriptBlock {openclaw gateway start}

# macOS/Linux:
nohup openclaw gateway start &
```

### 访问控制台

浏览器打开: http://localhost:18789

## ⚠️ 注意事项

1. **Windows**: 必须以管理员身份运行脚本
2. **macOS**: 首次安装 Homebrew 可能需要输入密码
3. **Linux**: 建议使用 sudo 运行以避免权限问题
4. **所有系统**: 安装完成后可能需要重启终端或运行 `source ~/.bashrc` / `source ~/.zshrc`

## 🔧 手动验证

如果脚本运行后命令不可用，请尝试：

```bash
# 查看 Node.js 版本
node --version  # 应显示 v22.x.x

# 查看 Git 版本
git --version   # 应显示 2.40.x 及以上

# 查看 OpenClaw 版本
openclaw --version
```

## 📝 镜像源

脚本已配置以下国内镜像加速：
- **Node.js**: npmmirror.com
- **npm**: registry.npmmirror.com

---

**制作日期**: 2026-03-09  
**支持 OpenClaw 版本**: Latest
