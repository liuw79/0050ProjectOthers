#!/bin/bash

# 内容创作系统 - 开发环境初始化脚本

echo "🚀 初始化开发环境..."

# 1. 检查环境
if [ ! -f "server/.env" ]; then
  echo "⚠️  警告: .env文件不存在，请复制.env.example并配置"
  if [ -f "server/.env.example" ]; then
    echo "运行: cp server/.env.example server/.env"
  fi
  exit 1
fi

# 2. 安装依赖
echo "📦 安装依赖..."
cd server
if [ ! -d "node_modules" ]; then
  npm install
else
  echo "依赖已安装"
fi
cd ..

# 3. 启动开发服务器
echo "🔧 启动开发服务器..."
cd server
npm run dev &
DEV_PID=$!
cd ..

echo "✅ 开发环境初始化完成！"
echo ""
echo "📝 开发服务器运行在: http://localhost:3000"
echo "📊 进度追踪文件: claude-progress.txt"
echo "📋 功能列表: feature_list.json"
echo ""
echo "💡 提示: Ctrl+C 停止服务器"
echo "💡 服务器PID: $DEV_PID"
