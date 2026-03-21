#!/bin/bash

echo "======================================"
echo "N8N - npm 安装方式"
echo "======================================"
echo ""
echo "这是使用 npm 安装 N8N 的备选方案"
echo "推荐使用 Docker 方式（更简单）"
echo ""
read -p "确认继续 npm 安装？(y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消安装"
    exit 1
fi

# 检查 Node.js
echo "检查 Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ 未安装 Node.js"
    echo "请先安装 Node.js: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v)
echo "✅ Node.js 版本: $NODE_VERSION"

# 检查 npm
if ! command -v npm &> /dev/null; then
    echo "❌ 未安装 npm"
    exit 1
fi

NPM_VERSION=$(npm -v)
echo "✅ npm 版本: $NPM_VERSION"
echo ""

# 安装 N8N
echo "正在安装 N8N..."
npm install -g n8n

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✅ N8N 安装成功！"
    echo "======================================"
    echo ""
    echo "启动命令:"
    echo "  n8n start"
    echo ""
    echo "自定义端口启动:"
    echo "  n8n start --port 5678"
    echo ""
    echo "开发模式（带隧道）:"
    echo "  n8n start --tunnel"
    echo ""
    echo "访问地址: http://localhost:5678"
    echo ""
    
    read -p "是否现在启动 N8N？(y/n) " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "启动 N8N..."
        n8n start
    fi
else
    echo ""
    echo "❌ 安装失败"
    echo "请检查错误信息"
fi


