#!/bin/bash

# ========================================
#    OpenClaw 本地部署脚本 (Ubuntu 20.04+)
#    一键安装 Node.js + Git + OpenClaw
# ========================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   OpenClaw 本地部署脚本 (Ubuntu)      ${NC}"
echo -e "${BLUE}========================================${NC}"
echo

# 检查 root 权限
check_root() {
    if [[ $EUID -ne 0 ]]; then
        echo -e "${YELLOW}[提示]${NC} 部分操作需要 root 权限，建议以 sudo 运行此脚本"
        echo "例如: sudo bash openclaw-install-linux.sh"
        echo
    fi
}

# 安装 Node.js 和 Git
install_deps() {
    echo -e "${BLUE}[1/4]${NC} 安装 Node.js 22.x 和 Git ..."
    
    # 检查是否已安装 Node.js 22.x
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
        if [ "$NODE_VERSION" = "22" ]; then
            echo -e "${GREEN}[✓]${NC} Node.js 22.x 已安装: $(node --version)"
        else
            echo -e "${YELLOW}检测到 Node.js $(node --version)，正在升级到 22.x...${NC}"
            install_nodejs
        fi
    else
        install_nodejs
    fi
    
    # 安装 Git
    if ! command -v git &> /dev/null; then
        echo "正在安装 Git..."
        sudo apt update
        sudo apt install -y git
    fi
    echo -e "${GREEN}[✓]${NC} Git 已安装: $(git --version)"
    echo
}

# 安装 Node.js 22.x
install_nodejs() {
    echo "正在安装 Node.js 22.x..."
    
    # 使用 NodeSource 安装
    curl -fsSL https://deb.nodesource.com/setup_22.x | sudo bash -
    sudo apt install -y nodejs
    
    echo -e "${GREEN}[✓]${NC} Node.js 安装完成: $(node --version)"
}

# 配置 npm 镜像和权限
configure_npm() {
    echo -e "${BLUE}[2/4]${NC} 配置 npm 国内镜像 ..."
    
    # 设置国内镜像
    npm config set registry https://registry.npmmirror.com
    echo -e "${GREEN}[✓]${NC} npm 镜像配置完成: https://registry.npmmirror.com"
    
    # 解决权限问题
    echo -e "${BLUE}[3/4]${NC} 解决 npm 全局权限问题 ..."
    
    # 创建 npm 全局目录（如果不存在）
    NPM_PREFIX="$HOME/.npm-global"
    mkdir -p "$NPM_PREFIX"
    
    # 配置 npm 使用新的前缀
    npm config set prefix "$NPM_PREFIX"
    
    # 添加到 PATH
    if ! grep -q "$NPM_PREFIX/bin" ~/.bashrc 2>/dev/null; then
        echo "export PATH=\"$NPM_PREFIX/bin:\$PATH\"" >> ~/.bashrc
        echo -e "${GREEN}[✓]${NC} 已将 npm 全局目录添加到 PATH"
    fi
    
    # 立即生效
    export PATH="$NPM_PREFIX/bin:$PATH"
    
    # 或者修复系统目录权限（备选方案）
    if [ -d "/usr/local/lib/node_modules" ]; then
        sudo chmod -R 777 /usr/local/lib/node_modules 2>/dev/null || true
    fi
    
    echo -e "${GREEN}[✓]${NC} npm 权限配置完成"
    echo
}

# 安装 OpenClaw
install_openclaw() {
    echo -e "${BLUE}[4/4]${NC} 安装 OpenClaw ..."
    echo "这可能需要几分钟，请耐心等待..."
    
    npm install -g openclaw@latest
    
    if command -v openclaw &> /dev/null; then
        echo -e "${GREEN}[✓]${NC} OpenClaw 安装完成"
    else
        # 尝试从新配置的 PATH 中查找
        export PATH="$HOME/.npm-global/bin:$PATH"
        if command -v openclaw &> /dev/null; then
            echo -e "${GREEN}[✓]${NC} OpenClaw 安装完成"
        else
            echo -e "${RED}[✗]${NC} OpenClaw 命令未找到"
            echo "请尝试手动运行: source ~/.bashrc && npm install -g openclaw@latest"
            exit 1
        fi
    fi
    echo
}

# 初始化工作空间
init_workspace() {
    echo "正在初始化工作空间 ..."
    
    WORKSPACE_DIR="$HOME/OpenClaw-Workspace"
    
    if [ ! -d "$WORKSPACE_DIR" ]; then
        mkdir -p "$WORKSPACE_DIR"
        echo -e "${GREEN}[✓]${NC} 创建工作目录: $WORKSPACE_DIR"
    fi
    
    cd "$WORKSPACE_DIR"
    
    echo "正在初始化 OpenClaw 配置..."
    openclaw init 2>/dev/null || {
        # 尝试从新 PATH 运行
        export PATH="$HOME/.npm-global/bin:$PATH"
        openclaw init || {
            echo -e "${YELLOW}[提示]${NC} 初始化命令可能需要手动执行"
            echo "请运行以下命令："
            echo "    source ~/.bashrc"
            echo "    cd $WORKSPACE_DIR"
            echo "    openclaw init"
        }
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
    echo "Node.js: $(node --version 2>/dev/null || echo '请运行: source ~/.bashrc')"
    echo "Git: $(git --version 2>/dev/null || echo '未安装')"
    echo "OpenClaw: $(openclaw --version 2>/dev/null || echo '请运行: source ~/.bashrc')"
    echo
    echo "[启动 Gateway 服务]"
    echo "前台启动: openclaw gateway start"
    echo "后台启动: nohup openclaw gateway start &"
    echo
    echo "[访问控制台]"
    echo "浏览器访问: http://localhost:18789"
    echo
    echo -e "${YELLOW}提示: 如果命令未找到，请运行: source ~/.bashrc${NC}"
}

# 主函数
main() {
    check_root
    install_deps
    configure_npm
    install_openclaw
    init_workspace
    verify_installation
}

main "$@"
