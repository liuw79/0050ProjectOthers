#!/bin/bash

# DataEase SQLBot 部署脚本
echo "🚀 开始部署 DataEase SQLBot..."

# 停止并删除已存在的容器
echo "📦 停止并删除已存在的SQLBot容器..."
docker stop sqlbot 2>/dev/null || true
docker rm sqlbot 2>/dev/null || true

# 创建数据目录
echo "📁 创建数据目录..."
mkdir -p ./data/sqlbot/excel
mkdir -p ./data/sqlbot/file
mkdir -p ./data/sqlbot/images
mkdir -p ./data/sqlbot/logs
mkdir -p ./data/postgresql

# 设置目录权限
chmod -R 755 ./data

# 部署 DataEase SQLBot
echo "🐳 启动 DataEase SQLBot 容器..."
docker run -d \
  --name sqlbot \
  --restart unless-stopped \
  -p 8000:8000 \
  -p 8001:8001 \
  -v $(pwd)/data/sqlbot/excel:/opt/sqlbot/data/excel \
  -v $(pwd)/data/sqlbot/file:/opt/sqlbot/data/file \
  -v $(pwd)/data/sqlbot/images:/opt/sqlbot/images \
  -v $(pwd)/data/sqlbot/logs:/opt/sqlbot/app/logs \
  -v $(pwd)/data/postgresql:/var/lib/postgresql/data \
  --privileged=true \
  dataease/sqlbot

# 等待容器启动
echo "⏳ 等待容器启动..."
sleep 30

# 检查容器状态
echo "🔍 检查容器状态..."
docker ps | grep sqlbot

echo "✅ DataEase SQLBot 部署完成！"
echo "🌐 访问地址: http://localhost:8000"
echo "👤 默认用户名: admin"
echo "🔑 默认密码: SQLBot@123456"
echo ""
echo "📝 接下来需要："
echo "1. 在浏览器中访问 http://localhost:8000"
echo "2. 使用默认账号登录"
echo "3. 配置数据源连接到 GW_Course 数据库"
echo "4. 配置 Kimi K2 AI 模型"