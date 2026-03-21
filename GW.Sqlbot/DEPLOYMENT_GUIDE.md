# SQLBot 远程服务器部署指南

## 概述

本指南详细说明如何将 SQLBot 部署到远程 Linux 服务器（Ubuntu/CentOS）上，包括完整的生产环境配置、安全设置和监控。

## 系统要求

### 服务器配置
- **操作系统**: Ubuntu 18.04+ 或 CentOS 7+
- **内存**: 最低 2GB，推荐 4GB+
- **存储**: 最低 20GB 可用空间
- **CPU**: 最低 2 核心
- **网络**: 公网 IP 地址

### 软件依赖
- Python 3.8+
- Nginx
- systemd
- Git
- 防火墙 (UFW/firewalld)

## 部署步骤

### 1. 准备部署文件

将以下文件上传到服务器的 `/tmp` 目录：

```bash
# 在本地打包部署文件
tar -czf sqlbot-deploy.tar.gz \
    deploy_remote.sh \
    setup_security.sh \
    sqlbot.service \
    nginx_sqlbot.conf \
    start_sqlbot.py \
    config/.env

# 上传到服务器
scp sqlbot-deploy.tar.gz user@your-server:/tmp/
```

### 2. 服务器初始部署

```bash
# 登录服务器
ssh user@your-server

# 切换到 root 用户
sudo su -

# 解压部署文件
cd /tmp
tar -xzf sqlbot-deploy.tar.gz

# 执行基础部署
chmod +x deploy_remote.sh
./deploy_remote.sh
```

### 3. 安全配置和服务启动

```bash
# 执行安全配置
chmod +x setup_security.sh
./setup_security.sh
```

### 4. 配置域名和 SSL（可选）

#### 4.1 配置域名解析
将您的域名 A 记录指向服务器 IP 地址。

#### 4.2 获取 Let's Encrypt 证书
```bash
# 安装 certbot
apt install certbot python3-certbot-nginx  # Ubuntu
yum install certbot python3-certbot-nginx  # CentOS

# 获取证书
certbot --nginx -d your-domain.com

# 自动续期
echo "0 12 * * * /usr/bin/certbot renew --quiet" | crontab -
```

#### 4.3 更新 Nginx 配置
编辑 `/etc/nginx/sites-available/sqlbot`，将 `your-domain.com` 替换为实际域名。

## 配置说明

### 环境变量配置

编辑 `/opt/sqlbot/config/.env` 文件：

```bash
# 服务配置
SERVICE_PORT=8004
SERVICE_HOST=0.0.0.0
DEBUG=False
ENVIRONMENT=production

# 数据库配置
DB_HOST=47.115.38.118
DB_PORT=9024
DB_NAME=GW_Course
DB_USER=gw_reader
DB_PASSWORD=gw_reader

# AI 模型配置
OPENAI_API_KEY=your_actual_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-3.5-turbo

# 安全配置
SECRET_KEY=your_generated_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
```

### 防火墙配置

默认开放的端口：
- **22**: SSH
- **80**: HTTP (重定向到 HTTPS)
- **443**: HTTPS
- **8004**: SQLBot 应用 (仅本地访问)

## 服务管理

### 基本命令

```bash
# 查看服务状态
systemctl status sqlbot

# 启动服务
systemctl start sqlbot

# 停止服务
systemctl stop sqlbot

# 重启服务
systemctl restart sqlbot

# 查看日志
journalctl -u sqlbot -f

# 查看应用日志
tail -f /opt/sqlbot/logs/sqlbot.log
```

### Nginx 管理

```bash
# 测试配置
nginx -t

# 重新加载配置
systemctl reload nginx

# 查看 Nginx 状态
systemctl status nginx

# 查看访问日志
tail -f /var/log/nginx/sqlbot_access.log

# 查看错误日志
tail -f /var/log/nginx/sqlbot_error.log
```

## 监控和维护

### 自动监控

系统已配置自动监控脚本 `/opt/sqlbot/monitor.sh`，每 5 分钟检查一次服务状态。

### 手动健康检查

```bash
# 本地健康检查
curl http://localhost:8004/health

# 外部健康检查
curl https://your-domain.com/health
```

### 日志管理

- **应用日志**: `/opt/sqlbot/logs/sqlbot.log`
- **监控日志**: `/opt/sqlbot/logs/monitor.log`
- **Nginx 日志**: `/var/log/nginx/sqlbot_*.log`
- **系统日志**: `journalctl -u sqlbot`

日志自动轮转配置已启用，保留 30 天历史记录。

### 备份策略

```bash
# 创建备份脚本
cat > /opt/sqlbot/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/sqlbot/backup"
DATE=$(date +%Y%m%d_%H%M%S)

# 备份配置文件
tar -czf $BACKUP_DIR/config_$DATE.tar.gz /opt/sqlbot/config/

# 备份日志
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz /opt/sqlbot/logs/

# 清理 7 天前的备份
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
EOF

chmod +x /opt/sqlbot/backup.sh

# 添加到定时任务 (每天凌晨 2 点)
echo "0 2 * * * /opt/sqlbot/backup.sh" | crontab -
```

## 性能优化

### 系统优化

```bash
# 增加文件描述符限制
echo "sqlbot soft nofile 65536" >> /etc/security/limits.conf
echo "sqlbot hard nofile 65536" >> /etc/security/limits.conf

# 优化内核参数
cat >> /etc/sysctl.conf << EOF
net.core.somaxconn = 1024
net.ipv4.tcp_max_syn_backlog = 1024
net.ipv4.ip_local_port_range = 1024 65535
EOF

sysctl -p
```

### 应用优化

如需要处理高并发，可以配置多个应用实例：

```bash
# 复制服务文件
cp /etc/systemd/system/sqlbot.service /etc/systemd/system/sqlbot@.service

# 修改端口配置
sed -i 's/8004/800%i/g' /etc/systemd/system/sqlbot@.service

# 启动多个实例
systemctl start sqlbot@4
systemctl start sqlbot@5

# 更新 Nginx upstream 配置
```

## 故障排除

### 常见问题

1. **服务无法启动**
   ```bash
   # 检查日志
   journalctl -u sqlbot -n 50
   
   # 检查配置文件
   python3 /opt/sqlbot/start_sqlbot.py --check-config
   ```

2. **数据库连接失败**
   ```bash
   # 测试数据库连接
   telnet 47.115.38.118 9024
   
   # 检查防火墙规则
   iptables -L
   ```

3. **Nginx 502 错误**
   ```bash
   # 检查应用是否运行
   netstat -tlnp | grep 8004
   
   # 检查 Nginx 配置
   nginx -t
   ```

4. **SSL 证书问题**
   ```bash
   # 检查证书有效期
   openssl x509 -in /etc/ssl/certs/sqlbot.crt -text -noout
   
   # 重新生成证书
   /opt/sqlbot/setup_security.sh
   ```

### 日志分析

```bash
# 查看错误日志
grep -i error /opt/sqlbot/logs/sqlbot.log

# 查看访问统计
awk '{print $1}' /var/log/nginx/sqlbot_access.log | sort | uniq -c | sort -nr

# 监控资源使用
htop
iostat -x 1
```

## 安全注意事项

1. **定期更新系统**
   ```bash
   apt update && apt upgrade  # Ubuntu
   yum update                 # CentOS
   ```

2. **配置 SSH 密钥认证**
   ```bash
   # 禁用密码登录
   sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
   systemctl restart sshd
   ```

3. **配置 fail2ban**
   ```bash
   apt install fail2ban
   systemctl enable fail2ban
   systemctl start fail2ban
   ```

4. **定期检查日志**
   ```bash
   # 检查登录日志
   last -n 20
   
   # 检查认证日志
   grep "authentication failure" /var/log/auth.log
   ```

## 访问地址

部署完成后，可通过以下地址访问：

- **本地访问**: `http://localhost:8004`
- **外部访问**: `https://your-domain.com`
- **健康检查**: `https://your-domain.com/health`
- **API 接口**: `https://your-domain.com/api/query`

## 技术支持

如遇到问题，请检查：

1. 系统日志: `journalctl -u sqlbot -f`
2. 应用日志: `/opt/sqlbot/logs/sqlbot.log`
3. Nginx 日志: `/var/log/nginx/sqlbot_error.log`
4. 监控日志: `/opt/sqlbot/logs/monitor.log`

---

**注意**: 请根据实际环境调整配置参数，特别是域名、数据库连接信息和 API 密钥。