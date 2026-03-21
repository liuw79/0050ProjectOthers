#!/bin/bash

# SQLBot 快速部署脚本
# 用于一键部署到远程服务器

set -e

# 配置变量
REMOTE_USER="root"
REMOTE_HOST=""
DEPLOY_DIR="/tmp/sqlbot-deploy"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# 显示使用说明
show_usage() {
    echo "SQLBot 快速部署脚本"
    echo ""
    echo "使用方法:"
    echo "  $0 <服务器IP> [用户名]"
    echo ""
    echo "参数:"
    echo "  服务器IP    - 远程服务器的 IP 地址"
    echo "  用户名      - SSH 用户名 (默认: root)"
    echo ""
    echo "示例:"
    echo "  $0 192.168.1.100"
    echo "  $0 192.168.1.100 ubuntu"
    echo ""
    echo "注意:"
    echo "  - 确保已配置 SSH 密钥认证"
    echo "  - 确保目标用户有 sudo 权限"
    echo "  - 建议在部署前备份服务器数据"
}

# 检查参数
check_params() {
    if [[ $# -lt 1 ]]; then
        show_usage
        exit 1
    fi
    
    REMOTE_HOST="$1"
    if [[ $# -ge 2 ]]; then
        REMOTE_USER="$2"
    fi
    
    log_info "目标服务器: $REMOTE_USER@$REMOTE_HOST"
}

# 检查本地文件
check_local_files() {
    log_step "检查本地部署文件..."
    
    local required_files=(
        "deploy_remote.sh"
        "setup_security.sh"
        "sqlbot.service"
        "nginx_sqlbot.conf"
        "start_sqlbot.py"
        "config/.env"
    )
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            log_error "缺少必需文件: $file"
            exit 1
        fi
    done
    
    log_info "本地文件检查完成"
}

# 测试 SSH 连接
test_ssh_connection() {
    log_step "测试 SSH 连接..."
    
    if ssh -o ConnectTimeout=10 -o BatchMode=yes "$REMOTE_USER@$REMOTE_HOST" "echo 'SSH 连接成功'" > /dev/null 2>&1; then
        log_info "SSH 连接测试成功"
    else
        log_error "SSH 连接失败，请检查:"
        echo "  1. 服务器 IP 地址是否正确"
        echo "  2. SSH 服务是否运行"
        echo "  3. 防火墙是否允许 SSH 连接"
        echo "  4. SSH 密钥是否正确配置"
        exit 1
    fi
}

# 打包部署文件
package_files() {
    log_step "打包部署文件..."
    
    local package_name="sqlbot-deploy-$(date +%Y%m%d_%H%M%S).tar.gz"
    
    tar -czf "$package_name" \
        deploy_remote.sh \
        setup_security.sh \
        sqlbot.service \
        nginx_sqlbot.conf \
        start_sqlbot.py \
        config/.env \
        DEPLOYMENT_GUIDE.md
    
    echo "$package_name"
}

# 上传文件到服务器
upload_files() {
    local package_file="$1"
    
    log_step "上传部署文件到服务器..."
    
    # 创建远程目录
    ssh "$REMOTE_USER@$REMOTE_HOST" "mkdir -p $DEPLOY_DIR"
    
    # 上传文件
    scp "$package_file" "$REMOTE_USER@$REMOTE_HOST:$DEPLOY_DIR/"
    
    # 解压文件
    ssh "$REMOTE_USER@$REMOTE_HOST" "cd $DEPLOY_DIR && tar -xzf $package_file"
    
    log_info "文件上传完成"
}

# 执行远程部署
execute_remote_deployment() {
    log_step "执行远程部署..."
    
    # 执行基础部署
    log_info "执行基础部署脚本..."
    ssh "$REMOTE_USER@$REMOTE_HOST" "cd $DEPLOY_DIR && chmod +x deploy_remote.sh && ./deploy_remote.sh"
    
    # 执行安全配置
    log_info "执行安全配置脚本..."
    ssh "$REMOTE_USER@$REMOTE_HOST" "cd $DEPLOY_DIR && chmod +x setup_security.sh && ./setup_security.sh"
    
    log_info "远程部署完成"
}

# 验证部署结果
verify_deployment() {
    log_step "验证部署结果..."
    
    # 检查服务状态
    log_info "检查 SQLBot 服务状态..."
    if ssh "$REMOTE_USER@$REMOTE_HOST" "systemctl is-active --quiet sqlbot"; then
        log_info "✅ SQLBot 服务运行正常"
    else
        log_warn "❌ SQLBot 服务未运行"
    fi
    
    # 检查 Nginx 状态
    log_info "检查 Nginx 服务状态..."
    if ssh "$REMOTE_USER@$REMOTE_HOST" "systemctl is-active --quiet nginx"; then
        log_info "✅ Nginx 服务运行正常"
    else
        log_warn "❌ Nginx 服务未运行"
    fi
    
    # 健康检查
    log_info "执行健康检查..."
    if ssh "$REMOTE_USER@$REMOTE_HOST" "curl -s -f http://localhost:8004/health > /dev/null"; then
        log_info "✅ 应用健康检查通过"
    else
        log_warn "❌ 应用健康检查失败"
    fi
}

# 显示部署信息
show_deployment_info() {
    log_step "部署信息"
    
    echo ""
    echo "=== SQLBot 部署完成 ==="
    echo "服务器地址: $REMOTE_HOST"
    echo "本地访问: http://$REMOTE_HOST:8004"
    echo "HTTPS 访问: https://$REMOTE_HOST (需要配置域名和证书)"
    echo "健康检查: curl http://$REMOTE_HOST:8004/health"
    echo ""
    echo "=== 管理命令 ==="
    echo "查看服务状态:"
    echo "  ssh $REMOTE_USER@$REMOTE_HOST 'systemctl status sqlbot'"
    echo ""
    echo "查看日志:"
    echo "  ssh $REMOTE_USER@$REMOTE_HOST 'journalctl -u sqlbot -f'"
    echo ""
    echo "重启服务:"
    echo "  ssh $REMOTE_USER@$REMOTE_HOST 'systemctl restart sqlbot'"
    echo ""
    echo "=== 后续配置 ==="
    echo "1. 配置域名解析指向服务器 IP"
    echo "2. 获取 SSL 证书 (Let's Encrypt)"
    echo "3. 更新 /opt/sqlbot/config/.env 中的 AI API 密钥"
    echo "4. 根据需要调整防火墙规则"
    echo ""
    echo "详细文档: $DEPLOY_DIR/DEPLOYMENT_GUIDE.md"
}

# 清理本地文件
cleanup() {
    log_step "清理临时文件..."
    
    # 删除打包文件
    rm -f sqlbot-deploy-*.tar.gz
    
    log_info "清理完成"
}

# 主函数
main() {
    log_info "开始 SQLBot 快速部署..."
    
    check_params "$@"
    check_local_files
    test_ssh_connection
    
    local package_file
    package_file=$(package_files)
    
    upload_files "$package_file"
    execute_remote_deployment
    verify_deployment
    show_deployment_info
    cleanup
    
    log_info "SQLBot 快速部署完成！"
}

# 错误处理
trap 'log_error "部署过程中发生错误，请检查日志"; cleanup; exit 1' ERR

# 执行主函数
main "$@"