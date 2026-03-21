#!/bin/bash

# 远程 NAS 清理脚本
# 通过 SSH 连接到 NAS 并执行清理操作
# 支持分目录并行处理以提高速度

# 配置变量
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONNECTION_CONFIG="$SCRIPT_DIR/nas_connection.conf"
LOG_FILE="$SCRIPT_DIR/remote_cleanup_$(date +%Y%m%d_%H%M%S).log"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 加载连接配置
load_connection_config() {
    if [ ! -f "$CONNECTION_CONFIG" ]; then
        echo -e "${RED}❌ 连接配置文件不存在: $CONNECTION_CONFIG${NC}"
        echo "请先创建连接配置文件"
        exit 1
    fi
    
    source "$CONNECTION_CONFIG"
    
    # 验证必要的配置
    if [ -z "$NAS_HOST" ] || [ -z "$NAS_USERNAME" ] || [ -z "$NAS_PASSWORD" ] || [ -z "$NAS_SSH_PORT" ]; then
        echo -e "${RED}❌ 连接配置不完整${NC}"
        exit 1
    fi
}

# 日志记录函数
log_message() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $message" | tee -a "$LOG_FILE"
}

# 显示横幅
show_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                  🌐 远程 NAS 清理工具                         ║"
    echo "║                                                              ║"
    echo "║  通过 SSH 连接到 NAS 并执行高效的分目录清理操作                ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${BLUE}NAS 地址: ${YELLOW}$NAS_HOST:$NAS_SSH_PORT${NC}"
    echo -e "${BLUE}用户名: ${YELLOW}$NAS_USERNAME${NC}"
    echo -e "${BLUE}远程路径: ${YELLOW}$NAS_REMOTE_PATH${NC}"
    echo
}

# 测试 SSH 连接
test_ssh_connection() {
    echo -e "${BLUE}🔗 测试 SSH 连接...${NC}"
    
    # 使用 sshpass 进行密码认证
    if ! command -v sshpass &> /dev/null; then
        echo -e "${YELLOW}⚠️ sshpass 未安装，尝试安装...${NC}"
        if command -v brew &> /dev/null; then
            brew install sshpass
        else
            echo -e "${RED}❌ 请先安装 sshpass: brew install sshpass${NC}"
            return 1
        fi
    fi
    
    # 测试连接
    if sshpass -p "$NAS_PASSWORD" ssh -p "$NAS_SSH_PORT" -o ConnectTimeout=10 -o StrictHostKeyChecking=no "$NAS_USERNAME@$NAS_HOST" "echo 'SSH连接成功'" 2>/dev/null; then
        echo -e "${GREEN}✅ SSH 连接测试成功${NC}"
        return 0
    else
        echo -e "${RED}❌ SSH 连接失败${NC}"
        echo "请检查："
        echo "  1. NAS 地址和端口是否正确"
        echo "  2. 用户名和密码是否正确"
        echo "  3. SSH 服务是否已启用"
        echo "  4. 防火墙设置是否允许连接"
        return 1
    fi
}

# 执行远程命令
execute_remote_command() {
    local command="$1"
    local description="$2"
    
    if [ -n "$description" ]; then
        echo -e "${YELLOW}$description${NC}"
    fi
    
    sshpass -p "$NAS_PASSWORD" ssh -p "$NAS_SSH_PORT" -o StrictHostKeyChecking=no "$NAS_USERNAME@$NAS_HOST" "$command" 2>/dev/null
}

# 获取远程磁盘使用情况
show_remote_disk_usage() {
    echo -e "${BLUE}📊 远程磁盘使用情况:${NC}"
    
    local disk_info
    disk_info=$(execute_remote_command "df -h $NAS_REMOTE_PATH" "正在获取磁盘信息...")
    
    if [ -n "$disk_info" ]; then
        echo "$disk_info" | awk 'NR==2 {printf "使用: %s / %s (%s)\n", $3, $2, $5}'
    else
        echo -e "${RED}❌ 无法获取磁盘信息${NC}"
    fi
    echo
}

# 获取主要目录列表
get_main_directories() {
    echo -e "${BLUE}📁 获取主要目录列表...${NC}"
    
    local dirs
    dirs=$(execute_remote_command "find $NAS_REMOTE_PATH -maxdepth 2 -type d -not -path '*/\.*' | head -20" "扫描目录结构...")
    
    if [ -n "$dirs" ]; then
        echo "发现的主要目录:"
        echo "$dirs" | while read -r dir; do
            if [ "$dir" != "$NAS_REMOTE_PATH" ]; then
                echo "  📂 $dir"
            fi
        done
    else
        echo -e "${RED}❌ 无法获取目录列表${NC}"
    fi
    echo
}

