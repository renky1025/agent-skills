@echo off
chcp 65001 >nul
title OpenClaw 本地部署脚本 - Windows 11
setlocal enabledelayedexpansion

echo ========================================
echo    OpenClaw 本地部署脚本 (Windows 11)
echo    一键安装 Node.js + Git + OpenClaw
echo ========================================
echo.
echo 请以管理员身份运行此脚本！
echo 按任意键继续...
pause >nul

:: 检查管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 请以管理员身份运行此脚本！
    echo 右键点击脚本，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo.
echo [1/5] 正在下载并安装 Node.js 22.x ...
echo ----------------------------------------

:: 下载 Node.js
if exist node-install.msi del /f node-install.msi
echo 正在下载 Node.js 安装包（国内镜像）...
powershell -Command "iwr -useb https://npmmirror.com/mirrors/node/v22.10.0/node-v22.10.0-x64.msi -OutFile node-install.msi" 2>nul

if not exist node-install.msi (
    echo [错误] Node.js 下载失败，请检查网络连接
    pause
    exit /b 1
)

echo 正在安装 Node.js，请稍候...
start /wait msiexec /i node-install.msi /qn /norestart

:: 刷新环境变量
call refreshenv.cmd 2>nul || (
    echo 正在刷新环境变量...
    setx PATH "%PATH%;C:\Program Files\nodejs\" >nul 2>&1
)

echo [✓] Node.js 安装完成
echo.

:: 验证 Node.js
echo 正在验证 Node.js 安装...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] Node.js 可能需要重启终端才能使用
    echo 请将 C:\Program Files\nodejs\ 添加到系统 PATH
) else (
    for /f "tokens=*" %%a in ('node --version') do echo [✓] Node.js 版本: %%a
)

echo.
echo [2/5] 正在安装 Git ...
echo ----------------------------------------

:: 检查是否已安装 Git
git --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%a in ('git --version') do echo [✓] Git 已安装: %%a
) else (
    echo 正在通过 winget 安装 Git...
    winget install Git.Git --accept-package-agreements --accept-source-agreements
    echo [✓] Git 安装完成
)

echo.
echo [3/5] 正在配置 npm 国内镜像 ...
echo ----------------------------------------
:: 等待 Node.js 完全可用
ping -n 3 127.0.0.1 >nul
node --version >nul 2>&1
if %errorlevel% equ 0 (
    npm config set registry https://registry.npmmirror.com
    echo [✓] npm 镜像配置完成: https://registry.npmmirror.com
) else (
    echo [警告] Node.js 尚未就绪，请手动运行以下命令：
    echo    npm config set registry https://registry.npmmirror.com
)

echo.
echo [4/5] 正在安装 OpenClaw ...
echo ----------------------------------------
node --version >nul 2>&1
if %errorlevel% equ 0 (
    echo 正在全局安装 OpenClaw，这可能需要几分钟...
    npm install -g openclaw@latest
    if %errorlevel% neq 0 (
        echo [错误] OpenClaw 安装失败
        pause
        exit /b 1
    )
    echo [✓] OpenClaw 安装完成
) else (
    echo [错误] Node.js 未就绪，无法安装 OpenClaw
    echo 请重启终端后手动运行: npm install -g openclaw@latest
    pause
    exit /b 1
)

echo.
echo [5/5] 正在初始化工作空间 ...
echo ----------------------------------------
if not exist "%USERPROFILE%\OpenClaw-Workspace" (
    mkdir "%USERPROFILE%\OpenClaw-Workspace"
    echo [✓] 创建工作目录: %USERPROFILE%\OpenClaw-Workspace
)

cd /d "%USERPROFILE%\OpenClaw-Workspace"
openclaw init 2>nul || (
    echo [提示] 请在终端中手动运行以下命令完成初始化：
    echo    cd %USERPROFILE%\OpenClaw-Workspace
    echo    openclaw init
)

echo.
echo ========================================
echo    安装完成！
echo ========================================
echo.
echo [验证信息]
node --version 2>nul && echo 或显示版本信息
git --version 2>nul && echo 或显示版本信息
openclaw --version 2>nul && echo 或显示版本信息
echo.
echo [启动 Gateway 服务]
echo 前台启动: openclaw gateway start
echo 后台启动: Start-Job -ScriptBlock {openclaw gateway start}
echo.
echo [访问控制台]
echo 浏览器访问: http://localhost:18789
echo.
echo 按任意键退出...
pause >nul
endlocal
