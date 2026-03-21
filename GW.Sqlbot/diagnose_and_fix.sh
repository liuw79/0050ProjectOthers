#!/bin/bash

echo "=== DataEase SQLBot 诊断和修复脚本 ==="

# 1. 检查8004端口（之前的简化版服务）
echo "1. 检查8004端口使用情况..."
lsof -i :8004 2>/dev/null || echo "8004端口未被占用"

# 2. 检查8080端口（DataEase SQLBot）
echo "2. 检查8080端口使用情况..."
lsof -i :8080 2>/dev/null || echo "8080端口未被占用"

# 3. 检查所有Python进程（可能的残留服务）
echo "3. 检查Python进程..."
ps aux | grep python | grep -v grep || echo "无Python进程运行"

# 4. 检查Docker容器状态
echo "4. 检查Docker容器状态..."
docker ps -a | grep -E "(sqlbot|dataease)" || echo "无相关Docker容器"

# 5. 停止可能的残留服务
echo "5. 清理残留服务..."

# 停止8004端口的进程
echo "停止8004端口进程..."
lsof -ti :8004 | xargs kill -9 2>/dev/null || echo "8004端口无进程需要停止"

# 停止8080端口的进程
echo "停止8080端口进程..."
lsof -ti :8080 | xargs kill -9 2>/dev/null || echo "8080端口无进程需要停止"

# 停止所有相关Docker容器
echo "停止相关Docker容器..."
docker stop $(docker ps -q --filter "ancestor=dataease/sqlbot") 2>/dev/null || echo "无DataEase容器需要停止"
docker rm $(docker ps -aq --filter "ancestor=dataease/sqlbot") 2>/dev/null || echo "无DataEase容器需要删除"

# 6. 重新部署DataEase SQLBot
echo "6. 重新部署DataEase SQLBot..."

# 创建数据目录
mkdir -p data/sqlbot/{logs,excel,images}
chmod 755 data/sqlbot data/sqlbot/*

# 使用国内镜像重新部署
echo "使用阿里云镜像部署DataEase SQLBot..."
docker run -d \
  --name dataease-sqlbot \
  --restart unless-stopped \
  -p 8080:8080 \
  -v $(pwd)/data/sqlbot:/opt/dataease/data \
  -v $(pwd)/config/.env:/opt/dataease/config/.env \
  -e DB_HOST=47.115.38.118 \
  -e DB_PORT=9024 \
  -e DB_USER=gw_reader \
  -e DB_PASSWORD=cZ1cM5nX5eX7 \
  -e DB_NAME=GW_Course \
  -e OPENAI_API_KEY=sk-22XL5TLeclRZyzj3lVAY0UYLy1S1NJJO45cKWTzWljMQDK8R \
  -e OPENAI_BASE_URL=https://api.moonshot.cn/v1 \
  -e MODEL_NAME=kimi-k2-0711-preview \
  registry.cn-hangzhou.aliyuncs.com/dataease/sqlbot:latest 2>/dev/null || \
docker run -d \
  --name dataease-sqlbot \
  --restart unless-stopped \
  -p 8080:8080 \
  -v $(pwd)/data/sqlbot:/opt/dataease/data \
  -v $(pwd)/config/.env:/opt/dataease/config/.env \
  -e DB_HOST=47.115.38.118 \
  -e DB_PORT=9024 \
  -e DB_USER=gw_reader \
  -e DB_PASSWORD=cZ1cM5nX5eX7 \
  -e DB_NAME=GW_Course \
  -e OPENAI_API_KEY=sk-22XL5TLeclRZyzj3lVAY0UYLy1S1NJJO45cKWTzWljMQDK8R \
  -e OPENAI_BASE_URL=https://api.moonshot.cn/v1 \
  -e MODEL_NAME=kimi-k2-0711-preview \
  dataease/sqlbot:latest

# 7. 等待容器启动
echo "7. 等待容器启动..."
sleep 15

# 8. 检查部署结果
echo "8. 检查部署结果..."
docker ps | grep dataease-sqlbot && echo "✅ 容器启动成功" || echo "❌ 容器启动失败"

# 9. 检查端口监听
echo "9. 检查端口监听..."
lsof -i :8080 && echo "✅ 8080端口正常监听" || echo "❌ 8080端口未监听"

# 10. 显示访问信息
echo ""
echo "=== 部署完成 ==="
echo "访问地址: http://localhost:8080"
echo "如果仍无法访问，请检查："
echo "1. 防火墙设置"
echo "2. Docker容器日志: docker logs dataease-sqlbot"
echo "3. 网络连接"

# 11. 显示容器日志
echo ""
echo "=== 容器启动日志 ==="
docker logs --tail 10 dataease-sqlbot 2>/dev/null || echo "无法获取容器日志"