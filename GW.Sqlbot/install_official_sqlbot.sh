#!/bin/bash

echo "🚀 安装并部署官方DataEase SQLBot"
echo "=================================="

# 检查Homebrew
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew未安装，正在安装..."
    /bin/bash -c "$(curl -fsSL https://mirrors.ustc.edu.cn/misc/homebrew-install.sh)"
fi

# 安装Docker Desktop
echo "📦 安装Docker Desktop..."
if ! command -v docker &> /dev/null; then
    echo "正在通过Homebrew安装Docker..."
    brew install --cask docker
    echo "✅ Docker Desktop安装完成"
    echo "⚠️  请手动启动Docker Desktop应用程序"
    echo "   1. 在应用程序文件夹中找到Docker"
    echo "   2. 双击启动Docker Desktop"
    echo "   3. 等待Docker启动完成（状态栏显示Docker图标）"
    echo "   4. 然后重新运行此脚本"
    exit 1
else
    echo "✅ Docker已安装"
fi

# 检查Docker是否运行
echo "🔍 检查Docker服务状态..."
if ! docker info &> /dev/null; then
    echo "❌ Docker未运行，请先启动Docker Desktop"
    echo "   启动后重新运行此脚本"
    exit 1
fi

echo "✅ Docker服务正常运行"

# 停止现有容器
echo "🧹 清理现有容器..."
docker stop sqlbot dataease-sqlbot 2>/dev/null || true
docker rm sqlbot dataease-sqlbot 2>/dev/null || true

# 拉取官方镜像
echo "📥 拉取官方DataEase SQLBot镜像..."
docker pull dataease/sqlbot:latest

# 启动官方SQLBot
echo "🚀 启动官方DataEase SQLBot..."
docker run -d \
    --name dataease-sqlbot \
    -p 8080:8080 \
    -e DB_HOST=47.115.38.118 \
    -e DB_PORT=9024 \
    -e DB_NAME=GW_Course \
    -e DB_USER=postgres \
    -e DB_PASSWORD=postgres \
    -e OPENAI_API_KEY=sk-kimi-k2-0711-preview \
    -e OPENAI_BASE_URL=https://api.moonshot.cn/v1 \
    -e MODEL_NAME=kimi-k2-0711-preview \
    dataease/sqlbot:latest

# 等待启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查容器状态
if docker ps | grep -q dataease-sqlbot; then
    echo "✅ 官方DataEase SQLBot启动成功！"
    echo ""
    echo "🌐 访问地址: http://localhost:8080"
    echo "📊 数据库: 47.115.38.118:9024/GW_Course"
    echo "🤖 AI模型: kimi-k2-0711-preview"
    echo ""
    echo "🔍 容器状态:"
    docker ps | grep dataease-sqlbot
    echo ""
    echo "📋 查看日志: docker logs dataease-sqlbot"
    echo "🛑 停止服务: docker stop dataease-sqlbot"
else
    echo "❌ 启动失败，查看日志:"
    docker logs dataease-sqlbot
fi