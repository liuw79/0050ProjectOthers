#!/bin/bash

echo "🚨 紧急修复 DataEase SQLBot 连接问题"
echo "===================================="

# 1. 强制清理所有相关容器和进程
echo "1. 清理所有相关服务..."
docker stop $(docker ps -aq) 2>/dev/null
docker rm $(docker ps -aq --filter "name=sqlbot") 2>/dev/null
docker rm $(docker ps -aq --filter "name=dataease") 2>/dev/null

# 清理端口占用
sudo lsof -ti :8080 | xargs sudo kill -9 2>/dev/null
sudo lsof -ti :8004 | xargs sudo kill -9 2>/dev/null

echo "2. 创建数据目录..."
mkdir -p data/sqlbot/{logs,excel,images}
chmod -R 755 data/

echo "3. 重新部署 DataEase SQLBot..."
# 使用最简单的配置重新部署
docker run -d \
  --name dataease-sqlbot-fix \
  --restart unless-stopped \
  -p 8080:8080 \
  -v $(pwd)/data/sqlbot:/opt/dataease/data \
  -e DB_HOST=47.115.38.118 \
  -e DB_PORT=9024 \
  -e DB_USER=gw_reader \
  -e DB_PASSWORD=cZ1cM5nX5eX7 \
  -e DB_NAME=GW_Course \
  -e OPENAI_API_KEY=sk-22XL5TLeclRZyzj3lVAY0UYLy1S1NJJO45cKWTzWljMQDK8R \
  -e OPENAI_BASE_URL=https://api.moonshot.cn/v1 \
  -e MODEL_NAME=kimi-k2-0711-preview \
  dataease/sqlbot:latest

echo "4. 等待容器启动..."
sleep 30

echo "5. 检查容器状态..."
docker ps | grep dataease-sqlbot-fix

echo "6. 检查容器日志..."
docker logs --tail 10 dataease-sqlbot-fix

echo "7. 测试端口连接..."
if nc -z localhost 8080 2>/dev/null; then
    echo "✅ 8080端口正在监听"
else
    echo "❌ 8080端口仍未监听"
    echo "容器详细日志："
    docker logs dataease-sqlbot-fix
fi

echo ""
echo "🌐 请尝试访问: http://localhost:8080"
echo "如果仍有问题，请查看容器日志: docker logs dataease-sqlbot-fix"