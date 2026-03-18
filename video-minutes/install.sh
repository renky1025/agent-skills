#!/bin/bash
# 视频纪要生成工具 - 安装脚本 (Linux/macOS)

echo "========================================"
echo "视频纪要生成工具 - 安装脚本"
echo "========================================"
echo

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] Python 未安装"
    echo "请先安装 Python 3.8 或更高版本"
    exit 1
fi

echo "[✓] Python 已安装: $(python3 --version)"

# 检查 ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo
    echo "[警告] FFmpeg 未安装"
    echo "正在尝试安装..."
    
    # 根据系统选择安装方式
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y ffmpeg
        elif command -v yum &> /dev/null; then
            sudo yum install -y ffmpeg
        else
            echo "[错误] 无法自动安装 FFmpeg，请手动安装"
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            brew install ffmpeg
        else
            echo "[错误] 请先安装 Homebrew: https://brew.sh"
            exit 1
        fi
    fi
else
    echo "[✓] FFmpeg 已安装: $(ffmpeg -version | head -n 1)"
fi

echo
echo "[1/3] 正在安装 Python 依赖..."
pip3 install openai-whisper

if [ $? -ne 0 ]; then
    echo "[错误] 依赖安装失败"
    exit 1
fi

echo
echo "[2/3] 正在复制配置文件..."
CONFIG_FILE="$HOME/.video-minutes-config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    cp config.json "$CONFIG_FILE"
    echo "[✓] 配置文件已复制到: $CONFIG_FILE"
else
    echo "[i] 配置文件已存在，跳过复制"
fi

echo
echo "[3/3] 安装完成！"
echo
echo "========================================"
echo "使用方法:"
echo "  python3 generate_minutes.py <视频文件>"
echo
echo "示例:"
echo "  python3 generate_minutes.py meeting.mp4"
echo "  python3 generate_minutes.py lecture.mp4 --model medium"
echo "========================================"
