#!/bin/bash

# ========================================
#    OpenClaw 本地部署脚本 (macOS 12+)
#    一键安装 Node.js + Git + OpenClaw
# ========================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   OpenClaw 本地部署脚本 (macOS 12+)   ${NC}"
echo -e "${BLUE}========================================${NC}"
echo

# 检查是否安装了 Homebrew
check_homebrew() {
    echo -e "${BLUE}[1/5]${NC} 检查 Homebrew ..."
    if ! command -v brew &> /dev/null; then
        echo -e "${YELLOW}Homebrew 未安装，正在安装...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # 配置 Homebrew 环境变量
        if [[ $(uname -m) == "arm64" ]]; then
            # Apple Silicon
            echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
            eval "$(/opt/homebrew/bin/brew shellenv)"
        else
            # Intel
            echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
            eval "$(/usr/local/bin/brew shellenv)"
        fi
        echo -e "${GREEN}[✓]${NC} Homebrew 安装完成"
    else
        echo -e "${GREEN}[✓]${NC} Homebrew 已安装: $(brew --version | head -n1)"
    fi
    echo
}

# 安装 Node.js 和 Git
install_deps() {
    echo -e "${BLUE}[2/5]${NC} 安装 Node.js 22.x 和 Git ..."
    
    # 安装 node@22
    if ! brew list node@22 &>/dev/null; then
        echo "正在安装 Node.js 22.x..."
        brew install node@22 git
        
        # 配置环境变量
        if [[ $(uname -m) == "arm64" ]]; then
            echo 'export PATH="/opt/homebrew/opt/node@22/bin:$PATH"' >> ~/.zshrc
            export PATH="/opt/homebrew/opt/node@22/bin:$PATH"
        else
            echo 'export PATH="/usr/local/opt/node@22/bin:$PATH"' >> ~/.zshrc
            export PATH="/usr/local/opt/node@22/bin:$PATH"
        fi
        echo -e "${GREEN}[✓]${NC} Node.js 22.x 安装完成"
    else
        echo -e "${GREEN}[✓]${NC} Node.js 22.x 已安装"
    fi
    
    # 确保 git 已安装
    if ! command -v git &> /dev/null; then
        brew install git
    fi
    echo -e "${GREEN}[✓]${NC} Git 已安装: $(git --version)"
    echo
}

# 配置 npm 镜像
configure_npm() {
    echo -e "${BLUE}[3/5]${NC} 配置 npm 国内镜像 ..."
    npm config set registry https://registry.npmmirror.com
    echo -e "${GREEN}[✓]${NC} npm 镜像配置完成: https://registry.npmmirror.com"
    echo
}

# 安装 OpenClaw
install_openclaw() {
    echo -e "${BLUE}[4/5]${NC} 安装 OpenClaw ..."
    echo "这可能需要几分钟，请耐心等待..."
    
    npm install -g openclaw@latest
    
    if command -v openclaw &> /dev/null; then
        echo -e "${GREEN}[✓]${NC} OpenClaw 安装完成: $(openclaw --version 2>/dev/null || echo '版本信息获取中')"
    else
        echo -e "${RED}[✗]${NC} OpenClaw 安装可能出现问题"
        echo "请尝试手动运行: npm install -g openclaw@latest"
        exit 1
    fi
    echo
}

# 初始化工作空间
init_workspace() {
    echo -e "${BLUE}[5/5]${NC} 初始化工作空间 ..."
    
    WORKSPACE_DIR="$HOME/OpenClaw-Workspace"
    
    if [ ! -d "$WORKSPACE_DIR" ]; then
        mkdir -p "$WORKSPACE_DIR"
        echo -e "${GREEN}[✓]${NC} 创建工作目录: $WORKSPACE_DIR"
    fi
    
    cd "$WORKSPACE_DIR"
    
    echo "正在初始化 OpenClaw 配置..."
    openclaw init || {
        echo -e "${YELLOW}[提示]${NC} 初始化命令可能需要手动执行"
        echo "请运行以下命令："
        echo "    cd $WORKSPACE_DIR"
        echo "    openclaw init"
    }
    
    echo -e "${GREEN}[✓]${NC} 工作空间初始化完成"
    echo
}

# 验证安装
verify_installation() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${GREEN}          安装完成！                  ${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo
    echo "[验证信息]"
    echo "Node.js: $(node --version 2>/dev/null || echo '请重启终端')"
    echo "Git: $(git --version 2>/dev/null || echo '请重启终端')"
    echo "OpenClaw: $(openclaw --version 2>/dev/null || echo '请重启终端')"
    echo
    echo "[启动 Gateway 服务]"
    echo "前台启动: openclaw gateway start"
    echo "后台启动: nohup openclaw gateway start &"
    echo
    echo "[访问控制台]"
    echo "浏览器访问: http://localhost:18789"
    echo
    echo -e "${YELLOW}提示: 如果命令未找到，请重启终端或运行: source ~/.zshrc${NC}"
}

# 主函数
main() {
    check_homebrew
    install_deps
    configure_npm
    install_openclaw
    init_workspace
    verify_installation
}

main "$@"
