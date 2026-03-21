#!/bin/bash

# 音乐文件分析和整理脚本
# 专门用于处理NAS中的音乐收藏，包括古典音乐等

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# 进度条相关变量
PROGRESS_BAR_WIDTH=50
PROGRESS_CHAR="█"
EMPTY_CHAR="░"

# 配置变量
MUSIC_PATH="/volume1/music"
LOG_DIR="./logs"
REPORT_DIR="./reports"
TEMP_DIR="/tmp/music_analysis"

# 音乐文件扩展名
MUSIC_EXTENSIONS=("mp3" "flac" "wav" "aac" "m4a" "ogg" "wma" "ape" "dsd" "dsf" "dff")

# 创建必要目录
mkdir -p "$LOG_DIR" "$REPORT_DIR" "$TEMP_DIR"

# 日志文件
LOG_FILE="$LOG_DIR/music_analysis_$(date +%Y%m%d_%H%M%S).log"

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

# 日志记录函数
log_message() {
    local level=$1
    local message="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message" | tee -a "$LOG_FILE"
}

# 显示标题
show_header() {
    clear
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                  🎵 NAS 音乐文件分析整理工具                 ║"
    echo "║                                                              ║"
    echo "║  专业音乐收藏管理 • 格式分析 • 重复检测 • 目录优化           ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}\n"
}

# 检查音乐目录是否存在
check_music_directory() {
    if [ ! -d "$MUSIC_PATH" ]; then
        echo -e "${RED}❌ 音乐目录不存在: $MUSIC_PATH${NC}"
        echo -e "${YELLOW}💡 请检查路径或修改脚本中的 MUSIC_PATH 变量${NC}"
        exit 1
    fi
    
    log_message "INFO" "音乐目录检查通过: $MUSIC_PATH"
    echo -e "${GREEN}✅ 音乐目录: $MUSIC_PATH${NC}"
}

