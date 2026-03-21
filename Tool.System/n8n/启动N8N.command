#!/bin/bash

# 获取脚本所在目录
cd "$(dirname "$0")"

echo "======================================"
echo "启动 N8N 工作流自动化平台"
echo "======================================"
echo ""

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: 未检测到 Docker"
    echo "请先安装 Docker Desktop for Mac"
    echo "下载地址: https://www.docker.com/products/docker-desktop"
    echo ""
    read -p "按回车键退出..."
    exit 1
fi

# 检查 Docker 是否运行
if ! docker info &> /dev/null; then
    echo "❌ 错误: Docker 未运行"
    echo "请先启动 Docker Desktop"
    echo ""
    read -p "按回车键退出..."
    exit 1
fi

# 检查 .env 文件是否存在
if [ ! -f .env ]; then
    echo "⚠️  未找到 .env 文件，从示例文件创建..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ 已创建 .env 文件"
        echo "⚠️  请修改 .env 文件中的密码后重新运行"
        echo ""
        read -p "按回车键退出..."
        exit 1
    else
        echo "❌ 错误: 未找到 .env.example 文件"
        exit 1
    fi
fi

# 创建必要的目录
mkdir -p n8n_data
mkdir -p local_files

echo "🚀 正在启动 N8N..."
echo ""

# 启动 Docker Compose
docker-compose up -d

# 检查启动状态
if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✅ N8N 已成功启动！"
    echo "======================================"
    echo ""
    echo "访问地址: http://localhost:5678"
    echo ""
    echo "默认登录信息:"
    echo "  用户名: admin"
    echo "  密码: admin123"
    echo "  (请在 .env 文件中修改密码)"
    echo ""
    echo "查看日志: docker-compose logs -f n8n"
    echo "停止服务: docker-compose down"
    echo ""
    
    # 等待服务启动
    echo "等待服务启动..."
    sleep 5
    
    # 自动打开浏览器
    open http://localhost:5678
else
    echo ""
    echo "❌ 启动失败，请查看错误信息"
    echo ""
fi

echo "按回车键退出..."
read


