#!/bin/bash

# Rustdesk 服务器管理脚本
# 用于日常维护和监控

RUSTDESK_DIR="/opt/rustdesk"
LOG_FILE="/var/log/rustdesk_manage.log"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# 检查目录
check_directory() {
    if [ ! -d "$RUSTDESK_DIR" ]; then
        log "错误: Rustdesk 目录不存在: $RUSTDESK_DIR"
        exit 1
    fi
    cd $RUSTDESK_DIR
}

# 显示帮助
show_help() {
    echo "Rustdesk 服务器管理工具"
    echo "用法: $0 [选项]"
    echo
    echo "选项:"
    echo "  status      - 显示服务状态"
    echo "  start       - 启动服务"
    echo "  stop        - 停止服务"
    echo "  restart     - 重启服务"
    echo "  logs        - 查看日志"
    echo "  update      - 更新服务"
    echo "  backup      - 备份配置和密钥"
    echo "  restore     - 恢复配置"
    echo "  monitor     - 监控服务状态"
    echo "  cleanup     - 清理旧日志和镜像"
    echo "  info        - 显示服务信息"
    echo "  test        - 测试连接"
    echo "  help        - 显示此帮助"
}

# 显示服务状态
show_status() {
    log "检查 Rustdesk 服务状态"
    echo "=== Docker 容器状态 ==="
    docker-compose ps
    echo
    echo "=== 端口监听状态 ==="
    netstat -tlnp | grep -E ':(21115|21116|21117|21119)' || echo "未发现监听端口"
    echo
    echo "=== 资源使用情况 ==="
    docker stats --no-stream rustdesk-hbbs rustdesk-hbbr 2>/dev/null || echo "容器未运行"
}

# 启动服务
start_service() {
    log "启动 Rustdesk 服务"
    docker-compose up -d
    sleep 5
    show_status
}

# 停止服务
stop_service() {
    log "停止 Rustdesk 服务"
    docker-compose down
}

# 重启服务
restart_service() {
    log "重启 Rustdesk 服务"
    docker-compose restart
    sleep 5
    show_status
}

# 查看日志
show_logs() {
    echo "选择要查看的日志:"
    echo "1) hbbs 日志"
    echo "2) hbbr 日志"
    echo "3) 所有日志"
    echo "4) 实时日志"
    read -p "请选择 (1-4): " choice
    
    case $choice in
        1) docker-compose logs hbbs ;;
        2) docker-compose logs hbbr ;;
        3) docker-compose logs ;;
        4) docker-compose logs -f ;;
        *) echo "无效选择" ;;
    esac
}

# 更新服务
update_service() {
    log "更新 Rustdesk 服务"
    echo "正在拉取最新镜像..."
    docker-compose pull
    echo "重启服务以应用更新..."
    docker-compose up -d
    sleep 5
    show_status
    log "更新完成"
}

# 备份配置
backup_config() {
    BACKUP_DIR="/opt/rustdesk_backup/$(date +%Y%m%d_%H%M%S)"
    log "备份配置到: $BACKUP_DIR"
    
    mkdir -p $BACKUP_DIR
    cp -r data $BACKUP_DIR/
    cp docker-compose.yml $BACKUP_DIR/
    
    echo "备份完成: $BACKUP_DIR"
    echo "备份内容:"
    ls -la $BACKUP_DIR
}

# 恢复配置
restore_config() {
    echo "可用的备份:"
    ls -la /opt/rustdesk_backup/ 2>/dev/null || {
        echo "未找到备份目录"
        return 1
    }
    
    read -p "请输入要恢复的备份目录名: " backup_name
    BACKUP_PATH="/opt/rustdesk_backup/$backup_name"
    
    if [ ! -d "$BACKUP_PATH" ]; then
        echo "备份目录不存在: $BACKUP_PATH"
        return 1
    fi
    
    log "从 $BACKUP_PATH 恢复配置"
    stop_service
    
    # 备份当前配置
    mv data data.old.$(date +%Y%m%d_%H%M%S) 2>/dev/null
    mv docker-compose.yml docker-compose.yml.old.$(date +%Y%m%d_%H%M%S) 2>/dev/null
    
    # 恢复配置
    cp -r $BACKUP_PATH/data .
    cp $BACKUP_PATH/docker-compose.yml .
    
    start_service
    log "配置恢复完成"
}