# 分目录快速扫描
quick_scan_by_directory() {
    echo -e "${BLUE}🔍 分目录快速扫描...${NC}"
    
    # 获取主要目录
    local main_dirs
    main_dirs=$(execute_remote_command "find $NAS_REMOTE_PATH -maxdepth 1 -type d -not -path '*/\.*' | grep -v '^$NAS_REMOTE_PATH$'")
    
    if [ -z "$main_dirs" ]; then
        echo -e "${RED}❌ 无法获取目录列表${NC}"
        return 1
    fi
    
    echo "正在扫描各目录，请稍候..."
    echo
    
    # 并行扫描各目录
    echo "$main_dirs" | while read -r dir; do
        if [ -n "$dir" ]; then
            local dir_name=$(basename "$dir")
            echo -e "${CYAN}📂 扫描目录: $dir_name${NC}"
            
            # 临时文件统计
            local temp_count
            temp_count=$(execute_remote_command "find '$dir' -type f \\( -name '*.tmp' -o -name '*.temp' -o -name '*.cache' -o -name '.DS_Store' -o -name 'Thumbs.db' \\) 2>/dev/null | wc -l")
            
            # 大文件统计
            local large_count
            large_count=$(execute_remote_command "find '$dir' -type f -size +100M 2>/dev/null | wc -l")
            
            # 空目录统计
            local empty_count
            empty_count=$(execute_remote_command "find '$dir' -type d -empty 2>/dev/null | wc -l")
            
            # 目录大小
            local dir_size
            dir_size=$(execute_remote_command "du -sh '$dir' 2>/dev/null | cut -f1")
            
            echo "  📊 大小: ${YELLOW}${dir_size:-未知}${NC}"
            echo "  🗑️ 临时文件: ${YELLOW}${temp_count:-0}${NC} 个"
            echo "  📦 大文件: ${YELLOW}${large_count:-0}${NC} 个"
            echo "  📁 空目录: ${YELLOW}${empty_count:-0}${NC} 个"
            echo
        fi
    done
}

# 清理指定目录的临时文件
clean_temp_files_in_directory() {
    local target_dir="$1"
    local dir_name=$(basename "$target_dir")
    
    echo -e "${BLUE}🗑️ 清理目录 '$dir_name' 中的临时文件...${NC}"
    
    local temp_patterns=(
        "*.tmp"
        "*.temp"
        "*.cache"
        "*.bak"
        "*.old"
        "*.swp"
        ".DS_Store"
        "Thumbs.db"
        "desktop.ini"
    )
    
    local total_removed=0
    
    for pattern in "${temp_patterns[@]}"; do
        echo -e "${YELLOW}  正在查找 $pattern 文件...${NC}"
        
        # 查找文件
        local files
        files=$(execute_remote_command "find '$target_dir' -name '$pattern' -type f 2>/dev/null")
        
        if [ -n "$files" ]; then
            local count
            count=$(echo "$files" | wc -l)
            
            if [ "$count" -gt 0 ]; then
                echo "    发现 $count 个 $pattern 文件"
                
                read -p "    删除这些文件吗？(y/N): " confirm
                if [[ $confirm =~ ^[Yy]$ ]]; then
                    # 执行删除
                    local delete_cmd="find '$target_dir' -name '$pattern' -type f -delete 2>/dev/null"
                    execute_remote_command "$delete_cmd" "正在删除文件..."
                    
                    total_removed=$((total_removed + count))
                    echo -e "    ${GREEN}✅ 已删除 $count 个文件${NC}"
                else
                    echo -e "    ${YELLOW}⏭️ 跳过删除${NC}"
                fi
            fi
        fi
    done
    
    if [ "$total_removed" -gt 0 ]; then
        echo -e "${GREEN}🎉 目录 '$dir_name' 清理完成！删除了 $total_removed 个文件${NC}"
    else
        echo -e "${BLUE}ℹ️ 目录 '$dir_name' 没有找到需要清理的临时文件${NC}"
    fi
    echo
}

