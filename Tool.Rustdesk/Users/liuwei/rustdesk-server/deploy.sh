#!/bin/bash

# RustDesk本地中继服务器部署脚本

set -e  # 遇到错误立即退出

RUSTDESK_DIR="/Users/liuwei/rustdesk-server"

echo "=== RustDesk 中继服务器本地部署 ==="
echo "安装目录: $RUSTDESK_DIR"
echo

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: Docker 未安装"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "错误: docker-compose 未安装"
    exit 1
fi

# 检查端口冲突
echo "检查端口使用情况..."
PORTS=(21115 21116 21117 21119)
for port in "${PORTS[@]}"; do
    if netstat -an | grep "LISTEN" | grep -q ".$port "; then
        echo "警告: 端口 $port 已被占用"
        netstat -an | grep "LISTEN" | grep ".$port "
        read -p "是否继续部署? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
done

# 进入安装目录
cd $RUSTDESK_DIR

# 创建数据目录
mkdir -p data

# 拉取镜像
echo "拉取 Docker 镜像..."
docker-compose pull

# 启动服务
echo "启动 RustDesk 服务..."
docker-compose up -d

# 等待服务启动
echo "等待服务启动..."
sleep 15

# 检查服务状态
echo "检查服务状态..."
docker-compose ps

# 检查端口监听
echo "检查端口监听状态..."
for port in "${PORTS[@]}"; do
    if netstat -an | grep "LISTEN" | grep -q ".$port "; then
        echo "✓ 端口 $port 正常监听"
    else
        echo "✗ 端口 $port 未监听"
    fi
done

# 等待密钥生成
echo "等待密钥生成..."
sleep 5

# 显示公钥
if [ -f "data/id_ed25519.pub" ]; then
    echo
    echo "=== 部署成功! ==="
    echo "服务器地址: localhost"
    echo "信令服务器端口: 21115"
    echo "中继服务器端口: 21117"
    echo
    echo "公钥内容 (客户端配置需要):"
    echo "----------------------------------------"
    cat data/id_ed25519.pub
    echo "----------------------------------------"
    echo
    echo "客户端配置:"
    echo "1. ID服务器: localhost:21115"
    echo "2. 中继服务器: localhost:21117"
    echo "3. 公钥: 上面显示的内容"
    echo
    echo "注意: 如果需要从其他设备连接，请使用本机IP地址替换localhost"
    echo "本机IP地址:"
    ifconfig | grep "inet " | grep -v 127.0.0.1
    echo
else
    echo "警告: 公钥文件未生成，请检查服务日志"
    echo "查看日志命令: docker-compose logs"
fi

echo
echo "常用管理命令:"
echo "查看状态: docker-compose ps"
echo "查看日志: docker-compose logs -f"
echo "重启服务: docker-compose restart"
echo "停止服务: docker-compose down"
echo "更新服务: docker-compose pull && docker-compose up -d"
echo
echo "部署完成!"