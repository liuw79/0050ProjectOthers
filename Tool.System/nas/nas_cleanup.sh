#!/bin/bash

# NAS 文件清理和整理脚本
# 用于分析、清理和优化 NAS 存储空间

# 配置变量
NAS_PATH="/volume1"  # 默认群晖 NAS 路径，请根据实际情况修改
LOG_FILE="/tmp/nas_cleanup.log"
REPORT_FILE="/tmp/nas_report.html"
MIN_FILE_SIZE="100M"  # 查找大于此大小的文件
DUPLICATE_THRESHOLD=2  # 重复文件数量阈值

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 进度条相关变量
PROGRESS_BAR_WIDTH=50
PROGRESS_CHAR="█"
EMPTY_CHAR="░"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
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

# 检查依赖
check_dependencies() {
    log_info "检查必要的依赖工具..."
    
    local missing_tools=()
    
    # 检查基本工具
    for tool in find du sort awk sed grep; do
        if ! command -v "$tool" &> /dev/null; then
            missing_tools+=("$tool")
        fi
    done
    
    # 检查可选工具
    if ! command -v fdupes &> /dev/null; then
        log_warn "fdupes 未安装，将使用替代方法查找重复文件"
    fi
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        log_error "缺少必要工具: ${missing_tools[*]}"
        return 1
    fi
    
    log_success "依赖检查完成"
    return 0
}