# 清理指定目录的空目录
clean_empty_dirs_in_directory() {
    local target_dir="$1"
    local dir_name=$(basename "$target_dir")
    
    echo -e "${BLUE}📁 清理目录 '$dir_name' 中的空目录...${NC}"
    
    local empty_dirs
    empty_dirs=$(execute_remote_command "find '$target_dir' -type d -empty 2>/dev/null")
    
    if [ -z "$empty_dirs" ]; then
        echo -e "${BLUE}ℹ️ 目录 '$dir_name' 没有发现空目录${NC}"
        echo
        return 0
    fi
    
    local count
    count=$(echo "$empty_dirs" | wc -l)
    
    echo "发现 $count 个空目录"
    echo "$empty_dirs" | head -5
    
    if [ "$count" -gt 5 ]; then
        echo "... 还有 $((count - 5)) 个目录"
    fi
    
    read -p "删除这些空目录吗？(y/N): " confirm
    if [[ $confirm =~ ^[Yy]$ ]]; then
        execute_remote_command "find '$target_dir' -type d -empty -delete 2>/dev/null" "正在删除空目录..."
        echo -e "${GREEN}✅ 空目录清理完成${NC}"
    else
        echo -e "${YELLOW}⏭️ 跳过删除空目录${NC}"
    fi
    echo
}

# 查找指定目录的大文件
find_large_files_in_directory() {
    local target_dir="$1"
    local dir_name=$(basename "$target_dir")
    
    echo -e "${BLUE}📦 查找目录 '$dir_name' 中的大文件 (>100MB)...${NC}"
    
    local large_files
    large_files=$(execute_remote_command "find '$target_dir' -type f -size +100M -exec ls -lh {} \\; 2>/dev/null | awk '{print \$5 \"\\t\" \$9}' | sort -hr | head -10")
    
    if [ -z "$large_files" ]; then
        echo -e "${BLUE}ℹ️ 目录 '$dir_name' 没有发现大文件 (>100MB)${NC}"
        echo
        return 0
    fi
    
    echo "发现的大文件 (前10个):"
    echo -e "${YELLOW}大小\t\t文件路径${NC}"
    echo "$large_files"
    echo
}

# 选择目录进行清理
select_directory_for_cleanup() {
    echo -e "${PURPLE}选择要清理的目录:${NC}"
    
    # 获取主要目录列表
    local main_dirs
    main_dirs=$(execute_remote_command "find $NAS_REMOTE_PATH -maxdepth 1 -type d -not -path '*/\.*' | grep -v '^$NAS_REMOTE_PATH$'")
    
    if [ -z "$main_dirs" ]; then
        echo -e "${RED}❌ 无法获取目录列表${NC}"
        return 1
    fi
    
    # 显示目录选项
    local dir_array=()
    local index=1
    
    echo "$main_dirs" | while read -r dir; do
        if [ -n "$dir" ]; then
            dir_array+=("$dir")
            local dir_name=$(basename "$dir")
            echo -e "${CYAN}  $index)${NC} 📂 $dir_name"
            ((index++))
        fi
    done
    
    echo -e "${CYAN}  0)${NC} 🔙 返回主菜单"
    echo
    
    read -p "请选择目录 (输入数字): " dir_choice
    
    if [[ "$dir_choice" == "0" ]]; then
        return 0
    fi
    
    # 转换为数组并选择目录
    local selected_dir
    selected_dir=$(echo "$main_dirs" | sed -n "${dir_choice}p")
    
    if [ -n "$selected_dir" ]; then
        echo -e "${GREEN}已选择目录: $(basename "$selected_dir")${NC}"
        echo
        
        # 显示目录清理选项
        echo -e "${PURPLE}选择清理操作:${NC}"
        echo -e "${CYAN}  1)${NC} 🗑️ 清理临时文件"
        echo -e "${CYAN}  2)${NC} 📁 清理空目录"
        echo -e "${CYAN}  3)${NC} 📦 查找大文件"
        echo -e "${CYAN}  4)${NC} 🧹 全部清理 (临时文件 + 空目录)"
        echo -e "${CYAN}  0)${NC} 🔙 返回"
        echo
        
        read -p "请选择操作 (0-4): " action_choice
        
        case $action_choice in
            1)
                clean_temp_files_in_directory "$selected_dir"
                ;;
            2)
                clean_empty_dirs_in_directory "$selected_dir"
                ;;
            3)
                find_large_files_in_directory "$selected_dir"
                ;;
            4)
                clean_temp_files_in_directory "$selected_dir"
                clean_empty_dirs_in_directory "$selected_dir"
                ;;
            0)
                return 0
                ;;
            *)
                echo -e "${RED}❌ 无效选项${NC}"
                ;;
        esac
    else
        echo -e "${RED}❌ 无效的目录选择${NC}"
    fi
}

