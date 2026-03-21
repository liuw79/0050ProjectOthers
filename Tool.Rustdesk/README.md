# RustDesk 中继服务器部署工具

## 概述
本项目用于在服务器 `op.gaowei.com` 上部署 RustDesk 中继服务器。

## 快速部署

### 方法一：一键部署（推荐）
```bash
# 上传脚本
scp quick_deploy.sh root@op.gaowei.com:/tmp/

# 连接服务器并执行
ssh root@op.gaowei.com
chmod +x /tmp/quick_deploy.sh
/tmp/quick_deploy.sh
```

### 方法二：Windows批处理
双击运行 `upload_and_deploy.bat`

## 端口分配
- 21115: hbbs TCP (信令服务器)
- 21116: hbbs TCP/UDP (NAT类型测试) 
- 21117: hbbr TCP (中继服务器)
- 21119: hbbr TCP (中继服务器)

### 4. 手动部署 (如果脚本失败)

#### 创建目录
```bash
mkdir -p /opt/rustdesk
cd /opt/rustdesk
```

#### 创建 docker-compose.yml
```yaml
version: '3'

services:
  hbbs:
    container_name: hbbs
    ports:
      - 21115:21115
      - 21116:21116
      - 21116:21116/udp
    image: rustdesk/rustdesk-server:latest
    command: hbbs -r op.gaowei.com:21117
    volumes:
      - ./data:/root
    networks:
      - rustdesk-net
    depends_on:
      - hbbr
    restart: unless-stopped

  hbbr:
    container_name: hbbr
    ports:
      - 21117:21117
      - 21119:21119
    image: rustdesk/rustdesk-server:latest
    command: hbbr
    volumes:
      - ./data:/root
    networks:
      - rustdesk-net
    restart: unless-stopped

networks:
  rustdesk-net:
    external: false
```

#### 启动服务
```bash
mkdir -p data
docker-compose up -d
```

## 验证部署

### 检查容器状态
```bash
docker-compose ps
```

### 检查端口监听
```bash
netstat -tlnp | grep -E ':(21115|21116|21117|21119)'
```

### 获取公钥
```bash
cat /opt/rustdesk/data/id_ed25519.pub
```

## 客户端配置

1. 在 Rustdesk 客户端中点击 "网络" -> "ID服务器"
2. 输入服务器地址: `op.gaowei.com:21115`
3. 输入中继服务器: `op.gaowei.com:21117`
4. 输入公钥 (从上面获取的内容)
5. 点击 "应用"

## 防火墙配置

如果服务器有防火墙，需要开放以下端口:
```bash
# UFW
sudo ufw allow 21115
sudo ufw allow 21116
sudo ufw allow 21117
sudo ufw allow 21119

# iptables
iptables -A INPUT -p tcp --dport 21115 -j ACCEPT
iptables -A INPUT -p tcp --dport 21116 -j ACCEPT
iptables -A INPUT -p udp --dport 21116 -j ACCEPT
iptables -A INPUT -p tcp --dport 21117 -j ACCEPT
iptables -A INPUT -p tcp --dport 21119 -j ACCEPT
```

## 故障排除

### 查看日志
```bash
cd /opt/rustdesk
docker-compose logs -f
```

### 重启服务
```bash
docker-compose restart
```

### 停止服务
```bash
docker-compose down
```

## 注意事项

1. 确保服务器防火墙已开放相应端口
2. 如果使用域名，确保DNS解析正确
3. 定期备份 `/opt/rustdesk/data` 目录中的密钥文件
4. 监控服务状态，确保服务正常运行

## 维护命令

```bash
# 查看服务状态
docker-compose ps

# 查看资源使用
docker stats

# 更新镜像
docker-compose pull
docker-compose up -d

# 清理未使用的镜像
docker image prune
```