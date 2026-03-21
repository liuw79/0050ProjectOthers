#!/bin/bash

# 获取脚本所在目录
cd "$(dirname "$0")"

echo "======================================"
echo "查看 N8N 日志"
echo "======================================"
echo "按 Ctrl+C 退出日志查看"
echo ""

# 显示日志（实时跟踪）
docker-compose logs -f n8n