# 分析音乐文件格式分布
analyze_music_formats() {
    echo -e "\n${BLUE}🔍 分析音乐文件格式分布...${NC}"
    
    local format_file="$TEMP_DIR/formats.txt"
    local total_files=0
    
    # 统计各种格式的文件数量
    for ext in "${MUSIC_EXTENSIONS[@]}"; do
        show_progress $((total_files + 1)) ${#MUSIC_EXTENSIONS[@]} "扫描 .$ext 文件"
        local count=$(find "$MUSIC_PATH" -type f -iname "*.$ext" 2>/dev/null | wc -l)
        if [ $count -gt 0 ]; then
            echo "$ext:$count" >> "$format_file"
            total_files=$((total_files + count))
        fi
    done
    
    complete_progress "格式分析完成"
    
    echo -e "\n${CYAN}📊 音乐文件格式统计:${NC}"
    if [ -f "$format_file" ]; then
        while IFS=':' read -r format count; do
            printf "  %-6s: %8d 个文件\n" ".$format" "$count"
        done < "$format_file" | sort -k3 -nr
        echo -e "${GREEN}📈 总计: $total_files 个音乐文件${NC}"
    else
        echo -e "${YELLOW}⚠️  未找到音乐文件${NC}"
    fi
    
    log_message "INFO" "音乐格式分析完成，总计 $total_files 个文件"
}

# 分析目录结构
analyze_directory_structure() {
    echo -e "\n${BLUE}📁 分析目录结构...${NC}"
    
    local structure_file="$TEMP_DIR/structure.txt"
    
    # 分析目录深度和文件分布
    find "$MUSIC_PATH" -type d | while read -r dir; do
        local depth=$(echo "$dir" | tr -cd '/' | wc -c)
        local file_count=$(find "$dir" -maxdepth 1 -type f \( $(printf " -iname '*.%s' -o" "${MUSIC_EXTENSIONS[@]}" | sed 's/ -o$//') \) 2>/dev/null | wc -l)
        if [ $file_count -gt 0 ]; then
            echo "$depth:$file_count:$dir" >> "$structure_file"
        fi
    done
    
    echo -e "\n${CYAN}🗂️  目录结构分析:${NC}"
    if [ -f "$structure_file" ]; then
        echo -e "${YELLOW}📊 按文件数量排序的目录:${NC}"
        sort -t':' -k2 -nr "$structure_file" | head -20 | while IFS=':' read -r depth count path; do
            local relative_path=${path#$MUSIC_PATH}
            [ -z "$relative_path" ] && relative_path="/"
            printf "  %4d 个文件 - %s\n" "$count" "$relative_path"
        done
        
        echo -e "\n${YELLOW}📏 目录深度分析:${NC}"
        awk -F':' '{print $1}' "$structure_file" | sort -n | uniq -c | while read -r count depth; do
            printf "  深度 %d: %d 个目录\n" "$depth" "$count"
        done
    fi
    
    log_message "INFO" "目录结构分析完成"
}

# 查找重复音乐文件
find_duplicate_music() {
    echo -e "\n${BLUE}🔍 查找重复音乐文件...${NC}"
    
    local duplicate_file="$TEMP_DIR/duplicates.txt"
    local hash_file="$TEMP_DIR/hashes.txt"
    
    # 计算音乐文件的MD5哈希值
    echo -e "${YELLOW}🔢 计算文件哈希值...${NC}"
    find "$MUSIC_PATH" -type f \( $(printf " -iname '*.%s' -o" "${MUSIC_EXTENSIONS[@]}" | sed 's/ -o$//') \) -exec md5sum {} \; 2>/dev/null > "$hash_file"
    
    # 查找重复的哈希值
    if [ -f "$hash_file" ]; then
        awk '{print $1}' "$hash_file" | sort | uniq -d > "$TEMP_DIR/dup_hashes.txt"
        
        if [ -s "$TEMP_DIR/dup_hashes.txt" ]; then
            echo -e "\n${RED}🚨 发现重复文件:${NC}"
            while read -r hash; do
                echo -e "\n${YELLOW}哈希值: $hash${NC}"
                grep "^$hash" "$hash_file" | while read -r h file; do
                    local size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
                    local size_mb=$((size / 1024 / 1024))
                    echo "  📄 $file (${size_mb}MB)"
                done
            done < "$TEMP_DIR/dup_hashes.txt" | tee "$duplicate_file"
            
            local dup_count=$(wc -l < "$TEMP_DIR/dup_hashes.txt")
            echo -e "\n${GREEN}📊 总计发现 $dup_count 组重复文件${NC}"
        else
            echo -e "${GREEN}✅ 未发现重复的音乐文件${NC}"
        fi
    fi
    
    log_message "INFO" "重复文件检查完成"
}

# 分析音乐文件大小分布
analyze_file_sizes() {
    echo -e "\n${BLUE}📏 分析文件大小分布...${NC}"
    
    local size_file="$TEMP_DIR/sizes.txt"
    
    # 收集文件大小信息
    find "$MUSIC_PATH" -type f \( $(printf " -iname '*.%s' -o" "${MUSIC_EXTENSIONS[@]}" | sed 's/ -o$//') \) -exec stat -f"%z %N" {} \; 2>/dev/null > "$size_file" || \
    find "$MUSIC_PATH" -type f \( $(printf " -iname '*.%s' -o" "${MUSIC_EXTENSIONS[@]}" | sed 's/ -o$//') \) -exec stat -c"%s %n" {} \; 2>/dev/null > "$size_file"
    
    if [ -f "$size_file" ] && [ -s "$size_file" ]; then
        echo -e "\n${CYAN}📊 文件大小分布:${NC}"
        
        # 按大小分类统计
        local tiny=0 small=0 medium=0 large=0 huge=0
        local total_size=0
        
        while read -r size file; do
            total_size=$((total_size + size))
            local size_mb=$((size / 1024 / 1024))
            
            if [ $size_mb -lt 5 ]; then
                tiny=$((tiny + 1))
            elif [ $size_mb -lt 20 ]; then
                small=$((small + 1))
            elif [ $size_mb -lt 50 ]; then
                medium=$((medium + 1))
            elif [ $size_mb -lt 100 ]; then
                large=$((large + 1))
            else
                huge=$((huge + 1))
            fi
        done < "$size_file"
        
        local total_gb=$((total_size / 1024 / 1024 / 1024))
        
        printf "  🔹 微小文件 (<5MB):   %6d 个\n" "$tiny"
        printf "  🔸 小文件 (5-20MB):   %6d 个\n" "$small"
        printf "  🔶 中等文件 (20-50MB): %6d 个\n" "$medium"
        printf "  🔷 大文件 (50-100MB): %6d 个\n" "$large"
        printf "  🔺 超大文件 (>100MB): %6d 个\n" "$huge"
        echo -e "\n${GREEN}💾 总存储空间: ${total_gb}GB${NC}"
        
        # 显示最大的文件
        echo -e "\n${YELLOW}🏆 最大的音乐文件:${NC}"
        sort -nr "$size_file" | head -10 | while read -r size file; do
            local size_mb=$((size / 1024 / 1024))
            local basename=$(basename "$file")
            printf "  %4dMB - %s\n" "$size_mb" "$basename"
        done
    fi
    
    log_message "INFO" "文件大小分析完成"
}

# 检查音乐文件命名规范
check_naming_conventions() {
    echo -e "\n${BLUE}📝 检查文件命名规范...${NC}"
    
    local naming_issues="$TEMP_DIR/naming_issues.txt"
    
    # 检查常见的命名问题
    echo -e "${YELLOW}🔍 检查命名问题...${NC}"
    
    # 查找包含特殊字符的文件
    find "$MUSIC_PATH" -type f \( $(printf " -iname '*.%s' -o" "${MUSIC_EXTENSIONS[@]}" | sed 's/ -o$//') \) | while read -r file; do
        local basename=$(basename "$file")
        
        # 检查各种命名问题
        if [[ "$basename" =~ [[:space:]]{2,} ]]; then
            echo "多余空格: $file" >> "$naming_issues"
        fi
        
        if [[ "$basename" =~ ^[[:space:]] ]] || [[ "$basename" =~ [[:space:]]\. ]]; then
            echo "前后空格: $file" >> "$naming_issues"
        fi
        
        if [[ "$basename" =~ [\[\]\(\)\{\}] ]]; then
            echo "特殊括号: $file" >> "$naming_issues"
        fi
        
        if [[ "$basename" =~ [^[:print:]] ]]; then
            echo "非打印字符: $file" >> "$naming_issues"
        fi
    done
    
    if [ -f "$naming_issues" ] && [ -s "$naming_issues" ]; then
        echo -e "\n${RED}⚠️  发现命名问题:${NC}"
        head -20 "$naming_issues" | while read -r line; do
            echo "  $line"
        done
        
        local issue_count=$(wc -l < "$naming_issues")
        if [ $issue_count -gt 20 ]; then
            echo -e "  ${YELLOW}... 还有 $((issue_count - 20)) 个问题${NC}"
        fi
    else
        echo -e "${GREEN}✅ 文件命名规范良好${NC}"
    fi
    
    log_message "INFO" "命名规范检查完成"
}

# 生成HTML报告
generate_html_report() {
    echo -e "\n${BLUE}📄 生成分析报告...${NC}"
    
    local report_file="$REPORT_DIR/music_analysis_$(date +%Y%m%d_%H%M%S).html"
    
    cat > "$report_file" << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NAS 音乐文件分析报告</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; background: #f5f7fa; }
        .container { max-width: 1200px; margin: 0 auto; background: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center; }
        .content { padding: 30px; }
        .section { margin-bottom: 30px; padding: 20px; border: 1px solid #e1e8ed; border-radius: 8px; }
        .section h2 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
        .stat-card { background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; border-left: 4px solid #3498db; }
        .stat-number { font-size: 2em; font-weight: bold; color: #2c3e50; }
        .stat-label { color: #7f8c8d; margin-top: 5px; }
        .file-list { max-height: 300px; overflow-y: auto; background: #f8f9fa; padding: 15px; border-radius: 5px; }
        .progress-bar { background: #ecf0f1; border-radius: 10px; overflow: hidden; margin: 10px 0; }
        .progress-fill { background: linear-gradient(90deg, #3498db, #2ecc71); height: 20px; border-radius: 10px; }
        .timestamp { color: #7f8c8d; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎵 NAS 音乐文件分析报告</h1>
            <p class="timestamp">生成时间: $(date '+%Y-%m-%d %H:%M:%S')</p>
        </div>
        <div class="content">
EOF

    # 添加格式统计
    if [ -f "$TEMP_DIR/formats.txt" ]; then
        echo '            <div class="section">' >> "$report_file"
        echo '                <h2>📊 音乐格式分布</h2>' >> "$report_file"
        echo '                <div class="stats">' >> "$report_file"
        
        while IFS=':' read -r format count; do
            cat >> "$report_file" << EOF
                    <div class="stat-card">
                        <div class="stat-number">$count</div>
                        <div class="stat-label">.$format 文件</div>
                    </div>
EOF
        done < "$TEMP_DIR/formats.txt"
        
        echo '                </div>' >> "$report_file"
        echo '            </div>' >> "$report_file"
    fi
    
    # 添加大小分析
    echo '            <div class="section">' >> "$report_file"
    echo '                <h2>💾 存储空间分析</h2>' >> "$report_file"
    echo '                <p>详细的文件大小分布和存储使用情况</p>' >> "$report_file"
    echo '            </div>' >> "$report_file"
    
    # 结束HTML
    cat >> "$report_file" << 'EOF'
        </div>
    </div>
</body>
</html>
EOF

    echo -e "${GREEN}✅ 报告已生成: $report_file${NC}"
    log_message "INFO" "HTML报告生成完成: $report_file"
}

# 清理临时文件
cleanup_temp_files() {
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
        log_message "INFO" "临时文件清理完成"
    fi
}

# 显示菜单
show_menu() {
    echo -e "\n${CYAN}🎵 音乐文件分析选项:${NC}"
    echo "  1) 📊 分析音乐格式分布"
    echo "  2) 📁 分析目录结构"
    echo "  3) 🔍 查找重复文件"
    echo "  4) 📏 分析文件大小"
    echo "  5) 📝 检查命名规范"
    echo "  6) 🚀 完整分析 (全部功能)"
    echo "  7) 📄 生成HTML报告"
    echo "  8) ⚙️  配置设置"
    echo "  9) 🚪 退出"
    echo ""
}

# 配置设置
configure_settings() {
    echo -e "\n${YELLOW}⚙️  当前配置:${NC}"
    echo "  音乐路径: $MUSIC_PATH"
    echo "  日志目录: $LOG_DIR"
    echo "  报告目录: $REPORT_DIR"
    echo ""
    
    read -p "是否要修改音乐路径? (y/N): " change_path
    if [[ $change_path =~ ^[Yy]$ ]]; then
        read -p "请输入新的音乐路径: " new_path
        if [ -d "$new_path" ]; then
            MUSIC_PATH="$new_path"
            echo -e "${GREEN}✅ 音乐路径已更新: $MUSIC_PATH${NC}"
        else
            echo -e "${RED}❌ 路径不存在: $new_path${NC}"
        fi
    fi
}

# 完整分析
full_analysis() {
    echo -e "\n${PURPLE}🚀 开始完整音乐文件分析...${NC}"
    
    analyze_music_formats
    analyze_directory_structure
    find_duplicate_music
    analyze_file_sizes
    check_naming_conventions
    generate_html_report
    
    echo -e "\n${GREEN}🎉 完整分析完成！${NC}"
}

# 主函数
main() {
    show_header
    check_music_directory
    
    while true; do
        show_menu
        read -p "请选择操作 (1-9): " choice
        
        case $choice in
            1) analyze_music_formats ;;
            2) analyze_directory_structure ;;
            3) find_duplicate_music ;;
            4) analyze_file_sizes ;;
            5) check_naming_conventions ;;
            6) full_analysis ;;
            7) generate_html_report ;;
            8) configure_settings ;;
            9) 
                echo -e "\n${GREEN}👋 感谢使用音乐文件分析工具！${NC}"
                cleanup_temp_files
                exit 0
                ;;
            *) 
                echo -e "${RED}❌ 无效选择，请输入 1-9${NC}"
                ;;
        esac
        
        echo ""
        read -p "按 Enter 继续..."
    done
}

# 信号处理
trap 'echo -e "\n${YELLOW}操作被中断${NC}"; cleanup_temp_files; exit 1' INT TERM

# 运行主函数
main "$@"