# 监控服务
monitor_service() {
    log "开始监控 Rustdesk 服务"
    echo "按 Ctrl+C 停止监控"
    
    while true; do
        clear
        echo "=== Rustdesk 服务监控 - $(date) ==="
        
        # 检查容器状态
        if docker-compose ps | grep -q "Up"; then
            echo "✓ 服务运行正常"
        else
            echo "✗ 服务异常"
            log "警告: 服务状态异常"
        fi
        
        # 检查端口
        for port in 21115 21116 21117 21119; do
            if netstat -tlnp | grep -q ":$port "; then
                echo "✓ 端口 $port 正常"
            else
                echo "✗ 端口 $port 异常"
                log "警告: 端口 $port 未监听"
            fi
        done
        
        # 显示资源使用
        echo
        echo "=== 资源使用 ==="
        docker stats --no-stream rustdesk-hbbs rustdesk-hbbr 2>/dev/null || echo "容器未运行"
        
        sleep 30
    done
}

# 清理
cleanup() {
    log "开始清理"
    
    echo "清理 Docker 镜像..."
    docker image prune -f
    
    echo "清理日志文件..."
    docker-compose logs --tail=1000 > /tmp/rustdesk_logs_$(date +%Y%m%d).log
    
    echo "清理完成"
}

# 显示服务信息
show_info() {
    echo "=== Rustdesk 服务信息 ==="
    echo "安装目录: $RUSTDESK_DIR"
    echo "配置文件: $RUSTDESK_DIR/docker-compose.yml"
    echo "数据目录: $RUSTDESK_DIR/data"
    echo "日志文件: $LOG_FILE"
    echo
    
    if [ -f "data/id_ed25519.pub" ]; then
        echo "=== 公钥信息 ==="
        cat data/id_ed25519.pub
        echo
    fi
    
    echo "=== 服务端点 ==="
    echo "信令服务器: $(hostname -I | awk '{print $1}'):21115"
    echo "中继服务器: $(hostname -I | awk '{print $1}'):21117"
    echo
    
    show_status
}

# 测试连接
test_connection() {
    echo "=== 连接测试 ==="
    
    # 测试端口连通性
    for port in 21115 21116 21117 21119; do
        if nc -z localhost $port 2>/dev/null; then
            echo "✓ 端口 $port 连通"
        else
            echo "✗ 端口 $port 不通"
        fi
    done
    
    echo
    echo "=== 网络测试 ==="
    echo "本机IP地址:"
    hostname -I
    
    echo "外网IP地址:"
    curl -s ifconfig.me || echo "无法获取外网IP"
}

# 主程序
main() {
    case "$1" in
        status)
            check_directory
            show_status
            ;;
        start)
            check_directory
            start_service
            ;;
        stop)
            check_directory
            stop_service
            ;;
        restart)
            check_directory
            restart_service
            ;;
        logs)
            check_directory
            show_logs
            ;;
        update)
            check_directory
            update_service
            ;;
        backup)
            check_directory
            backup_config
            ;;
        restore)
            check_directory
            restore_config
            ;;
        monitor)
            check_directory
            monitor_service
            ;;
        cleanup)
            check_directory
            cleanup
            ;;
        info)
            check_directory
            show_info
            ;;
        test)
            check_directory
            test_connection
            ;;
        help|--help|-h)
            show_help
            ;;
        "")
            show_help
            ;;
        *)
            echo "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
}

# 执行主程序
main "$@"