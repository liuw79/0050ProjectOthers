#!/bin/bash

# Automatic Video File Organizer for NAS
# 自动视频文件整理工具
# Author: AI Assistant
# Date: $(date +%Y-%m-%d)

# 加载配置文件
CONFIG_FILE="$(dirname "$0")/video_config.conf"
if [[ -f "$CONFIG_FILE" ]]; then
    source "$CONFIG_FILE"
else
    echo "错误：找不到配置文件 $CONFIG_FILE"
    exit 1
fi

# 默认配置
VIDEO_BASE_PATH="${VIDEO_BASE_PATH:-/Volumes/video}"
LOG_DIR="${LOG_DIR:-$(dirname "$0")/logs}"
REPORT_DIR="${REPORT_DIR:-$(dirname "$0")/reports}"
DRY_RUN="${DRY_RUN:-true}"
AUTO_ORGANIZE="${AUTO_ORGANIZE:-false}"

# 创建必要的目录
mkdir -p "$LOG_DIR" "$REPORT_DIR"

# 日志文件
LOG_FILE="$LOG_DIR/video_auto_organize_$(date +%Y%m%d_%H%M%S).log"
REPORT_FILE="$REPORT_DIR/video_organize_report_$(date +%Y%m%d_%H%M%S).html"
STATS_FILE="$LOG_DIR/organize_stats_$(date +%Y%m%d_%H%M%S).json"

# 统计变量
FILES_MOVED=0
FILES_SKIPPED=0
FILES_ERROR=0
DUPLICATES_FOUND=0
SPACE_SAVED=0
TOTAL_PROCESSED=0

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 错误处理
error_exit() {
    log "错误: $1"
    exit 1
}

# 进度显示
show_progress() {
    local current=$1
    local total=$2
    local operation="$3"
    local percentage=$((current * 100 / total))
    printf "\r[%3d%%] %s (%d/%d)" "$percentage" "$operation" "$current" "$total"
}

# 检查文件是否为视频文件
is_video_file() {
    local file="$1"
    local ext="${file##*.}"
    ext="${ext,,}"  # 转小写
    
    case "$ext" in
        mp4|mkv|avi|mov|wmv|flv|webm|m4v|3gp|ts|m2ts|mpg|mpeg|rm|rmvb)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# 获取文件信息
get_file_info() {
    local file="$1"
    local info_json="{}"
    
    if command -v ffprobe &> /dev/null; then
        info_json=$(ffprobe -v quiet -print_format json -show_format -show_streams "$file" 2>/dev/null || echo '{}')
    fi
    
    echo "$info_json"
}

# 检测重复文件
detect_duplicates() {
    log "检测重复文件..."
    
    local temp_dir="$(mktemp -d)"
    local size_map="$temp_dir/size_map.txt"
    local duplicates="$temp_dir/duplicates.txt"
    
    # 按文件大小分组
    find "$VIDEO_BASE_PATH" -type f -exec stat -f"%z %N" {} \; | sort -n > "$size_map"
    
    # 查找相同大小的文件
    awk '{size=$1; $1=""; files[size]=files[size] $0 "\n"} END {for(s in files) if(gsub(/\n/,"\n",files[s])>1) print files[s]}' "$size_map" > "$duplicates"
    
    local duplicate_groups=0
    if [[ -s "$duplicates" ]]; then
        duplicate_groups=$(grep -c '^$' "$duplicates" || echo 0)
        log "发现 $duplicate_groups 组可能的重复文件"
        
        # 如果启用了内容检测
        if [[ "$CONTENT_BASED_DUPLICATE" == "true" ]]; then
            verify_duplicates_by_content "$duplicates"
        fi
    else
        log "未发现重复文件"
    fi
    
    rm -rf "$temp_dir"
    return $duplicate_groups
}

# 通过内容验证重复文件
verify_duplicates_by_content() {
    local duplicates_file="$1"
    log "通过文件内容验证重复文件..."
    
    # 这里可以使用 md5 或其他哈希算法
    # 由于视频文件较大，这个过程可能很慢
    local verified=0
    
    while IFS= read -r line; do
        if [[ -n "$line" ]]; then
            local file1=$(echo "$line" | awk '{print $1}')
            local file2=$(echo "$line" | awk '{print $2}')
            
            if [[ -f "$file1" && -f "$file2" ]]; then
                # 比较文件的前1MB内容
                if cmp -s <(head -c 1048576 "$file1") <(head -c 1048576 "$file2"); then
                    log "确认重复: $file1 <-> $file2"
                    ((verified++))
                    ((DUPLICATES_FOUND++))
                fi
            fi
        fi
    done < "$duplicates_file"
    
    log "验证了 $verified 对重复文件"
}

# 清理空目录
clean_empty_directories() {
    log "清理空目录..."
    
    local cleaned=0
    
    # 查找空目录（排除回收站）
    find "$VIDEO_BASE_PATH" -type d -empty ! -path "*/\#recycle*" | while read -r dir; do
        if [[ "$DRY_RUN" == "true" ]]; then
            log "[DRY RUN] 将删除空目录: $dir"
        else
            log "删除空目录: $dir"
            rmdir "$dir" 2>/dev/null && ((cleaned++))
        fi
    done
    
    log "清理了 $cleaned 个空目录"
}

# 整理文件到新结构
organize_by_category() {
    log "按分类整理文件..."
    
    local total_files=0
    local processed=0
    
    # 计算总文件数
    total_files=$(find "$VIDEO_BASE_PATH" -type f -name "*.mp4" -o -name "*.mkv" -o -name "*.avi" | wc -l)
    log "需要处理 $total_files 个视频文件"
    
    # 处理每个文件
    find "$VIDEO_BASE_PATH" -type f \( -name "*.mp4" -o -name "*.mkv" -o -name "*.avi" -o -name "*.mov" \) | while read -r file; do
        ((processed++))
        ((TOTAL_PROCESSED++))
        
        show_progress $processed $total_files "整理文件"
        
        # 获取文件信息
        local filename=$(basename "$file")
        local dirname=$(dirname "$file")
        local current_category=$(basename "$dirname")
        
        # 根据当前目录确定新位置
        local new_category=""
        case "$current_category" in
            "电影")
                new_category="电影/待分类"
                ;;
            "电视")
                new_category="电视剧/待分类"
                ;;
            "动画")
                new_category="动画/待分类"
                ;;
            "记录片")
                new_category="纪录片/待分类"
                ;;
            "教程")
                new_category="教程/待分类"
                ;;
            "演出")
                new_category="演出/待分类"
                ;;
            *)
                new_category="其他/待分类"
                ;;
        esac
        
        # 创建新目录
        local new_dir="$VIDEO_BASE_PATH/$new_category"
        if [[ "$DRY_RUN" != "true" ]]; then
            mkdir -p "$new_dir"
        fi
        
        # 移动文件
        local new_path="$new_dir/$filename"
        if [[ "$file" != "$new_path" ]]; then
            if [[ "$DRY_RUN" == "true" ]]; then
                log "[DRY RUN] 将移动: $file -> $new_path"
            else
                if mv "$file" "$new_path" 2>/dev/null; then
                    log "移动成功: $filename -> $new_category"
                    ((FILES_MOVED++))
                else
                    log "移动失败: $file"
                    ((FILES_ERROR++))
                fi
            fi
        else
            ((FILES_SKIPPED++))
        fi
    done
    
    echo  # 换行
    log "文件整理完成"
}

