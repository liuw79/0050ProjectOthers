#!/bin/bash

# SQLBot 服务器安全配置脚本

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否为 root 用户
check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "此脚本需要 root 权限运行"
        exit 1
    fi
}

# 配置防火墙
setup_firewall() {
    log_info "配置防火墙规则..."
    
    # 检测防火墙类型
    if command -v ufw &> /dev/null; then
        # Ubuntu UFW
        log_info "使用 UFW 配置防火墙"
        
        # 重置防火墙规则
        ufw --force reset
        
        # 默认策略
        ufw default deny incoming
        ufw default allow outgoing
        
        # 允许 SSH
        ufw allow ssh
        ufw allow 22/tcp
        
        # 允许 HTTP/HTTPS
        ufw allow 80/tcp
        ufw allow 443/tcp
        
        # 允许 SQLBot 端口 (仅本地)
        ufw allow from 127.0.0.1 to any port 8004
        
        # 启用防火墙
        ufw --force enable
        
        log_info "UFW 防火墙配置完成"
        
    elif command -v firewall-cmd &> /dev/null; then
        # CentOS/RHEL firewalld
        log_info "使用 firewalld 配置防火墙"
        
        systemctl start firewalld
        systemctl enable firewalld
        
        # 添加服务
        firewall-cmd --permanent --add-service=ssh
        firewall-cmd --permanent --add-service=http
        firewall-cmd --permanent --add-service=https
        
        # 重新加载配置
        firewall-cmd --reload
        
        log_info "firewalld 防火墙配置完成"
    else
        log_warn "未检测到支持的防火墙，请手动配置"
    fi
}

# 配置 systemd 服务
setup_systemd_service() {
    log_info "配置 systemd 服务..."
    
    # 复制服务文件
    if [[ -f "/opt/sqlbot/sqlbot.service" ]]; then
        cp /opt/sqlbot/sqlbot.service /etc/systemd/system/
    else
        log_error "服务文件不存在: /opt/sqlbot/sqlbot.service"
        return 1
    fi
    
    # 重新加载 systemd
    systemctl daemon-reload
    
    # 启用服务
    systemctl enable sqlbot.service
    
    log_info "systemd 服务配置完成"
}

# 配置 Nginx
setup_nginx() {
    log_info "配置 Nginx..."
    
    # 检查 Nginx 是否安装
    if ! command -v nginx &> /dev/null; then
        log_error "Nginx 未安装"
        return 1
    fi
    
    # 复制配置文件
    if [[ -f "/opt/sqlbot/nginx_sqlbot.conf" ]]; then
        cp /opt/sqlbot/nginx_sqlbot.conf /etc/nginx/sites-available/sqlbot
        
        # 创建软链接
        ln -sf /etc/nginx/sites-available/sqlbot /etc/nginx/sites-enabled/
        
        # 删除默认站点 (如果存在)
        if [[ -f "/etc/nginx/sites-enabled/default" ]]; then
            rm -f /etc/nginx/sites-enabled/default
        fi
        
        # 测试配置
        nginx -t
        
        # 启用并启动 Nginx
        systemctl enable nginx
        systemctl restart nginx
        
        log_info "Nginx 配置完成"
    else
        log_error "Nginx 配置文件不存在"
        return 1
    fi
}

# 生成自签名 SSL 证书 (用于测试)
generate_ssl_cert() {
    log_info "生成自签名 SSL 证书..."
    
    SSL_DIR="/etc/ssl"
    CERT_DIR="$SSL_DIR/certs"
    KEY_DIR="$SSL_DIR/private"
    
    mkdir -p $CERT_DIR $KEY_DIR
    
    # 生成私钥
    openssl genrsa -out $KEY_DIR/sqlbot.key 2048
    
    # 生成证书
    openssl req -new -x509 -key $KEY_DIR/sqlbot.key -out $CERT_DIR/sqlbot.crt -days 365 -subj "/C=CN/ST=Beijing/L=Beijing/O=SQLBot/CN=localhost"
    
    # 设置权限
    chmod 600 $KEY_DIR/sqlbot.key
    chmod 644 $CERT_DIR/sqlbot.crt
    
    # 更新 Nginx 配置中的证书路径
    sed -i "s|/etc/ssl/certs/your-domain.crt|$CERT_DIR/sqlbot.crt|g" /etc/nginx/sites-available/sqlbot
    sed -i "s|/etc/ssl/private/your-domain.key|$KEY_DIR/sqlbot.key|g" /etc/nginx/sites-available/sqlbot
    
    log_info "SSL 证书生成完成"
}

