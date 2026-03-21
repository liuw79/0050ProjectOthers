#!/bin/bash

echo "🔧 快速修复 DataEase SQLBot 访问问题"

# 强制清理所有相关进程和容器
echo "1. 强制清理所有相关服务..."

# 杀死8004和8080端口的所有进程
sudo lsof -ti :8004 | xargs sudo kill -9 2>/dev/null
sudo lsof -ti :8080 | xargs sudo kill -9 2>/dev/null

# 停止并删除所有相关Docker容器
docker stop $(docker ps -aq) 2>/dev/null
docker rm $(docker ps -aq --filter "name=sqlbot") 2>/dev/null
docker rm $(docker ps -aq --filter "name=dataease") 2>/dev/null

echo "2. 重新部署 DataEase SQLBot..."

# 使用简化的Docker命令重新部署
docker run -d \
  --name dataease-sqlbot-new \
  --restart unless-stopped \
  -p 8080:8080 \
  -e DB_HOST=47.115.38.118 \
  -e DB_PORT=9024 \
  -e DB_USER=gw_reader \
  -e DB_PASSWORD=cZ1cM5nX5eX7 \
  -e DB_NAME=GW_Course \
  dataease/sqlbot:latest

echo "3. 等待服务启动..."
sleep 20

echo "4. 检查服务状态..."
docker ps | grep dataease-sqlbot-new

echo "5. 检查端口监听..."
netstat -tlnp | grep :8080 || lsof -i :8080

echo ""
echo "✅ 修复完成！"
echo "🌐 访问地址: http://localhost:8080"
echo "📋 如果仍有问题，请运行: docker logs dataease-sqlbot-new"