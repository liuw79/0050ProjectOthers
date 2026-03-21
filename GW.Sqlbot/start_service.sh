#!/bin/bash

echo "🚀 启动本地SQLBot服务"
echo "===================="

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，正在创建..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "📦 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖包..."
pip install flask psycopg2-binary openai python-dotenv

# 加载环境变量
if [ -f "config/.env" ]; then
    echo "⚙️  加载环境配置..."
    export $(cat config/.env | grep -v '^#' | xargs)
fi

# 检查端口占用
echo "🔍 检查端口8080..."
if lsof -i :8080 >/dev/null 2>&1; then
    echo "⚠️  端口8080被占用，正在清理..."
    lsof -ti :8080 | xargs kill -9 2>/dev/null
    sleep 2
fi

# 启动服务
echo "🌐 启动SQLBot服务..."
echo "访问地址: http://localhost:8080"
echo "按 Ctrl+C 停止服务"
echo "===================="

python start_local_sqlbot.py