# 分析磁盘使用情况
analyze_disk_usage() {
    log_info "分析磁盘使用情况..."
    
    echo "=== 磁盘使用情况分析 ===" >> "$LOG_FILE"
    
    echo -e "${YELLOW}📊 磁盘分析进度:${NC}"
    
    # 步骤1: 总体磁盘使用情况
    show_progress 1 2 "获取磁盘使用情况"
    df -h "$NAS_PATH" | tee -a "$LOG_FILE" > /dev/null
    
    # 步骤2: 各目录大小排序
    show_progress 2 2 "分析目录大小"
    echo "\n=== 最大的20个目录 ===" >> "$LOG_FILE"
    du -h "$NAS_PATH"/* 2>/dev/null | sort -hr | head -20 | tee -a "$LOG_FILE" > /dev/null
    
    complete_progress "磁盘分析完成"
    
    # 显示结果
    echo -e "\n${CYAN}=== 磁盘使用情况 ===${NC}"
    df -h "$NAS_PATH"
    echo -e "\n${CYAN}=== 最大的20个目录 ===${NC}"
    du -h "$NAS_PATH"/* 2>/dev/null | sort -hr | head -20
    
    log_success "磁盘使用情况分析完成"
}

# 查找大文件
find_large_files() {
    log_info "查找大文件（大于 $MIN_FILE_SIZE）..."
    
    echo "\n=== 大文件列表 ===" >> "$LOG_FILE"
    
    echo -e "${YELLOW}🔍 大文件扫描进度:${NC}"
    
    # 步骤1: 查找大文件
    show_progress 1 3 "扫描大文件"
    local large_files=$(find "$NAS_PATH" -type f -size +"$MIN_FILE_SIZE" -exec ls -lh {} \; 2>/dev/null)
    
    # 步骤2: 格式化输出
    show_progress 2 3 "格式化文件列表"
    local formatted_files=$(echo "$large_files" | awk '{print $5 "\t" $9}')
    
    # 步骤3: 排序并限制数量
    show_progress 3 3 "排序文件列表"
    local sorted_files=$(echo "$formatted_files" | sort -hr | head -50)
    
    complete_progress "大文件扫描完成"
    
    # 显示结果
    echo -e "\n${CYAN}=== 大文件列表 (>${MIN_FILE_SIZE}) ===${NC}"
    echo "$sorted_files" | tee -a "$LOG_FILE"
    
    local file_count=$(echo "$sorted_files" | grep -c '^' 2>/dev/null || echo "0")
    echo -e "\n${BLUE}📈 统计: 找到 $file_count 个大文件${NC}"
    
    log_success "大文件查找完成，找到 $file_count 个文件"
}

# 查找重复文件
find_duplicate_files() {
    log_info "查找重复文件..."
    
    echo "\n=== 重复文件分析 ===" >> "$LOG_FILE"
    
    echo -e "${YELLOW}🔍 重复文件扫描进度 (这可能需要较长时间):${NC}"
    
    if command -v fdupes &> /dev/null; then
        # 使用 fdupes 查找重复文件
        show_progress 1 1 "使用fdupes扫描重复文件"
        local duplicates=$(fdupes -r "$NAS_PATH" 2>/dev/null)
        complete_progress "fdupes扫描完成"
    else
        # 使用 MD5 校验和查找重复文件
        log_info "使用 MD5 校验和查找重复文件（可能需要较长时间）..."
        
        # 步骤1: 计算MD5
        show_progress 1 3 "计算文件MD5值"
        local md5_results=$(find "$NAS_PATH" -type f -exec md5sum {} \; 2>/dev/null)
        
        # 步骤2: 排序
        show_progress 2 3 "排序MD5结果"
        local sorted_md5=$(echo "$md5_results" | sort)
        
        # 步骤3: 查找重复
        show_progress 3 3 "查找重复文件"
        local duplicates=$(echo "$sorted_md5" | uniq -w32 -dD)
        complete_progress "MD5扫描完成"
    fi
    
    # 显示结果
    echo -e "\n${CYAN}=== 重复文件列表 ===${NC}"
    if [[ -z "$duplicates" ]]; then
        echo -e "${GREEN}✅ 没有找到重复文件${NC}"
    else
        echo "$duplicates" | tee -a "$LOG_FILE"
        local dup_count=$(echo "$duplicates" | grep -c '^' 2>/dev/null || echo "0")
        echo -e "\n${BLUE}📈 统计: 找到 $dup_count 个重复文件${NC}"
    fi
    
    log_success "重复文件查找完成"
}

# 查找空目录
find_empty_directories() {
    log_info "查找空目录..."
    
    echo "\n=== 空目录列表 ===" >> "$LOG_FILE"
    
    echo -e "${YELLOW}📁 空目录扫描进度:${NC}"
    
    # 步骤1: 查找空目录
    show_progress 1 2 "扫描空目录"
    local empty_dirs=$(find "$NAS_PATH" -type d -empty 2>/dev/null)
    
    # 步骤2: 统计结果
    show_progress 2 2 "统计空目录"
    local dir_count=$(echo "$empty_dirs" | grep -c '^' 2>/dev/null || echo "0")
    complete_progress "空目录扫描完成"
    
    # 显示结果
    echo -e "\n${CYAN}=== 空目录列表 ===${NC}"
    if [[ $dir_count -eq 0 ]]; then
        echo -e "${GREEN}✅ 没有找到空目录${NC}"
    else
        echo "$empty_dirs" | tee -a "$LOG_FILE"
        echo -e "\n${BLUE}📈 统计: 找到 $dir_count 个空目录${NC}"
    fi
    
    log_success "空目录查找完成，找到 $dir_count 个目录"
}

# 查找临时文件和缓存文件
find_temp_files() {
    log_info "查找临时文件和缓存文件..."
    
    echo "\n=== 临时文件和缓存文件 ===" >> "$LOG_FILE"
    
    # 常见的临时文件扩展名
    local temp_patterns=(
        "*.tmp"
        "*.temp"
        "*.cache"
        "*.bak"
        "*.old"
        "*.swp"
        "*.~*"
        "*~"
        ".DS_Store"
        "Thumbs.db"
        "*.log"
    )
    
    echo -e "${YELLOW}🗑️  临时文件扫描进度:${NC}"
    local total_patterns=${#temp_patterns[@]}
    local current=0
    local total_temp_files=0
    
    for pattern in "${temp_patterns[@]}"; do
        ((current++))
        show_progress $current $total_patterns "扫描 $pattern 文件"
        
        echo "\n--- 查找 $pattern 文件 ---" >> "$LOG_FILE"
        local pattern_files=$(find "$NAS_PATH" -name "$pattern" -type f 2>/dev/null | head -20)
        echo "$pattern_files" | tee -a "$LOG_FILE" > /dev/null
        
        local pattern_count=$(echo "$pattern_files" | grep -c '^' 2>/dev/null || echo "0")
        total_temp_files=$((total_temp_files + pattern_count))
    done
    
    complete_progress "临时文件扫描完成"
    
    # 显示汇总结果
    echo -e "\n${CYAN}=== 临时文件汇总 ===${NC}"
    for pattern in "${temp_patterns[@]}"; do
        echo -e "${BLUE}--- $pattern 文件 ---${NC}"
        local pattern_files=$(find "$NAS_PATH" -name "$pattern" -type f 2>/dev/null | head -10)
        if [[ -n "$pattern_files" ]]; then
            echo "$pattern_files"
        else
            echo -e "${GREEN}  (未找到)${NC}"
        fi
        echo ""
    done
    
    echo -e "${BLUE}📈 总计: 找到约 $total_temp_files 个临时文件${NC}"
    
    log_success "临时文件查找完成，找到约 $total_temp_files 个文件"
}

# 分析文件类型分布
analyze_file_types() {
    log_info "分析文件类型分布..."
    
    echo "\n=== 文件类型分布 ===" >> "$LOG_FILE"
    
    echo -e "${YELLOW}📊 文件类型分析进度:${NC}"
    
    # 步骤1: 查找所有文件
    show_progress 1 4 "扫描所有文件"
    local all_files=$(find "$NAS_PATH" -type f 2>/dev/null)
    
    # 步骤2: 提取文件扩展名
    show_progress 2 4 "提取文件扩展名"
    local extensions=$(echo "$all_files" | sed 's/.*\.//')
    
    # 步骤3: 排序和统计
    show_progress 3 4 "统计文件类型"
    local sorted_extensions=$(echo "$extensions" | sort | uniq -c | sort -nr)
    
    # 步骤4: 格式化输出
    show_progress 4 4 "格式化结果"
    local formatted_result=$(echo "$sorted_extensions" | head -20 | awk '{printf "%-10s %s\n", $1, $2}')
    
    complete_progress "文件类型分析完成"
    
    # 显示结果
    echo -e "\n${CYAN}=== 文件类型分布 (前20种) ===${NC}"
    echo "$formatted_result" | tee -a "$LOG_FILE"
    
    local type_count=$(echo "$formatted_result" | grep -c '^' 2>/dev/null || echo "0")
    echo -e "\n${BLUE}📈 统计: 分析了 $type_count 种文件类型${NC}"
    
    log_success "文件类型分析完成，分析了 $type_count 种类型"
}

# 生成 HTML 报告
generate_html_report() {
    log_info "生成 HTML 报告..."
    
    cat > "$REPORT_FILE" << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NAS 存储分析报告</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-top: 30px;
        }
        .summary {
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .warning {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .success {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        pre {
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 14px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #3498db;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #7f8c8d;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗄️ NAS 存储分析报告</h1>
        
        <div class="summary">
            <h2>📊 报告摘要</h2>
            <p><strong>生成时间:</strong> $(date)</p>
            <p><strong>分析路径:</strong> $NAS_PATH</p>
            <p><strong>报告类型:</strong> 存储空间分析与清理建议</p>
        </div>

EOF

    # 添加日志内容到 HTML 报告
    echo "        <h2>📋 详细分析结果</h2>" >> "$REPORT_FILE"
    echo "        <pre>" >> "$REPORT_FILE"
    cat "$LOG_FILE" >> "$REPORT_FILE"
    echo "        </pre>" >> "$REPORT_FILE"
    
    # 添加清理建议
    cat >> "$REPORT_FILE" << 'EOF'
        
        <h2>🧹 清理建议</h2>
        <div class="warning">
            <h3>⚠️ 注意事项</h3>
            <ul>
                <li>删除文件前请务必备份重要数据</li>
                <li>建议先在测试环境中验证清理脚本</li>
                <li>大文件删除前请确认是否还需要</li>
                <li>重复文件删除时保留一份即可</li>
            </ul>
        </div>
        
        <div class="success">
            <h3>✅ 推荐清理项目</h3>
            <ul>
                <li>删除空目录</li>
                <li>清理临时文件和缓存文件</li>
                <li>删除重复文件（保留一份）</li>
                <li>压缩或归档长期不用的大文件</li>
                <li>清理系统日志文件</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>报告由 NAS 清理脚本自动生成 | 请谨慎操作，确保数据安全</p>
        </div>
    </div>
</body>
</html>
EOF

    log_success "HTML 报告已生成: $REPORT_FILE"
}

# 交互式清理功能
interactive_cleanup() {
    log_info "启动交互式清理模式..."
    
    echo -e "\n${YELLOW}=== 交互式清理模式 ===${NC}"
    echo "请选择要执行的清理操作:"
    echo "1) 删除空目录"
    echo "2) 删除临时文件"
    echo "3) 删除重复文件（交互式）"
    echo "4) 压缩大文件"
    echo "5) 全部执行"
    echo "0) 退出"
    
    read -p "请输入选项 (0-5): " choice
    
    case $choice in
        1)
            cleanup_empty_directories
            ;;
        2)
            cleanup_temp_files
            ;;
        3)
            cleanup_duplicates_interactive
            ;;
        4)
            compress_large_files
            ;;
        5)
            cleanup_empty_directories
            cleanup_temp_files
            cleanup_duplicates_interactive
            compress_large_files
            ;;
        0)
            log_info "退出清理模式"
            return 0
            ;;
        *)
            log_error "无效选项"
            return 1
            ;;
    esac
}

# 删除空目录
cleanup_empty_directories() {
    log_info "开始删除空目录..."
    
    local empty_dirs
    empty_dirs=$(find "$NAS_PATH" -type d -empty 2>/dev/null)
    
    if [ -z "$empty_dirs" ]; then
        log_info "没有发现空目录"
        return 0
    fi
    
    echo "发现以下空目录:"
    echo "$empty_dirs"
    
    read -p "确认删除这些空目录吗？(y/N): " confirm
    if [[ $confirm =~ ^[Yy]$ ]]; then
        echo "$empty_dirs" | xargs -r rmdir
        log_success "空目录删除完成"
    else
        log_info "取消删除空目录"
    fi
}

# 删除临时文件
cleanup_temp_files() {
    log_info "开始删除临时文件..."
    
    local temp_patterns=(
        "*.tmp"
        "*.temp"
        "*.cache"
        "*.swp"
        ".DS_Store"
        "Thumbs.db"
    )
    
    for pattern in "${temp_patterns[@]}"; do
        local temp_files
        temp_files=$(find "$NAS_PATH" -name "$pattern" -type f 2>/dev/null)
        
        if [ -n "$temp_files" ]; then
            echo "发现 $pattern 文件:"
            echo "$temp_files" | head -10
            
            read -p "删除这些 $pattern 文件吗？(y/N): " confirm
            if [[ $confirm =~ ^[Yy]$ ]]; then
                echo "$temp_files" | xargs -r rm -f
                log_success "$pattern 文件删除完成"
            fi
        fi
    done
}

# 交互式删除重复文件
cleanup_duplicates_interactive() {
    log_info "开始交互式重复文件清理..."
    
    if command -v fdupes &> /dev/null; then
        fdupes -r "$NAS_PATH" 2>/dev/null | while IFS= read -r line; do
            if [ -n "$line" ]; then
                echo "发现重复文件组:"
                echo "$line"
                read -p "删除重复文件吗？(保留第一个) (y/N): " confirm
                if [[ $confirm =~ ^[Yy]$ ]]; then
                    # 这里需要更复杂的逻辑来处理重复文件
                    log_info "重复文件处理功能需要进一步完善"
                fi
            fi
        done
    else
        log_warn "fdupes 未安装，跳过重复文件清理"
    fi
}

# 压缩大文件
compress_large_files() {
    log_info "开始压缩大文件..."
    
    local large_files
    large_files=$(find "$NAS_PATH" -type f -size +"$MIN_FILE_SIZE" 2>/dev/null | head -10)
    
    if [ -z "$large_files" ]; then
        log_info "没有发现需要压缩的大文件"
        return 0
    fi
    
    echo "发现以下大文件:"
    echo "$large_files"
    
    read -p "压缩这些大文件吗？(y/N): " confirm
    if [[ $confirm =~ ^[Yy]$ ]]; then
        echo "$large_files" | while IFS= read -r file; do
            if [ -f "$file" ]; then
                log_info "压缩文件: $file"
                gzip "$file" && log_success "压缩完成: $file.gz"
            fi
        done
    fi
}

# 主函数
main() {
    echo -e "${BLUE}=== NAS 文件清理和整理工具 ===${NC}"
    echo "开始时间: $(date)"
    
    # 初始化日志文件
    > "$LOG_FILE"
    
    # 检查依赖
    if ! check_dependencies; then
        exit 1
    fi
    
    # 检查 NAS 路径
    if [ ! -d "$NAS_PATH" ]; then
        log_error "NAS 路径不存在: $NAS_PATH"
        log_info "请修改脚本中的 NAS_PATH 变量"
        exit 1
    fi
    
    # 执行分析
    analyze_disk_usage
    find_large_files
    find_duplicate_files
    find_empty_directories
    find_temp_files
    analyze_file_types
    
    # 生成报告
    generate_html_report
    
    echo -e "\n${GREEN}=== 分析完成 ===${NC}"
    echo "日志文件: $LOG_FILE"
    echo "HTML 报告: $REPORT_FILE"
    
    # 询问是否进入交互式清理模式
    read -p "是否进入交互式清理模式？(y/N): " cleanup_confirm
    if [[ $cleanup_confirm =~ ^[Yy]$ ]]; then
        interactive_cleanup
    fi
    
    echo "结束时间: $(date)"
    log_success "NAS 清理分析完成"
}

# 脚本入口
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi