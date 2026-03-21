#!/bin/bash

echo "🔍 DataEase SQLBot 服务状态检查"
echo "================================"

# 1. 检查Docker是否运行
echo "1. 检查Docker服务..."
if command -v docker &> /dev/null; then
    echo "✅ Docker已安装"
    if docker info &> /dev/null; then
        echo "✅ Docker服务正在运行"
    else
        echo "❌ Docker服务未运行，请启动Docker"
        exit 1
    fi
else
    echo "❌ Docker未安装"
    exit 1
fi

# 2. 检查容器状态
echo ""
echo "2. 检查容器状态..."
CONTAINERS=$(docker ps -a --filter "name=sqlbot" --filter "name=dataease" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}")
if [ -n "$CONTAINERS" ]; then
    echo "$CONTAINERS"
else
    echo "❌ 未找到相关容器"
fi

# 3. 检查端口占用
echo ""
echo "3. 检查端口占用..."
echo "8004端口:"
lsof -i :8004 2>/dev/null || echo "  未被占用"
echo "8080端口:"
lsof -i :8080 2>/dev/null || echo "  未被占用"

# 4. 检查网络连接
echo ""
echo "4. 测试本地访问..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8080 2>/dev/null | grep -q "200\|302\|404"; then
    echo "✅ 8080端口可访问"
else
    echo "❌ 8080端口无响应"
fi

# 5. 显示修复建议
echo ""
echo "🔧 修复建议:"
echo "如果服务未运行，请执行以下命令之一："
echo "  ./quick_fix.sh          # 快速修复"
echo "  ./diagnose_and_fix.sh   # 完整诊断修复"
echo ""
echo "如果容器存在但未运行，尝试："
echo "  docker start <容器名>"
echo ""
echo "如果需要重新部署："
echo "  docker run -d --name dataease-sqlbot -p 8080:8080 \\"
echo "    -e DB_HOST=47.115.38.118 -e DB_PORT=9024 \\"
echo "    -e DB_USER=gw_reader -e DB_PASSWORD=cZ1cM5nX5eX7 \\"
echo "    -e DB_NAME=GW_Course dataease/sqlbot:latest"