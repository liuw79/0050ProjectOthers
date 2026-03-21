#!/bin/bash

# 交互式 NAS 清理工具
# 支持目录选择、详细日志记录和安全确认

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 进度条相关变量
PROGRESS_BAR_WIDTH=50
PROGRESS_CHAR="█"
EMPTY_CHAR="░"

# 配置文件路径
CONFIG_FILE="$(dirname "$0")/nas_connection.conf"
LOG_DIR="$(dirname "$0")/logs"
LOG_FILE="$LOG_DIR/cleanup_$(date +%Y%m%d_%H%M%S).log"

# 创建日志目录
mkdir -p "$LOG_DIR"

# 日志函数
log_info() {
    local message="$1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $message" | tee -a "$LOG_FILE"
}

log_warn() {
    local message="$1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARN: $message" | tee -a "$LOG_FILE"
}

log_error() {
    local message="$1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $message" | tee -a "$LOG_FILE"
}

# 进度条函数
show_progress() {
    local current=$1
    local total=$2
    local message="$3"
    local percent=$((current * 100 / total))
    local filled=$((current * PROGRESS_BAR_WIDTH / total))
    local empty=$((PROGRESS_BAR_WIDTH - filled))
    
    printf "\r${CYAN}%s${NC} [" "$message"
    printf "%*s" $filled | tr ' ' "$PROGRESS_CHAR"
    printf "%*s" $empty | tr ' ' "$EMPTY_CHAR"
    printf "] %d%% (%d/%d)" $percent $current $total
}

# 完成进度条显示
complete_progress() {
    local message="$1"
    printf "\r${GREEN}%s${NC} [" "$message"
    printf "%*s" $PROGRESS_BAR_WIDTH | tr ' ' "$PROGRESS_CHAR"
    printf "] 100%%\n"
}

# 带进度条的命令执行
execute_with_progress() {
    local command="$1"
    local description="$2"
    local steps="$3"
    
    if [[ -z "$steps" ]]; then
        steps=1
    fi
    
    log_info "执行带进度的远程命令: $command"
    
    for ((i=1; i<=steps; i++)); do
        show_progress $i $steps "$description"
        sleep 0.1
    done
    
    local result=$(execute_remote_command "$command" "")
    complete_progress "$description"
    echo "$result"
    
    return $?
}

# 显示标题
show_header() {
    clear
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                  🧹 交互式 NAS 清理工具                      ║"
    echo "║                                                              ║"
    echo "║  智能清理 • 目录选择 • 详细日志 • 安全确认                   ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# 加载配置
load_config() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        log_error "配置文件不存在: $CONFIG_FILE"
        echo -e "${RED}❌ 配置文件不存在，请先创建 nas_connection.conf${NC}"
        exit 1
    fi
    
    source "$CONFIG_FILE"
    log_info "配置文件加载成功"
}

# 测试SSH连接
test_ssh_connection() {
    echo -e "${YELLOW}🔍 测试 SSH 连接...${NC}"
    log_info "开始测试SSH连接到 $NAS_HOST:$NAS_SSH_PORT"
    
    # 测试连接
    if sshpass -p "$NAS_PASSWORD" ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no -p "$NAS_SSH_PORT" "$NAS_USERNAME@$NAS_HOST" "echo 'SSH连接成功'" 2>/dev/null; then
        echo -e "${GREEN}✅ SSH 连接成功${NC}"
        log_info "SSH连接测试成功"
        return 0
    else
        echo -e "${RED}❌ SSH 连接失败${NC}"
        log_error "SSH连接失败"
        echo -e "${YELLOW}请检查:${NC}"
        echo "  1. NAS SSH 服务是否启用"
        echo "  2. 用户名密码是否正确"
        echo "  3. 端口号是否正确 (当前: $NAS_SSH_PORT)"
        echo "  4. 网络连接是否正常"
        echo ""
        read -p "是否继续尝试连接? (y/N): " continue_choice
        if [[ ! "$continue_choice" =~ ^[Yy]$ ]]; then
            exit 1
        fi
        return 1
    fi
}