# 配置日志轮转
setup_log_rotation() {
    log_info "配置日志轮转..."
    
    cat > /etc/logrotate.d/sqlbot << EOF
/opt/sqlbot/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 sqlbot sqlbot
    postrotate
        systemctl reload sqlbot || true
    endscript
}
EOF

    log_info "日志轮转配置完成"
}

# 创建监控脚本
create_monitoring_script() {
    log_info "创建监控脚本..."
    
    cat > /opt/sqlbot/monitor.sh << 'EOF'
#!/bin/bash

# SQLBot 监控脚本

SERVICE_NAME="sqlbot"
LOG_FILE="/opt/sqlbot/logs/monitor.log"
HEALTH_URL="http://localhost:8004/health"

log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> $LOG_FILE
}

check_service() {
    if systemctl is-active --quiet $SERVICE_NAME; then
        return 0
    else
        return 1
    fi
}

check_health() {
    if curl -s -f $HEALTH_URL > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

restart_service() {
    log_message "重启服务: $SERVICE_NAME"
    systemctl restart $SERVICE_NAME
    sleep 10
}

# 主监控逻辑
if ! check_service; then
    log_message "服务未运行，尝试启动"
    systemctl start $SERVICE_NAME
    sleep 5
fi

if ! check_health; then
    log_message "健康检查失败，尝试重启服务"
    restart_service
    
    if check_health; then
        log_message "服务重启成功"
    else
        log_message "服务重启失败，需要人工干预"
    fi
fi
EOF

    chmod +x /opt/sqlbot/monitor.sh
    chown sqlbot:sqlbot /opt/sqlbot/monitor.sh
    
    # 添加到 crontab
    (crontab -l 2>/dev/null; echo "*/5 * * * * /opt/sqlbot/monitor.sh") | crontab -
    
    log_info "监控脚本创建完成"
}

# 启动所有服务
start_services() {
    log_info "启动服务..."
    
    # 启动 SQLBot
    systemctl start sqlbot
    
    # 重启 Nginx
    systemctl restart nginx
    
    # 检查服务状态
    sleep 5
    
    if systemctl is-active --quiet sqlbot; then
        log_info "SQLBot 服务启动成功"
    else
        log_error "SQLBot 服务启动失败"
        systemctl status sqlbot
    fi
    
    if systemctl is-active --quiet nginx; then
        log_info "Nginx 服务启动成功"
    else
        log_error "Nginx 服务启动失败"
        systemctl status nginx
    fi
}

# 显示部署信息
show_deployment_info() {
    log_info "部署完成！"
    echo ""
    echo "=== SQLBot 部署信息 ==="
    echo "服务状态: $(systemctl is-active sqlbot)"
    echo "Nginx 状态: $(systemctl is-active nginx)"
    echo "本地访问: http://localhost:8004"
    echo "外部访问: https://your-domain.com (需要配置域名)"
    echo "健康检查: curl http://localhost:8004/health"
    echo ""
    echo "=== 管理命令 ==="
    echo "查看服务状态: systemctl status sqlbot"
    echo "查看日志: journalctl -u sqlbot -f"
    echo "重启服务: systemctl restart sqlbot"
    echo "停止服务: systemctl stop sqlbot"
    echo ""
    echo "=== 配置文件位置 ==="
    echo "应用配置: /opt/sqlbot/config/.env"
    echo "Nginx 配置: /etc/nginx/sites-available/sqlbot"
    echo "服务配置: /etc/systemd/system/sqlbot.service"
    echo "日志目录: /opt/sqlbot/logs/"
}

# 主函数
main() {
    log_info "开始 SQLBot 安全配置..."
    
    check_root
    setup_firewall
    setup_systemd_service
    setup_nginx
    generate_ssl_cert
    setup_log_rotation
    create_monitoring_script
    start_services
    show_deployment_info
}

# 执行主函数
main "$@"