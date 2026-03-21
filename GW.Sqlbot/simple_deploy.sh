#!/bin/bash

echo "🔧 简化部署 DataEase SQLBot"
echo "=========================="

# 停止所有相关容器
echo "停止现有容器..."
docker stop $(docker ps -q) 2>/dev/null
docker rm $(docker ps -aq --filter "name=sqlbot") 2>/dev/null
docker rm $(docker ps -aq --filter "name=dataease") 2>/dev/null

# 使用最简单的方式部署
echo "启动新容器..."
docker run -d \
  --name sqlbot-simple \
  -p 8080:8080 \
  -e DB_HOST=47.115.38.118 \
  -e DB_PORT=9024 \
  -e DB_USER=gw_reader \
  -e DB_PASSWORD=cZ1cM5nX5eX7 \
  -e DB_NAME=GW_Course \
  dataease/sqlbot:latest

echo "等待启动..."
sleep 20

echo "检查状态..."
docker ps | grep sqlbot-simple

echo "检查端口..."
netstat -tlnp | grep :8080 2>/dev/null || lsof -i :8080

echo ""
echo "✅ 部署完成"
echo "🌐 访问: http://localhost:8080"