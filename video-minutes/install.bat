@echo off
chcp 65001 >nul
echo ========================================
echo 视频纪要生成工具 - 安装脚本
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python 未安装
    echo 请先安装 Python 3.8 或更高版本: https://www.python.org/downloads/
    exit /b 1
)

echo [✓] Python 已安装

REM 检查 ffmpeg
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [警告] FFmpeg 未安装
    echo 正在尝试通过 winget 安装...
    winget install Gyan.FFmpeg --accept-package-agreements --accept-source-agreements
    if errorlevel 1 (
        echo [错误] FFmpeg 安装失败
        echo 请手动安装: https://ffmpeg.org/download.html
        exit /b 1
    )
) else (
    echo [✓] FFmpeg 已安装
)

echo.
echo [1/3] 正在安装 Python 依赖...
pip install openai-whisper

if errorlevel 1 (
    echo [错误] 依赖安装失败
    exit /b 1
)

echo.
echo [2/3] 正在复制配置文件...
if not exist "%USERPROFILE%\.video-minutes-config.json" (
    copy "config.json" "%USERPROFILE%\.video-minutes-config.json"
    echo [✓] 配置文件已复制到用户目录
) else (
    echo [i] 配置文件已存在，跳过复制
)

echo.
echo [3/3] 安装完成！
echo.
echo ========================================
echo 使用方法:
echo   python generate_minutes.py ^<视频文件^>
echo.
echo 示例:
echo   python generate_minutes.py meeting.mp4
echo   python generate_minutes.py lecture.mp4 --model medium
echo ========================================
pause
