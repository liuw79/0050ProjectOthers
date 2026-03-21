#!/bin/bash

# NAS 快速清理脚本
# 提供常见的快速清理操作，无需复杂配置

# 配置变量
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/nas_config.conf"
NAS_PATH="/volume1"  # 默认路径，会从配置文件读取

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 读取配置文件
load_config() {
    if [ -f "$CONFIG_FILE" ]; then
        # 读取配置文件中的 NAS_PATH
        local config_nas_path
        config_nas_path=$(grep '^NAS_PATH=' "$CONFIG_FILE" | cut -d'=' -f2 | tr -d '"')
        if [ -n "$config_nas_path" ]; then
            NAS_PATH="$config_nas_path"
        fi
    fi
}

# 显示横幅
show_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🧹 NAS 快速清理工具                        ║"
    echo "║                                                              ║"
    echo "║  快速清理您的 NAS 存储空间，释放磁盘容量                        ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${BLUE}当前 NAS 路径: ${YELLOW}$NAS_PATH${NC}"
    echo
}

# 显示磁盘使用情况
show_disk_usage() {
    echo -e "${BLUE}📊 当前磁盘使用情况:${NC}"
    if [ -d "$NAS_PATH" ]; then
        df -h "$NAS_PATH" | awk 'NR==2 {printf "使用: %s / %s (%s)\n", $3, $2, $5}'
    else
        echo -e "${RED}❌ NAS 路径不存在: $NAS_PATH${NC}"
        return 1
    fi
    echo
}

# 快速扫描
quick_scan() {
    echo -e "${BLUE}🔍 快速扫描存储空间...${NC}"
    
    if [ ! -d "$NAS_PATH" ]; then
        echo -e "${RED}❌ NAS 路径不存在: $NAS_PATH${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}正在扫描，请稍候...${NC}"
    
    # 统计各类文件
    local temp_files
    local large_files
    local empty_dirs
    local duplicate_count
    
    # 临时文件
    temp_files=$(find "$NAS_PATH" \( -name "*.tmp" -o -name "*.temp" -o -name "*.cache" -o -name ".DS_Store" -o -name "Thumbs.db" \) -type f 2>/dev/null | wc -l)
    
    # 大文件 (>100MB)
    large_files=$(find "$NAS_PATH" -type f -size +100M 2>/dev/null | wc -l)
    
    # 空目录
    empty_dirs=$(find "$NAS_PATH" -type d -empty 2>/dev/null | wc -l)
    
    # 显示结果
    echo -e "${GREEN}📋 扫描结果:${NC}"
    echo -e "  🗑️  临时文件: ${YELLOW}$temp_files${NC} 个"
    echo -e "  📦 大文件 (>100MB): ${YELLOW}$large_files${NC} 个"
    echo -e "  📁 空目录: ${YELLOW}$empty_dirs${NC} 个"
    echo
}

# 清理临时文件
clean_temp_files() {
    echo -e "${BLUE}🗑️ 清理临时文件...${NC}"
    
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
    local total_size=0
    
    for pattern in "${temp_patterns[@]}"; do
        echo -e "${YELLOW}  正在查找 $pattern 文件...${NC}"
        
        local files
        files=$(find "$NAS_PATH" -name "$pattern" -type f 2>/dev/null)
        
        if [ -n "$files" ]; then
            local count
            count=$(echo "$files" | wc -l)
            
            echo "    发现 $count 个 $pattern 文件"
            
            # 计算大小
            local size
            size=$(echo "$files" | xargs -r ls -l 2>/dev/null | awk '{sum+=$5} END {print sum+0}')
            
            if [ "$size" -gt 0 ]; then
                local size_mb=$((size / 1024 / 1024))
                echo "    总大小: ${size_mb} MB"
                
                read -p "    删除这些文件吗？(y/N): " confirm
                if [[ $confirm =~ ^[Yy]$ ]]; then
                    echo "$files" | xargs -r rm -f
                    total_removed=$((total_removed + count))
                    total_size=$((total_size + size))
                    echo -e "    ${GREEN}✅ 已删除 $count 个文件${NC}"
                else
                    echo -e "    ${YELLOW}⏭️ 跳过删除${NC}"
                fi
            fi
        fi
    done
    
    if [ "$total_removed" -gt 0 ]; then
        local total_size_mb=$((total_size / 1024 / 1024))
        echo -e "${GREEN}🎉 清理完成！删除了 $total_removed 个文件，释放了 ${total_size_mb} MB 空间${NC}"
    else
        echo -e "${BLUE}ℹ️ 没有找到需要清理的临时文件${NC}"
    fi
    echo
}

