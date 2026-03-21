#!/bin/bash

# Rustdesk 一键部署脚本
# 适用于已有 Docker 环境的服务器

set -e  # 遇到错误立即退出

SERVER_IP="op.gaowei.com"
RUSTDESK_DIR="/opt/rustdesk"

echo "=== Rustdesk 中继服务器一键部署 ==="
echo "服务器: $SERVER_IP"
echo "安装目录: $RUSTDESKDIR"
echo

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: Docker 未安装"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "警告: docker-compose 未安装，尝试安装..."
    curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# 检查端口冲突
echo "检查端口使用情况..."
PORTS=(21115 21116 21117 21119)
for port in "${PORTS[@]}"; do
    if netstat -tlnp | grep ":$port " > /dev/null; then
        echo "警告: 端口 $port 已被占用"
        netstat -tlnp | grep ":$port "
        read -p "是否继续部署? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
done

# 创建安装目录
echo "创建安装目录..."
mkdir -p $RUSTDESK_DIR
cd $RUSTDESK_DIR

# 备份现有配置
if [ -f "docker-compose.yml" ]; then
    echo "备份现有配置..."
    cp docker-compose.yml docker-compose.yml.backup.$(date +%Y%m%d_%H%M%S)
fi

# 创建 docker-compose.yml
echo "创建 Docker Compose 配置..."
cat > docker-compose.yml << EOF
version: '3.8'

services:
  hbbs:
    container_name: rustdesk-hbbs
    ports:
      - "21115:21115"
      - "21116:21116"
      - "21116:21116/udp"
    image: rustdesk/rustdesk-server:latest
    command: hbbs -r $SERVER_IP:21117
    volumes:
      - ./data:/root
    networks:
      - rustdesk-net
    depends_on:
      - hbbr
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  hbbr:
    container_name: rustdesk-hbbr
    ports:
      - "21117:21117"
      - "21119:21119"
    image: rustdesk/rustdesk-server:latest
    command: hbbr
    volumes:
      - ./data:/root
    networks:
      - rustdesk-net
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

networks:
  rustdesk-net:
    driver: bridge
EOF

# 创建数据目录
mkdir -p data

# 拉取镜像
echo "拉取 Docker 镜像..."
docker-compose pull

# 启动服务
echo "启动 Rustdesk 服务..."
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
    if netstat -tlnp | grep ":$port " > /dev/null; then
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
    echo "服务器地址: $SERVER_IP"
    echo "信令服务器端口: 21115"
    echo "中继服务器端口: 21117"
    echo
    echo "公钥内容 (客户端配置需要):"
    echo "----------------------------------------"
    cat data/id_ed25519.pub
    echo "----------------------------------------"
    echo
    echo "客户端配置:"
    echo "1. ID服务器: $SERVER_IP:21115"
    echo "2. 中继服务器: $SERVER_IP:21117"
    echo "3. 公钥: 上面显示的内容"
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