# 全局快速清理
global_quick_cleanup() {
    echo -e "${PURPLE}🧹 开始全局快速清理...${NC}"
    echo
    
    echo -e "${YELLOW}⚠️ 这将清理整个 NAS 的临时文件和空目录${NC}"
    read -p "确认继续吗？(y/N): " confirm
    
    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}⏭️ 已取消全局清理${NC}"
        return 0
    fi
    
    echo -e "${BLUE}第1步: 清理全局临时文件${NC}"
    
    local temp_patterns=(
        "*.tmp"
        "*.temp"
        "*.cache"
        ".DS_Store"
        "Thumbs.db"
        "desktop.ini"
    )
    
    local total_removed=0
    
    for pattern in "${temp_patterns[@]}"; do
        echo -e "${YELLOW}  正在查找 $pattern 文件...${NC}"
        
        local count
        count=$(execute_remote_command "find $NAS_REMOTE_PATH -name '$pattern' -type f 2>/dev/null | wc -l")
        
        if [ "$count" -gt 0 ]; then
            echo "    发现 $count 个 $pattern 文件"
            
            read -p "    删除这些文件吗？(y/N): " confirm
            if [[ $confirm =~ ^[Yy]$ ]]; then
                execute_remote_command "find $NAS_REMOTE_PATH -name '$pattern' -type f -delete 2>/dev/null" "正在删除文件..."
                total_removed=$((total_removed + count))
                echo -e "    ${GREEN}✅ 已删除 $count 个文件${NC}"
            else
                echo -e "    ${YELLOW}⏭️ 跳过删除${NC}"
            fi
        fi
    done
    
    echo -e "${BLUE}第2步: 清理全局空目录${NC}"
    
    local empty_count
    empty_count=$(execute_remote_command "find $NAS_REMOTE_PATH -type d -empty 2>/dev/null | wc -l")
    
    if [ "$empty_count" -gt 0 ]; then
        echo "发现 $empty_count 个空目录"
        read -p "删除这些空目录吗？(y/N): " confirm
        if [[ $confirm =~ ^[Yy]$ ]]; then
            execute_remote_command "find $NAS_REMOTE_PATH -type d -empty -delete 2>/dev/null" "正在删除空目录..."
            echo -e "${GREEN}✅ 空目录清理完成${NC}"
        else
            echo -e "${YELLOW}⏭️ 跳过删除空目录${NC}"
        fi
    else
        echo -e "${BLUE}ℹ️ 没有发现空目录${NC}"
    fi
    
    echo -e "${GREEN}🎉 全局清理完成！${NC}"
    if [ "$total_removed" -gt 0 ]; then
        echo -e "${GREEN}删除了 $total_removed 个临时文件${NC}"
    fi
    echo
}

# 显示菜单
show_menu() {
    echo -e "${PURPLE}请选择操作:${NC}"
    echo -e "${CYAN}  1)${NC} 🔍 分目录快速扫描"
    echo -e "${CYAN}  2)${NC} 📂 选择目录进行清理"
    echo -e "${CYAN}  3)${NC} 🧹 全局快速清理"
    echo -e "${CYAN}  4)${NC} 📊 查看磁盘使用情况"
    echo -e "${CYAN}  5)${NC} 📁 查看目录结构"
    echo -e "${CYAN}  6)${NC} 🔗 测试连接"
    echo -e "${CYAN}  0)${NC} 🚪 退出"
    echo
}

# 主函数
main() {
    # 加载连接配置
    load_connection_config
    
    # 显示横幅
    show_banner
    
    # 测试连接
    if ! test_ssh_connection; then
        echo -e "${RED}❌ 无法连接到 NAS，程序退出${NC}"
        exit 1
    fi
    
    echo
    
    # 显示磁盘使用情况
    show_remote_disk_usage
    
    # 主循环
    while true; do
        show_menu
        read -p "请输入选项 (0-6): " choice
        echo
        
        case $choice in
            1)
                quick_scan_by_directory
                ;;
            2)
                select_directory_for_cleanup
                ;;
            3)
                global_quick_cleanup
                ;;
            4)
                show_remote_disk_usage
                ;;
            5)
                get_main_directories
                ;;
            6)
                test_ssh_connection
                ;;
            0)
                echo -e "${GREEN}👋 感谢使用远程 NAS 清理工具！${NC}"
                log_message "清理会话结束"
                exit 0
                ;;
            *)
                echo -e "${RED}❌ 无效选项，请重新选择${NC}"
                echo
                ;;
        esac
        
        # 暂停，等待用户按键
        read -p "按回车键继续..."
        echo
    done
}

# 检查是否直接运行脚本
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi