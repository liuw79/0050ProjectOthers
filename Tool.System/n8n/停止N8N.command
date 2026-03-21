#!/bin/bash

# 获取脚本所在目录
cd "$(dirname "$0")"

echo "======================================"
echo "停止 N8N 服务"
echo "======================================"
echo ""

# 检查 Docker 是否运行
if ! docker info &> /dev/null; then
    echo "❌ Docker 未运行"
    exit 1
fi

echo "🛑 正在停止 N8N..."
docker-compose down

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ N8N 已成功停止"
else
    echo ""
    echo "❌ 停止失败"
fi

echo ""
echo "按回车键退出..."
read


