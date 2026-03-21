#!/bin/bash

cd "$(dirname "$0")"

echo "======================================"
echo "N8N 环境检查"
echo "======================================"
echo ""

# 检查 Docker
echo "1️⃣  检查 Docker 安装..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    echo "   ✅ Docker 已安装: $DOCKER_VERSION"
else
    echo "   ❌ Docker 未安装"
    echo "   请访问 https://www.docker.com/products/docker-desktop 下载安装"
fi
echo ""

# 检查 Docker 运行状态
echo "2️⃣  检查 Docker 运行状态..."
if docker info &> /dev/null; then
    echo "   ✅ Docker 正在运行"
else
    echo "   ❌ Docker 未运行，请启动 Docker Desktop"
fi
echo ""

# 检查配置文件
echo "3️⃣  检查配置文件..."
if [ -f .env ]; then
    echo "   ✅ .env 配置文件存在"
else
    echo "   ❌ .env 配置文件不存在"
fi

if [ -f docker-compose.yml ]; then
    echo "   ✅ docker-compose.yml 存在"
else
    echo "   ❌ docker-compose.yml 不存在"
fi
echo ""

# 检查 N8N 容器状态
echo "4️⃣  检查 N8N 服务状态..."
if docker ps | grep -q n8n; then
    echo "   ✅ N8N 服务正在运行"
    echo "   访问地址: http://localhost:5678"
    echo ""
    echo "   容器信息:"
    docker ps --filter "name=n8n" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
else
    if docker ps -a | grep -q n8n; then
        echo "   ⚠️  N8N 容器存在但未运行"
        echo "   使用 './启动N8N.command' 启动服务"
    else
        echo "   ℹ️  N8N 服务未启动"
        echo "   使用 './启动N8N.command' 启动服务"
    fi
fi
echo ""

# 检查端口占用
echo "5️⃣  检查端口 5678..."
if lsof -Pi :5678 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "   ⚠️  端口 5678 已被占用"
    echo "   占用进程:"
    lsof -i :5678
else
    echo "   ✅ 端口 5678 可用"
fi
echo ""

# 检查数据目录
echo "6️⃣  检查数据目录..."
if [ -d n8n_data ]; then
    DATA_SIZE=$(du -sh n8n_data 2>/dev/null | cut -f1)
    echo "   ✅ 数据目录存在 (大小: $DATA_SIZE)"
else
    echo "   ℹ️  数据目录不存在（首次运行时会自动创建）"
fi
echo ""

echo "======================================"
echo "环境检查完成！"
echo "======================================"
echo ""
echo "按回车键退出..."
read