# 清理空目录
clean_empty_dirs() {
    echo -e "${BLUE}📁 清理空目录...${NC}"
    
    local empty_dirs
    empty_dirs=$(find "$NAS_PATH" -type d -empty 2>/dev/null)
    
    if [ -z "$empty_dirs" ]; then
        echo -e "${BLUE}ℹ️ 没有发现空目录${NC}"
        echo
        return 0
    fi
    
    local count
    count=$(echo "$empty_dirs" | wc -l)
    
    echo "发现 $count 个空目录:"
    echo "$empty_dirs" | head -10
    
    if [ "$count" -gt 10 ]; then
        echo "... 还有 $((count - 10)) 个目录"
    fi
    
    read -p "删除这些空目录吗？(y/N): " confirm
    if [[ $confirm =~ ^[Yy]$ ]]; then
        echo "$empty_dirs" | xargs -r rmdir 2>/dev/null
        echo -e "${GREEN}✅ 空目录清理完成${NC}"
    else
        echo -e "${YELLOW}⏭️ 跳过删除空目录${NC}"
    fi
    echo
}

# 查找大文件
find_large_files() {
    echo -e "${BLUE}📦 查找大文件 (>100MB)...${NC}"
    
    local large_files
    large_files=$(find "$NAS_PATH" -type f -size +100M -exec ls -lh {} \; 2>/dev/null | \
        awk '{print $5 "\t" $9}' | sort -hr | head -20)
    
    if [ -z "$large_files" ]; then
        echo -e "${BLUE}ℹ️ 没有发现大文件 (>100MB)${NC}"
        echo
        return 0
    fi
    
    echo "发现的大文件 (前20个):"
    echo -e "${YELLOW}大小\t\t文件路径${NC}"
    echo "$large_files"
    echo
    
    echo -e "${CYAN}💡 建议操作:${NC}"
    echo "  1. 检查是否还需要这些大文件"
    echo "  2. 考虑压缩不常用的大文件"
    echo "  3. 将旧文件移动到归档存储"
    echo
}

# 查找重复文件（简化版）
find_duplicates_simple() {
    echo -e "${BLUE}🔍 查找重复文件（按大小）...${NC}"
    
    echo -e "${YELLOW}正在扫描，这可能需要一些时间...${NC}"
    
    # 按文件大小查找可能的重复文件
    local duplicates
    duplicates=$(find "$NAS_PATH" -type f -exec ls -l {} \; 2>/dev/null | \
        awk '{print $5 "\t" $9}' | sort -n | uniq -d -w 10 | head -20)
    
    if [ -z "$duplicates" ]; then
        echo -e "${BLUE}ℹ️ 没有发现明显的重复文件${NC}"
        echo
        return 0
    fi
    
    echo "发现可能的重复文件（相同大小）:"
    echo -e "${YELLOW}大小\t\t文件路径${NC}"
    echo "$duplicates"
    echo
    
    echo -e "${CYAN}💡 建议:${NC}"
    echo "  1. 手动检查这些文件是否真的重复"
    echo "  2. 使用专业工具进行精确的重复文件检测"
    echo "  3. 保留一份，删除其他副本"
    echo
}

# 显示目录大小排行
show_directory_sizes() {
    echo -e "${BLUE}📊 目录大小排行 (前10个)...${NC}"
    
    echo -e "${YELLOW}正在计算目录大小...${NC}"
    
    local dir_sizes
    dir_sizes=$(du -h "$NAS_PATH"/* 2>/dev/null | sort -hr | head -10)
    
    if [ -n "$dir_sizes" ]; then
        echo -e "${YELLOW}大小\t\t目录${NC}"
        echo "$dir_sizes"
    else
        echo -e "${BLUE}ℹ️ 无法获取目录大小信息${NC}"
    fi
    echo
}

# 系统清理（清理系统生成的文件）
system_cleanup() {
    echo -e "${BLUE}🔧 系统文件清理...${NC}"
    
    local system_files=(
        ".DS_Store"
        "Thumbs.db"
        "desktop.ini"
        ".Spotlight-V100"
        ".Trashes"
        ".fseventsd"
        "@eaDir"
    )
    
    local total_removed=0
    
    for file_pattern in "${system_files[@]}"; do
        echo -e "${YELLOW}  正在查找 $file_pattern...${NC}"
        
        local files
        if [[ "$file_pattern" == "@eaDir" ]]; then
            files=$(find "$NAS_PATH" -name "$file_pattern" -type d 2>/dev/null)
        else
            files=$(find "$NAS_PATH" -name "$file_pattern" 2>/dev/null)
        fi
        
        if [ -n "$files" ]; then
            local count
            count=$(echo "$files" | wc -l)
            echo "    发现 $count 个 $file_pattern"
            
            read -p "    删除这些系统文件吗？(y/N): " confirm
            if [[ $confirm =~ ^[Yy]$ ]]; then
                if [[ "$file_pattern" == "@eaDir" ]]; then
                    echo "$files" | xargs -r rm -rf
                else
                    echo "$files" | xargs -r rm -f
                fi
                total_removed=$((total_removed + count))
                echo -e "    ${GREEN}✅ 已删除 $count 个项目${NC}"
            else
                echo -e "    ${YELLOW}⏭️ 跳过删除${NC}"
            fi
        fi
    done
    
    if [ "$total_removed" -gt 0 ]; then
        echo -e "${GREEN}🎉 系统清理完成！删除了 $total_removed 个项目${NC}"
    else
        echo -e "${BLUE}ℹ️ 没有找到需要清理的系统文件${NC}"
    fi
    echo
}

# 显示菜单
show_menu() {
    echo -e "${PURPLE}请选择操作:${NC}"
    echo -e "${CYAN}  1)${NC} 🔍 快速扫描"
    echo -e "${CYAN}  2)${NC} 🗑️  清理临时文件"
    echo -e "${CYAN}  3)${NC} 📁 清理空目录"
    echo -e "${CYAN}  4)${NC} 📦 查找大文件"
    echo -e "${CYAN}  5)${NC} 🔍 查找重复文件"
    echo -e "${CYAN}  6)${NC} 📊 目录大小排行"
    echo -e "${CYAN}  7)${NC} 🔧 系统文件清理"
    echo -e "${CYAN}  8)${NC} 🧹 一键清理 (临时文件 + 空目录 + 系统文件)"
    echo -e "${CYAN}  9)${NC} ⚙️  配置设置"
    echo -e "${CYAN}  0)${NC} 🚪 退出"
    echo
}

# 一键清理
one_click_cleanup() {
    echo -e "${PURPLE}🧹 开始一键清理...${NC}"
    echo
    
    echo -e "${BLUE}第1步: 清理临时文件${NC}"
    clean_temp_files
    
    echo -e "${BLUE}第2步: 清理空目录${NC}"
    clean_empty_dirs
    
    echo -e "${BLUE}第3步: 清理系统文件${NC}"
    system_cleanup
    
    echo -e "${GREEN}🎉 一键清理完成！${NC}"
    echo
}

# 配置设置
config_settings() {
    echo -e "${BLUE}⚙️ 配置设置${NC}"
    echo
    echo -e "当前 NAS 路径: ${YELLOW}$NAS_PATH${NC}"
    echo
    echo "1) 修改 NAS 路径"
    echo "2) 编辑配置文件"
    echo "3) 返回主菜单"
    echo
    
    read -p "请选择 (1-3): " config_choice
    
    case $config_choice in
        1)
            read -p "请输入新的 NAS 路径: " new_path
            if [ -d "$new_path" ]; then
                NAS_PATH="$new_path"
                echo -e "${GREEN}✅ NAS 路径已更新为: $NAS_PATH${NC}"
            else
                echo -e "${RED}❌ 路径不存在: $new_path${NC}"
            fi
            ;;
        2)
            if command -v nano &> /dev/null; then
                nano "$CONFIG_FILE"
            elif command -v vim &> /dev/null; then
                vim "$CONFIG_FILE"
            else
                echo -e "${YELLOW}请手动编辑配置文件: $CONFIG_FILE${NC}"
            fi
            ;;
        3)
            return
            ;;
        *)
            echo -e "${RED}❌ 无效选项${NC}"
            ;;
    esac
    echo
}

# 主函数
main() {
    # 加载配置
    load_config
    
    # 显示横幅
    show_banner
    
    # 显示磁盘使用情况
    show_disk_usage
    
    # 主循环
    while true; do
        show_menu
        read -p "请输入选项 (0-9): " choice
        echo
        
        case $choice in
            1)
                quick_scan
                ;;
            2)
                clean_temp_files
                ;;
            3)
                clean_empty_dirs
                ;;
            4)
                find_large_files
                ;;
            5)
                find_duplicates_simple
                ;;
            6)
                show_directory_sizes
                ;;
            7)
                system_cleanup
                ;;
            8)
                one_click_cleanup
                ;;
            9)
                config_settings
                ;;
            0)
                echo -e "${GREEN}👋 感谢使用 NAS 快速清理工具！${NC}"
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