# 执行远程命令
execute_remote_command() {
    local command="$1"
    local description="$2"
    
    log_info "执行远程命令: $command"
    if [[ -n "$description" ]]; then
        echo -e "${BLUE}🔧 $description${NC}"
    fi
    
    sshpass -p "$NAS_PASSWORD" ssh -o ConnectTimeout=30 -o StrictHostKeyChecking=no -p "$NAS_SSH_PORT" "$NAS_USERNAME@$NAS_HOST" "$command" 2>&1 | tee -a "$LOG_FILE"
    local exit_code=${PIPESTATUS[0]}
    
    if [[ $exit_code -eq 0 ]]; then
        log_info "命令执行成功: $command"
    else
        log_error "命令执行失败: $command (退出码: $exit_code)"
    fi
    
    return $exit_code
}

# 获取目录列表
get_directory_list() {
    echo -e "${BLUE}📁 获取 NAS 目录列表...${NC}"
    log_info "获取NAS目录列表"
    
    local dirs=$(execute_remote_command "find $NAS_REMOTE_PATH -maxdepth 2 -type d -name '*' | head -20 | sort" "获取目录列表")
    
    if [[ -z "$dirs" ]]; then
        log_error "无法获取目录列表"
        return 1
    fi
    
    echo "$dirs"
}

# 显示目录选择菜单
show_directory_menu() {
    local dirs="$1"
    
    echo -e "${CYAN}\n📋 可用目录列表:${NC}"
    echo "$dirs" | nl -w2 -s'. '
    
    echo -e "${PURPLE}特殊选项:${NC}"
    echo "  0. 全部目录 (谨慎使用)"
    echo "  q. 退出程序"
    echo ""
}

# 选择目录
select_directory() {
    local dirs="$1"
    local dir_array=()
    
    # 将目录列表转换为数组
    while IFS= read -r line; do
        [[ -n "$line" ]] && dir_array+=("$line")
    done <<< "$dirs"
    
    while true; do
        show_directory_menu "$dirs"
        read -p "请选择要清理的目录 (输入数字): " choice
        
        case "$choice" in
            q|Q)
                echo -e "${YELLOW}👋 退出程序${NC}"
                log_info "用户选择退出程序"
                exit 0
                ;;
            0)
                echo -e "${RED}⚠️  您选择了清理所有目录，这可能需要很长时间！${NC}"
                read -p "确认要继续吗? (输入 'YES' 确认): " confirm
                if [[ "$confirm" == "YES" ]]; then
                    selected_dir="$NAS_REMOTE_PATH"
                    log_info "用户选择清理所有目录: $selected_dir"
                    return 0
                fi
                ;;
            '')
                echo -e "${RED}❌ 请输入有效选项${NC}"
                ;;
            *)
                if [[ "$choice" =~ ^[0-9]+$ ]] && [[ $choice -ge 1 ]] && [[ $choice -le ${#dir_array[@]} ]]; then
                    selected_dir="${dir_array[$((choice-1))]}"
                    echo -e "${GREEN}✅ 已选择目录: $selected_dir${NC}"
                    log_info "用户选择目录: $selected_dir"
                    return 0
                else
                    echo -e "${RED}❌ 无效选择，请输入 1-${#dir_array[@]} 之间的数字${NC}"
                fi
                ;;
        esac
        echo ""
    done
}

# 显示清理选项菜单
show_cleanup_menu() {
    echo -e "${CYAN}\n🧹 清理选项:${NC}"
    echo "  1. 快速扫描 (查看目录大小和文件统计)"
    echo "  2. 清理临时文件 (.tmp, .cache, .log等)"
    echo "  3. 清理空目录"
    echo "  4. 查找大文件 (>100MB)"
    echo "  5. 查找重复文件"
    echo "  6. 自定义清理 (指定文件类型)"
    echo "  7. 完整清理报告"
    echo "  8. 返回目录选择"
    echo "  q. 退出程序"
    echo ""
}

# 快速扫描
quick_scan() {
    local target_dir="$1"
    
    echo -e "${BLUE}🔍 正在扫描目录: $target_dir${NC}"
    log_info "开始快速扫描: $target_dir"
    
    echo -e "${YELLOW}📊 扫描进度:${NC}"
    
    # 步骤1: 目录大小统计
    show_progress 1 3 "分析目录大小"
    execute_remote_command "echo '=== 目录大小统计 ==='; du -sh '$target_dir'/* 2>/dev/null | sort -hr | head -10" "获取目录大小排行" > /dev/null
    
    # 步骤2: 文件类型统计
    show_progress 2 3 "统计文件类型"
    execute_remote_command "echo '\n=== 文件类型统计 ==='; find '$target_dir' -type f -name '*.*' | sed 's/.*\.//' | sort | uniq -c | sort -nr | head -10" "统计文件类型" > /dev/null
    
    # 步骤3: 总体统计
    show_progress 3 3 "计算总体统计"
    execute_remote_command "echo '\n=== 总体统计 ==='; echo \"总文件数: \$(find '$target_dir' -type f | wc -l)\"; echo \"总目录数: \$(find '$target_dir' -type d | wc -l)\"; echo \"总大小: \$(du -sh '$target_dir' | cut -f1)\"" "获取总体统计" > /dev/null
    
    complete_progress "扫描完成"
    
    # 显示结果
    echo -e "\n${CYAN}=== 扫描结果 ===${NC}"
    execute_remote_command "echo '=== 目录大小统计 ==='; du -sh '$target_dir'/* 2>/dev/null | sort -hr | head -10" ""
    execute_remote_command "echo '\n=== 文件类型统计 ==='; find '$target_dir' -type f -name '*.*' | sed 's/.*\.//' | sort | uniq -c | sort -nr | head -10" ""
    execute_remote_command "echo '\n=== 总体统计 ==='; echo \"总文件数: \$(find '$target_dir' -type f | wc -l)\"; echo \"总目录数: \$(find '$target_dir' -type d | wc -l)\"; echo \"总大小: \$(du -sh '$target_dir' | cut -f1)\"" ""
    
    log_info "快速扫描完成: $target_dir"
}

# 清理临时文件
clean_temp_files() {
    local target_dir="$1"
    
    echo -e "${YELLOW}🗑️  正在清理临时文件...${NC}"
    log_info "开始清理临时文件: $target_dir"
    
    # 步骤1: 扫描临时文件
    echo -e "${YELLOW}📊 扫描进度:${NC}"
    show_progress 1 2 "扫描临时文件"
    
    # 显示将要删除的文件
    echo -e "\n${CYAN}预览将要删除的临时文件:${NC}"
    local temp_files=$(execute_remote_command "find '$target_dir' -type f \\( -name '*.tmp' -o -name '*.cache' -o -name '*.log' -o -name '*.bak' -o -name '*~' -o -name '.DS_Store' \\) -print" "查找临时文件")
    
    show_progress 2 2 "分析临时文件"
    local file_count=$(echo "$temp_files" | grep -c '^' 2>/dev/null || echo "0")
    complete_progress "扫描完成"
    
    echo "$temp_files"
    echo -e "\n${BLUE}📈 统计: 找到 $file_count 个临时文件${NC}"
    
    if [[ $file_count -eq 0 ]]; then
        echo -e "${GREEN}✅ 没有找到临时文件${NC}"
        return 0
    fi
    
    read -p "确认删除这些文件吗? (y/N): " confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}🗑️  删除进度:${NC}"
        show_progress 1 1 "删除临时文件"
        execute_remote_command "find '$target_dir' -type f \\( -name '*.tmp' -o -name '*.cache' -o -name '*.log' -o -name '*.bak' -o -name '*~' -o -name '.DS_Store' \\) -delete" "删除临时文件" > /dev/null
        complete_progress "删除完成"
        echo -e "${GREEN}✅ 临时文件清理完成 (删除了 $file_count 个文件)${NC}"
        log_info "临时文件清理完成: $target_dir, 删除文件数: $file_count"
    else
        echo -e "${YELLOW}⏭️  跳过临时文件清理${NC}"
        log_info "用户跳过临时文件清理"
    fi
}

# 清理空目录
clean_empty_dirs() {
    local target_dir="$1"
    
    echo -e "${YELLOW}📁 正在查找空目录...${NC}"
    log_info "开始清理空目录: $target_dir"
    
    # 步骤1: 扫描空目录
    echo -e "${YELLOW}📊 扫描进度:${NC}"
    show_progress 1 2 "扫描空目录"
    
    # 显示空目录
    echo -e "\n${CYAN}找到的空目录:${NC}"
    local empty_dirs=$(execute_remote_command "find '$target_dir' -type d -empty -print" "查找空目录")
    
    show_progress 2 2 "分析空目录"
    local dir_count=$(echo "$empty_dirs" | grep -c '^' 2>/dev/null || echo "0")
    complete_progress "扫描完成"
    
    echo "$empty_dirs"
    echo -e "\n${BLUE}📈 统计: 找到 $dir_count 个空目录${NC}"
    
    if [[ $dir_count -eq 0 ]]; then
        echo -e "${GREEN}✅ 没有找到空目录${NC}"
        return 0
    fi
    
    read -p "确认删除这些空目录吗? (y/N): " confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}🗑️  删除进度:${NC}"
        show_progress 1 1 "删除空目录"
        execute_remote_command "find '$target_dir' -type d -empty -delete" "删除空目录" > /dev/null
        complete_progress "删除完成"
        echo -e "${GREEN}✅ 空目录清理完成 (删除了 $dir_count 个目录)${NC}"
        log_info "空目录清理完成: $target_dir, 删除目录数: $dir_count"
    else
        echo -e "${YELLOW}⏭️  跳过空目录清理${NC}"
        log_info "用户跳过空目录清理"
    fi
}

# 查找大文件
find_large_files() {
    local target_dir="$1"
    
    echo -e "${BLUE}🔍 正在查找大文件 (>100MB)...${NC}"
    log_info "开始查找大文件: $target_dir"
    
    # 步骤1: 扫描大文件
    echo -e "${YELLOW}📊 扫描进度:${NC}"
    show_progress 1 3 "扫描大文件"
    
    local large_files=$(execute_remote_command "find '$target_dir' -type f -size +100M -exec ls -lh {} \\;" "查找大文件")
    
    show_progress 2 3 "分析文件大小"
    local file_count=$(echo "$large_files" | grep -c '^' 2>/dev/null || echo "0")
    
    show_progress 3 3 "排序文件列表"
    local sorted_files=$(echo "$large_files" | sort -k5 -hr)
    complete_progress "扫描完成"
    
    echo -e "\n${CYAN}=== 大文件列表 (>100MB) ===${NC}"
    echo "$sorted_files"
    echo -e "\n${BLUE}📈 统计: 找到 $file_count 个大文件${NC}"
    
    if [[ $file_count -eq 0 ]]; then
        echo -e "${GREEN}✅ 没有找到大于100MB的文件${NC}"
    fi
    
    log_info "大文件查找完成: $target_dir, 找到文件数: $file_count"
}

# 查找重复文件
find_duplicate_files() {
    local target_dir="$1"
    
    echo -e "${BLUE}🔍 正在查找重复文件...${NC}"
    log_info "开始查找重复文件: $target_dir"
    
    echo -e "${YELLOW}📊 扫描进度 (这可能需要较长时间):${NC}"
    
    # 步骤1: 计算文件MD5
    show_progress 1 3 "计算文件MD5值"
    local md5_results=$(execute_remote_command "find '$target_dir' -type f -exec md5sum {} \\;" "计算MD5")
    
    # 步骤2: 排序MD5结果
    show_progress 2 3 "排序MD5结果"
    local sorted_md5=$(echo "$md5_results" | sort)
    
    # 步骤3: 查找重复
    show_progress 3 3 "查找重复文件"
    local duplicates=$(echo "$sorted_md5" | uniq -d -w32)
    complete_progress "扫描完成"
    
    local dup_count=$(echo "$duplicates" | grep -c '^' 2>/dev/null || echo "0")
    
    echo -e "\n${CYAN}=== 重复文件列表 ===${NC}"
    if [[ $dup_count -eq 0 ]]; then
        echo -e "${GREEN}✅ 没有找到重复文件${NC}"
    else
        echo "$duplicates"
        echo -e "\n${BLUE}📈 统计: 找到 $dup_count 个重复文件${NC}"
    fi
    
    log_info "重复文件查找完成: $target_dir, 找到重复文件数: $dup_count"
}

# 自定义清理
custom_cleanup() {
    local target_dir="$1"
    
    echo -e "${PURPLE}🎯 自定义清理${NC}"
    echo "请输入要清理的文件扩展名 (例如: *.avi, *.mkv, *.iso)"
    read -p "文件模式: " file_pattern
    
    if [[ -z "$file_pattern" ]]; then
        echo -e "${RED}❌ 未输入文件模式${NC}"
        return 1
    fi
    
    log_info "开始自定义清理: $target_dir, 模式: $file_pattern"
    
    # 步骤1: 扫描匹配文件
    echo -e "${YELLOW}📊 扫描进度:${NC}"
    show_progress 1 2 "扫描匹配文件"
    
    # 显示匹配的文件
    echo -e "\n${CYAN}匹配的文件:${NC}"
    local matched_files=$(execute_remote_command "find '$target_dir' -type f -name '$file_pattern' -exec ls -lh {} \\;" "查找匹配文件")
    
    show_progress 2 2 "分析匹配文件"
    local file_count=$(echo "$matched_files" | grep -c '^' 2>/dev/null || echo "0")
    complete_progress "扫描完成"
    
    echo "$matched_files"
    echo -e "\n${BLUE}📈 统计: 找到 $file_count 个匹配文件 (模式: $file_pattern)${NC}"
    
    if [[ $file_count -eq 0 ]]; then
        echo -e "${GREEN}✅ 没有找到匹配的文件${NC}"
        return 0
    fi
    
    read -p "确认删除这些文件吗? (y/N): " confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}🗑️  删除进度:${NC}"
        show_progress 1 1 "删除匹配文件"
        execute_remote_command "find '$target_dir' -type f -name '$file_pattern' -delete" "删除匹配文件" > /dev/null
        complete_progress "删除完成"
        echo -e "${GREEN}✅ 自定义清理完成 (删除了 $file_count 个文件)${NC}"
        log_info "自定义清理完成: $target_dir, 模式: $file_pattern, 删除文件数: $file_count"
    else
        echo -e "${YELLOW}⏭️  跳过自定义清理${NC}"
        log_info "用户跳过自定义清理"
    fi
}

# 生成完整清理报告
generate_full_report() {
    local target_dir="$1"
    local report_file="$LOG_DIR/report_$(date +%Y%m%d_%H%M%S).txt"
    
    echo -e "${BLUE}📊 正在生成完整清理报告...${NC}"
    log_info "开始生成完整报告: $target_dir"
    
    echo -e "${YELLOW}📊 报告生成进度:${NC}"
    
    {
        echo "=== NAS 清理报告 ==="
        echo "生成时间: $(date)"
        echo "目标目录: $target_dir"
        echo ""
        
        # 步骤1: 目录大小统计
        show_progress 1 6 "分析目录大小"
        echo "=== 目录大小统计 ==="
        execute_remote_command "du -sh '$target_dir'/* 2>/dev/null | sort -hr" "" 2>/dev/null
        
        # 步骤2: 文件类型统计
        show_progress 2 6 "统计文件类型"
        echo "\n=== 文件类型统计 ==="
        execute_remote_command "find '$target_dir' -type f -name '*.*' | sed 's/.*\.//' | sort | uniq -c | sort -nr" "" 2>/dev/null
        
        # 步骤3: 大文件列表
        show_progress 3 6 "查找大文件"
        echo "\n=== 大文件列表 (>100MB) ==="
        execute_remote_command "find '$target_dir' -type f -size +100M -exec ls -lh {} \\; | sort -k5 -hr" "" 2>/dev/null
        
        # 步骤4: 临时文件统计
        show_progress 4 6 "统计临时文件"
        echo "\n=== 临时文件统计 ==="
        execute_remote_command "find '$target_dir' -type f \\( -name '*.tmp' -o -name '*.cache' -o -name '*.log' -o -name '*.bak' -o -name '*~' -o -name '.DS_Store' \\) | wc -l" "" 2>/dev/null
        
        # 步骤5: 空目录统计
        show_progress 5 6 "统计空目录"
        echo "\n=== 空目录统计 ==="
        execute_remote_command "find '$target_dir' -type d -empty | wc -l" "" 2>/dev/null
        
        # 步骤6: 总体统计
        show_progress 6 6 "生成总体统计"
        echo "\n=== 总体统计 ==="
        execute_remote_command "echo \"总文件数: \$(find '$target_dir' -type f | wc -l)\"; echo \"总目录数: \$(find '$target_dir' -type d | wc -l)\"; echo \"总大小: \$(du -sh '$target_dir' | cut -f1)\"" "" 2>/dev/null
        
    } > "$report_file"
    
    complete_progress "报告生成完成"
    
    echo -e "\n${GREEN}✅ 报告已生成: $report_file${NC}"
    echo -e "${CYAN}📄 报告内容预览:${NC}"
    head -20 "$report_file"
    echo -e "${YELLOW}... (完整报告请查看文件)${NC}"
    
    log_info "完整报告生成完成: $report_file"
}

# 清理操作循环
cleanup_loop() {
    local target_dir="$1"
    
    while true; do
        show_cleanup_menu
        read -p "请选择清理操作 (输入数字): " choice
        
        case "$choice" in
            1) quick_scan "$target_dir" ;;
            2) clean_temp_files "$target_dir" ;;
            3) clean_empty_dirs "$target_dir" ;;
            4) find_large_files "$target_dir" ;;
            5) find_duplicate_files "$target_dir" ;;
            6) custom_cleanup "$target_dir" ;;
            7) generate_full_report "$target_dir" ;;
            8) return 0 ;;
            q|Q)
                echo -e "${YELLOW}👋 退出程序${NC}"
                log_info "用户选择退出程序"
                exit 0
                ;;
            *)
                echo -e "${RED}❌ 无效选择，请输入 1-8 或 q${NC}"
                ;;
        esac
        
        echo ""
        read -p "按 Enter 继续..."
    done
}

# 主函数
main() {
    show_header
    
    log_info "=== 交互式NAS清理工具启动 ==="
    log_info "日志文件: $LOG_FILE"
    
    # 加载配置
    load_config
    
    echo -e "${BLUE}📡 NAS 连接信息:${NC}"
    echo "  主机: $NAS_HOST"
    echo "  端口: $NAS_SSH_PORT"
    echo "  用户: $NAS_USERNAME"
    echo "  路径: $NAS_REMOTE_PATH"
    echo ""
    
    # 测试连接
    if ! test_ssh_connection; then
        echo -e "${RED}❌ SSH 连接失败，请检查配置后重试${NC}"
        log_error "SSH连接失败，程序退出"
        exit 1
    fi
    
    # 主循环
    while true; do
        # 获取目录列表
        dirs=$(get_directory_list)
        if [[ -z "$dirs" ]]; then
            echo -e "${RED}❌ 无法获取目录列表${NC}"
            exit 1
        fi
        
        # 选择目录
        select_directory "$dirs"
        
        # 执行清理操作
        cleanup_loop "$selected_dir"
    done
}

# 信号处理
trap 'echo -e "\n${YELLOW}程序被中断${NC}"; log_info "程序被用户中断"; exit 1' INT TERM

# 运行主函数
main "$@"