# 优化存储空间
optimize_storage() {
    log "优化存储空间..."
    
    # 清理回收站中的旧文件
    if [[ -d "$RECYCLE_BIN_PATH" ]]; then
        log "清理回收站..."
        local old_files=$(find "$RECYCLE_BIN_PATH" -type f -mtime +30 | wc -l)
        if [[ $old_files -gt 0 ]]; then
            if [[ "$DRY_RUN" == "true" ]]; then
                log "[DRY RUN] 将删除回收站中 $old_files 个超过30天的文件"
            else
                find "$RECYCLE_BIN_PATH" -type f -mtime +30 -delete
                log "删除了回收站中 $old_files 个旧文件"
            fi
        fi
    fi
    
    # 查找并报告大文件
    log "分析大文件..."
    local large_files=$(find "$VIDEO_BASE_PATH" -type f -size +5G | wc -l)
    log "发现 $large_files 个超过5GB的大文件"
    
    # 查找小文件（可能是样本或损坏文件）
    local small_files=$(find "$VIDEO_BASE_PATH" -type f -size -10M -name "*.mp4" -o -name "*.mkv" -o -name "*.avi" | wc -l)
    log "发现 $small_files 个小于10MB的视频文件（可能需要检查）"
}

# 生成整理报告
generate_organize_report() {
    log "生成整理报告..."
    
    # 生成统计JSON
    cat > "$STATS_FILE" << EOF
{
    "timestamp": "$(date -Iseconds)",
    "operation": "auto_organize",
    "dry_run": $DRY_RUN,
    "statistics": {
        "total_processed": $TOTAL_PROCESSED,
        "files_moved": $FILES_MOVED,
        "files_skipped": $FILES_SKIPPED,
        "files_error": $FILES_ERROR,
        "duplicates_found": $DUPLICATES_FOUND,
        "space_saved_bytes": $SPACE_SAVED
    },
    "config": {
        "video_base_path": "$VIDEO_BASE_PATH",
        "auto_organize": "$AUTO_ORGANIZE",
        "detect_duplicates": "$DETECT_DUPLICATES"
    }
}
EOF
    
    # 生成HTML报告
    cat > "$REPORT_FILE" << EOF
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>视频文件自动整理报告</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1, h2 { color: #333; border-bottom: 2px solid #2196F3; padding-bottom: 10px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .stat-card { background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #2196F3; }
        .stat-number { font-size: 2em; font-weight: bold; color: #2196F3; }
        .stat-label { color: #666; margin-top: 5px; }
        .success { color: #4CAF50; }
        .warning { color: #ff9800; }
        .error { color: #f44336; }
        .dry-run { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; margin: 20px 0; }
        .summary { background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 视频文件自动整理报告</h1>
        <p><strong>执行时间:</strong> $(date '+%Y-%m-%d %H:%M:%S')</p>
        <p><strong>处理路径:</strong> $VIDEO_BASE_PATH</p>
EOF
    
    if [[ "$DRY_RUN" == "true" ]]; then
        cat >> "$REPORT_FILE" << EOF
        <div class="dry-run">
            <strong>⚠️ 注意:</strong> 这是干运行模式，没有实际移动或删除任何文件。
        </div>
EOF
    fi
    
    cat >> "$REPORT_FILE" << EOF
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">$TOTAL_PROCESSED</div>
                <div class="stat-label">总处理文件数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number success">$FILES_MOVED</div>
                <div class="stat-label">成功移动</div>
            </div>
            <div class="stat-card">
                <div class="stat-number warning">$FILES_SKIPPED</div>
                <div class="stat-label">跳过文件</div>
            </div>
            <div class="stat-card">
                <div class="stat-number error">$FILES_ERROR</div>
                <div class="stat-label">处理错误</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">$DUPLICATES_FOUND</div>
                <div class="stat-label">发现重复</div>
            </div>
        </div>
        
        <h2>📊 处理摘要</h2>
        <div class="summary">
            <h3>操作结果</h3>
            <ul>
EOF
    
    if [[ $FILES_MOVED -gt 0 ]]; then
        echo "                <li class='success'>✅ 成功整理了 $FILES_MOVED 个文件</li>" >> "$REPORT_FILE"
    fi
    
    if [[ $FILES_ERROR -gt 0 ]]; then
        echo "                <li class='error'>❌ $FILES_ERROR 个文件处理失败</li>" >> "$REPORT_FILE"
    fi
    
    if [[ $DUPLICATES_FOUND -gt 0 ]]; then
        echo "                <li class='warning'>⚠️ 发现 $DUPLICATES_FOUND 个重复文件</li>" >> "$REPORT_FILE"
    fi
    
    cat >> "$REPORT_FILE" << EOF
            </ul>
            
            <h3>💡 建议</h3>
            <ul>
                <li>定期运行此工具以保持文件组织</li>
                <li>检查并处理发现的重复文件</li>
                <li>考虑对大文件进行压缩以节省空间</li>
                <li>定期清理回收站</li>
            </ul>
        </div>
        
        <div style="margin-top: 30px; font-size: 0.9em; color: #666;">
            <p>日志文件: $LOG_FILE</p>
            <p>统计文件: $STATS_FILE</p>
        </div>
    </div>
</body>
</html>
EOF
    
    log "报告已生成: $REPORT_FILE"
}

# 主函数
main() {
    log "=== 视频文件自动整理工具启动 ==="
    log "配置文件: $CONFIG_FILE"
    log "视频目录: $VIDEO_BASE_PATH"
    log "干运行模式: $DRY_RUN"
    log "自动整理: $AUTO_ORGANIZE"
    
    # 检查视频目录是否存在
    if [[ ! -d "$VIDEO_BASE_PATH" ]]; then
        error_exit "视频目录不存在: $VIDEO_BASE_PATH"
    fi
    
    # 检查是否启用自动整理
    if [[ "$AUTO_ORGANIZE" != "true" ]]; then
        log "自动整理未启用，仅进行分析"
    fi
    
    # 开始处理
    local start_time=$(date +%s)
    
    # 检测重复文件
    if [[ "$DETECT_DUPLICATES" == "true" ]]; then
        detect_duplicates
    fi
    
    # 执行整理（如果启用）
    if [[ "$AUTO_ORGANIZE" == "true" ]]; then
        organize_by_category
        clean_empty_directories
    fi
    
    # 优化存储
    optimize_storage
    
    # 生成报告
    generate_organize_report
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    log "=== 整理完成 ==="
    log "总耗时: ${duration}秒"
    log "日志文件: $LOG_FILE"
    log "报告文件: $REPORT_FILE"
    
    # 打开报告文件
    if [[ "$OPEN_REPORT" == "true" ]] && command -v open &> /dev/null; then
        open "$REPORT_FILE"
    fi
}

# 显示帮助信息
show_help() {
    cat << EOF
视频文件自动整理工具

用法: $0 [选项]

选项:
  -h, --help          显示此帮助信息
  -c, --config FILE   指定配置文件路径
  -d, --dry-run       仅分析，不进行任何修改
  -f, --force         强制执行（覆盖安全设置）
  -v, --verbose       详细输出
  --enable-organize   启用自动整理
  --detect-duplicates 启用重复文件检测

示例:
  $0                           # 使用默认配置进行分析
  $0 --dry-run                 # 仅分析模式
  $0 --enable-organize         # 启用自动整理
  $0 --detect-duplicates       # 检测重复文件

注意:
  - 首次使用建议启用 --dry-run 模式
  - 确保有足够的备份再进行实际整理
  - 大型视频库的处理可能需要较长时间

EOF
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -c|--config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        -d|--dry-run)
            DRY_RUN="true"
            shift
            ;;
        -f|--force)
            FORCE="true"
            shift
            ;;
        -v|--verbose)
            VERBOSE="true"
            shift
            ;;
        --enable-organize)
            AUTO_ORGANIZE="true"
            shift
            ;;
        --detect-duplicates)
            DETECT_DUPLICATES="true"
            shift
            ;;
        *)
            echo "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 安全检查
if [[ "$DRY_RUN" != "true" && "$FORCE" != "true" ]]; then
    echo "警告: 即将对视频文件进行实际操作"
    echo "建议先使用 --dry-run 模式进行测试"
    echo "继续请输入 'yes': "
    read -r confirmation
    if [[ "$confirmation" != "yes" ]]; then
        echo "操作已取消"
        exit 0
    fi
fi

# 运行主函数
main