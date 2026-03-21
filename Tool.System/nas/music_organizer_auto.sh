#!/bin/bash

# 自动音乐文件整理脚本
# Automatic Music File Organization Script
# 基于分析结果自动整理音乐文件目录结构

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

# 配置文件路径
CONFIG_FILE="./music_config.conf"

# 默认配置
MUSIC_PATH="/volume1/music"
ORGANIZED_PATH="/volume1/music_organized"
BACKUP_PATH="./backups"
LOG_DIR="./logs"
TEMP_DIR="/tmp/music_organize"

# 整理模式
ORGANIZE_MODE="artist_album"  # artist_album, genre_artist, year_artist, composer_work
SAFE_MODE=true
CREATE_BACKUP=true

# 加载配置文件
load_config() {
    if [ -f "$CONFIG_FILE" ]; then
        echo -e "${BLUE}📋 加载配置文件: $CONFIG_FILE${NC}"
        source "$CONFIG_FILE"
        
        # 使用配置文件中的值
        MUSIC_PATH="${MUSIC_ROOT_PATH:-$MUSIC_PATH}"
        BACKUP_PATH="${BACKUP_DIRECTORY:-$BACKUP_PATH}"
        LOG_DIR="${LOG_DIRECTORY:-$LOG_DIR}"
        TEMP_DIR="${TEMP_DIRECTORY:-$TEMP_DIR}"
        SAFE_MODE="${SAFE_MODE:-true}"
        
        echo -e "${GREEN}✅ 配置加载完成${NC}"
    else
        echo -e "${YELLOW}⚠️  配置文件不存在，使用默认配置${NC}"
    fi
}

# 创建必要目录
mkdir -p "$LOG_DIR" "$TEMP_DIR" "$BACKUP_PATH"

# 日志文件
LOG_FILE="$LOG_DIR/music_organize_$(date +%Y%m%d_%H%M%S).log"

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
    echo "║                🎵 自动音乐文件整理工具                      ║"
    echo "║                                                              ║"
    echo "║  智能分类 • 自动重命名 • 目录优化 • 安全备份                ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}\n"
}

# 检查依赖工具
check_dependencies() {
    local missing_tools=()
    
    # 检查必需的工具
    for tool in "find" "stat" "md5sum" "ffprobe"; do
        if ! command -v "$tool" &> /dev/null; then
            missing_tools+=("$tool")
        fi
    done
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        echo -e "${RED}❌ 缺少必需工具: ${missing_tools[*]}${NC}"
        echo -e "${YELLOW}💡 请安装缺少的工具后重试${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ 依赖检查通过${NC}"
}

# 获取音乐文件元数据
get_music_metadata() {
    local file="$1"
    local metadata_file="$TEMP_DIR/metadata_$(basename "$file").txt"
    
    # 使用ffprobe获取元数据
    if command -v ffprobe &> /dev/null; then
        ffprobe -v quiet -print_format json -show_format "$file" 2>/dev/null > "$metadata_file"
        
        if [ -f "$metadata_file" ]; then
            # 提取关键信息
            local artist=$(grep -o '"artist"[[:space:]]*:[[:space:]]*"[^"]*"' "$metadata_file" | cut -d'"' -f4)
            local album=$(grep -o '"album"[[:space:]]*:[[:space:]]*"[^"]*"' "$metadata_file" | cut -d'"' -f4)
            local title=$(grep -o '"title"[[:space:]]*:[[:space:]]*"[^"]*"' "$metadata_file" | cut -d'"' -f4)
            local date=$(grep -o '"date"[[:space:]]*:[[:space:]]*"[^"]*"' "$metadata_file" | cut -d'"' -f4)
            local genre=$(grep -o '"genre"[[:space:]]*:[[:space:]]*"[^"]*"' "$metadata_file" | cut -d'"' -f4)
            local track=$(grep -o '"track"[[:space:]]*:[[:space:]]*"[^"]*"' "$metadata_file" | cut -d'"' -f4)
            
            # 输出结果
            echo "ARTIST=$artist"
            echo "ALBUM=$album"
            echo "TITLE=$title"
            echo "DATE=$date"
            echo "GENRE=$genre"
            echo "TRACK=$track"
        fi
    else
        # 如果没有ffprobe，尝试从文件名推断
        local basename=$(basename "$file" | sed 's/\.[^.]*$//')
        
        # 简单的文件名解析
        if [[ "$basename" =~ ^([0-9]+)[[:space:]]*-[[:space:]]*(.+)$ ]]; then
            echo "TRACK=${BASH_REMATCH[1]}"
            echo "TITLE=${BASH_REMATCH[2]}"
        else
            echo "TITLE=$basename"
        fi
        
        # 从目录结构推断艺术家和专辑
        local dir_path=$(dirname "$file")
        local parent_dir=$(basename "$dir_path")
        local grandparent_dir=$(basename "$(dirname "$dir_path")")
        
        echo "ALBUM=$parent_dir"
        echo "ARTIST=$grandparent_dir"
    fi
    
    # 清理临时文件
    [ -f "$metadata_file" ] && rm -f "$metadata_file"
}

# 清理文件名
sanitize_filename() {
    local filename="$1"
    
    # 移除或替换不安全的字符
    filename=$(echo "$filename" | sed 's/[<>:"|?*]/_/g')
    filename=$(echo "$filename" | sed 's/[[:space:]]*$//g')
    filename=$(echo "$filename" | sed 's/^[[:space:]]*//g')
    filename=$(echo "$filename" | sed 's/[[:space:]]\+/ /g')
    
    # 限制长度
    if [ ${#filename} -gt 200 ]; then
        filename="${filename:0:200}"
    fi
    
    echo "$filename"
}

# 生成目标路径
generate_target_path() {
    local file="$1"
    local metadata="$2"
    
    # 解析元数据
    local artist album title date genre track
    eval "$metadata"
    
    # 清理元数据
    artist=$(sanitize_filename "$artist")
    album=$(sanitize_filename "$album")
    title=$(sanitize_filename "$title")
    genre=$(sanitize_filename "$genre")
    
    # 设置默认值
    [ -z "$artist" ] && artist="Unknown Artist"
    [ -z "$album" ] && album="Unknown Album"
    [ -z "$title" ] && title=$(basename "$file" | sed 's/\.[^.]*$//')
    [ -z "$genre" ] && genre="Unknown Genre"
    
    # 获取文件扩展名
    local extension="${file##*.}"
    
    # 根据整理模式生成路径
    local target_dir target_filename
    
    case "$ORGANIZE_MODE" in
        "artist_album")
            target_dir="$ORGANIZED_PATH/$artist/$album"
            if [ -n "$track" ] && [[ "$track" =~ ^[0-9]+$ ]]; then
                target_filename=$(printf "%02d - %s.%s" "$track" "$title" "$extension")
            else
                target_filename="$title.$extension"
            fi
            ;;
        "genre_artist")
            target_dir="$ORGANIZED_PATH/$genre/$artist/$album"
            target_filename="$title.$extension"
            ;;
        "year_artist")
            local year="${date:0:4}"
            [ -z "$year" ] && year="Unknown Year"
            target_dir="$ORGANIZED_PATH/$year/$artist/$album"
            target_filename="$title.$extension"
            ;;
        "composer_work")
            # 特殊处理古典音乐
            if [[ "$genre" =~ [Cc]lassical ]] || [[ "$album" =~ [Cc]lassical ]]; then
                # 尝试从艺术家或专辑中提取作曲家信息
                local composer="$artist"
                target_dir="$ORGANIZED_PATH/Classical/$composer/$album"
            else
                target_dir="$ORGANIZED_PATH/$artist/$album"
            fi
            target_filename="$title.$extension"
            ;;
        *)
            target_dir="$ORGANIZED_PATH/$artist/$album"
            target_filename="$title.$extension"
            ;;
    esac
    
    echo "$target_dir/$target_filename"
}

# 创建备份
create_backup() {
    if [ "$CREATE_BACKUP" = "true" ]; then
        echo -e "\n${BLUE}💾 创建备份...${NC}"
        
        local backup_name="music_backup_$(date +%Y%m%d_%H%M%S)"
        local backup_full_path="$BACKUP_PATH/$backup_name"
        
        if [ -d "$MUSIC_PATH" ]; then
            mkdir -p "$backup_full_path"
            
            # 创建文件列表备份
            find "$MUSIC_PATH" -type f > "$backup_full_path/file_list.txt"
            
            # 创建目录结构备份
            find "$MUSIC_PATH" -type d > "$backup_full_path/dir_list.txt"
            
            # 记录备份信息
            cat > "$backup_full_path/backup_info.txt" << EOF
备份时间: $(date '+%Y-%m-%d %H:%M:%S')
源路径: $MUSIC_PATH
备份类型: 文件列表备份
脚本版本: 1.0.0
EOF
            
            echo -e "${GREEN}✅ 备份创建完成: $backup_full_path${NC}"
            log_message "INFO" "备份创建完成: $backup_full_path"
        else
            echo -e "${RED}❌ 源路径不存在，无法创建备份${NC}"
        fi
    fi
}

# 整理音乐文件
organize_music_files() {
    echo -e "\n${BLUE}🎵 开始整理音乐文件...${NC}"
    
    # 查找所有音乐文件
    local music_files=()
    while IFS= read -r -d '' file; do
        music_files+=("$file")
    done < <(find "$MUSIC_PATH" -type f \( -iname "*.mp3" -o -iname "*.flac" -o -iname "*.wav" -o -iname "*.aac" -o -iname "*.m4a" -o -iname "*.ogg" -o -iname "*.wma" -o -iname "*.ape" \) -print0)
    
    local total_files=${#music_files[@]}
    
    if [ $total_files -eq 0 ]; then
        echo -e "${YELLOW}⚠️  未找到音乐文件${NC}"
        return
    fi
    
    echo -e "${CYAN}📊 找到 $total_files 个音乐文件${NC}"
    
    # 创建整理目标目录
    mkdir -p "$ORGANIZED_PATH"
    
    local processed=0
    local moved=0
    local errors=0
    
    # 处理每个文件
    for file in "${music_files[@]}"; do
        processed=$((processed + 1))
        show_progress $processed $total_files "整理音乐文件"
        
        # 获取元数据
        local metadata=$(get_music_metadata "$file")
        
        # 生成目标路径
        local target_path=$(generate_target_path "$file" "$metadata")
        local target_dir=$(dirname "$target_path")
        
        # 检查是否需要移动
        if [ "$file" = "$target_path" ]; then
            continue  # 文件已在正确位置
        fi
        
        # 创建目标目录
        if [ "$SAFE_MODE" = "false" ]; then
            mkdir -p "$target_dir"
            
            # 检查目标文件是否已存在
            if [ -f "$target_path" ]; then
                # 生成唯一文件名
                local counter=1
                local base_name=$(basename "$target_path" | sed 's/\.[^.]*$//')
                local extension="${target_path##*.}"
                
                while [ -f "$target_dir/${base_name}_${counter}.$extension" ]; do
                    counter=$((counter + 1))
                done
                
                target_path="$target_dir/${base_name}_${counter}.$extension"
            fi
            
            # 移动文件
            if mv "$file" "$target_path" 2>/dev/null; then
                moved=$((moved + 1))
                log_message "INFO" "文件移动: $file -> $target_path"
            else
                errors=$((errors + 1))
                log_message "ERROR" "文件移动失败: $file -> $target_path"
            fi
        else
            # 安全模式：只记录操作
            echo "[SAFE MODE] 将移动: $file -> $target_path" >> "$LOG_FILE"
        fi
    done
    
    complete_progress "音乐文件整理完成"
    
    # 显示统计信息
    echo -e "\n${CYAN}📊 整理统计:${NC}"
    echo -e "  📁 处理文件: $processed"
    if [ "$SAFE_MODE" = "false" ]; then
        echo -e "  ✅ 成功移动: $moved"
        echo -e "  ❌ 移动失败: $errors"
    else
        echo -e "  🔒 安全模式: 仅记录操作，未实际移动文件"
    fi
    
    log_message "INFO" "音乐文件整理完成: 处理$processed, 移动$moved, 错误$errors"
}

# 清理空目录
cleanup_empty_directories() {
    if [ "$SAFE_MODE" = "false" ]; then
        echo -e "\n${BLUE}🧹 清理空目录...${NC}"
        
        local removed_dirs=0
        
        # 查找并删除空目录
        while IFS= read -r -d '' dir; do
            if rmdir "$dir" 2>/dev/null; then
                removed_dirs=$((removed_dirs + 1))
                log_message "INFO" "删除空目录: $dir"
            fi
        done < <(find "$MUSIC_PATH" -type d -empty -print0)
        
        echo -e "${GREEN}✅ 清理了 $removed_dirs 个空目录${NC}"
    else
        echo -e "\n${YELLOW}🔒 安全模式：跳过空目录清理${NC}"
    fi
}

# 生成整理报告
generate_organization_report() {
    echo -e "\n${BLUE}📄 生成整理报告...${NC}"
    
    local report_file="$LOG_DIR/organization_report_$(date +%Y%m%d_%H%M%S).html"
    
    cat > "$report_file" << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>音乐文件整理报告</title>
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
        .success { color: #27ae60; }
        .warning { color: #f39c12; }
        .error { color: #e74c3c; }
        .timestamp { color: #7f8c8d; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎵 音乐文件整理报告</h1>
            <p class="timestamp">生成时间: $(date '+%Y-%m-%d %H:%M:%S')</p>
        </div>
        <div class="content">
            <div class="section">
                <h2>📊 整理统计</h2>
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number success">$(grep "处理文件" "$LOG_FILE" | tail -1 | grep -o '[0-9]\+' | head -1 || echo "0")</div>
                        <div class="stat-label">处理文件数</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number success">$(grep "成功移动" "$LOG_FILE" | tail -1 | grep -o '[0-9]\+' | head -1 || echo "0")</div>
                        <div class="stat-label">成功移动</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number error">$(grep "移动失败" "$LOG_FILE" | tail -1 | grep -o '[0-9]\+' | head -1 || echo "0")</div>
                        <div class="stat-label">移动失败</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>⚙️ 整理配置</h2>
                <p><strong>整理模式:</strong> $ORGANIZE_MODE</p>
                <p><strong>安全模式:</strong> $([ "$SAFE_MODE" = "true" ] && echo "启用" || echo "禁用")</p>
                <p><strong>源路径:</strong> $MUSIC_PATH</p>
                <p><strong>目标路径:</strong> $ORGANIZED_PATH</p>
            </div>
            
            <div class="section">
                <h2>📝 操作日志</h2>
                <div style="max-height: 400px; overflow-y: auto; background: #f8f9fa; padding: 15px; border-radius: 5px; font-family: monospace; font-size: 0.9em;">
EOF

    # 添加最近的日志条目
    tail -50 "$LOG_FILE" | while read -r line; do
        echo "                    <div>$line</div>" >> "$report_file"
    done
    
    cat >> "$report_file" << 'EOF'
                </div>
            </div>
        </div>
    </div>
</body>
</html>
EOF

    echo -e "${GREEN}✅ 报告已生成: $report_file${NC}"
    log_message "INFO" "整理报告生成完成: $report_file"
}

# 显示菜单
show_menu() {
    echo -e "\n${CYAN}🎵 音乐文件整理选项:${NC}"
    echo "  1) 🔍 预览整理计划 (安全模式)"
    echo "  2) 🎯 执行音乐文件整理"
    echo "  3) 🧹 清理空目录"
    echo "  4) 📄 生成整理报告"
    echo "  5) ⚙️  配置整理选项"
    echo "  6) 💾 创建备份"
    echo "  7) 🔄 完整整理流程"
    echo "  8) 🚪 退出"
    echo ""
}

# 配置整理选项
configure_options() {
    echo -e "\n${YELLOW}⚙️  当前配置:${NC}"
    echo "  音乐路径: $MUSIC_PATH"
    echo "  整理路径: $ORGANIZED_PATH"
    echo "  整理模式: $ORGANIZE_MODE"
    echo "  安全模式: $SAFE_MODE"
    echo "  创建备份: $CREATE_BACKUP"
    echo ""
    
    read -p "是否要修改整理模式? (y/N): " change_mode
    if [[ $change_mode =~ ^[Yy]$ ]]; then
        echo "可选模式:"
        echo "  1) artist_album - 艺术家/专辑"
        echo "  2) genre_artist - 流派/艺术家/专辑"
        echo "  3) year_artist - 年份/艺术家/专辑"
        echo "  4) composer_work - 作曲家/作品 (古典音乐)"
        
        read -p "请选择模式 (1-4): " mode_choice
        case $mode_choice in
            1) ORGANIZE_MODE="artist_album" ;;
            2) ORGANIZE_MODE="genre_artist" ;;
            3) ORGANIZE_MODE="year_artist" ;;
            4) ORGANIZE_MODE="composer_work" ;;
            *) echo -e "${RED}无效选择${NC}" ;;
        esac
    fi
    
    read -p "是否启用安全模式? (Y/n): " safe_mode
    if [[ $safe_mode =~ ^[Nn]$ ]]; then
        SAFE_MODE="false"
        echo -e "${YELLOW}⚠️  安全模式已禁用，将实际移动文件${NC}"
    else
        SAFE_MODE="true"
        echo -e "${GREEN}🔒 安全模式已启用，仅预览操作${NC}"
    fi
}

# 完整整理流程
full_organization() {
    echo -e "\n${PURPLE}🚀 开始完整音乐文件整理流程...${NC}"
    
    # 确认操作
    if [ "$SAFE_MODE" = "false" ]; then
        echo -e "${RED}⚠️  警告: 即将实际移动音乐文件！${NC}"
        read -p "确认继续? (y/N): " confirm
        if [[ ! $confirm =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}操作已取消${NC}"
            return
        fi
    fi
    
    create_backup
    organize_music_files
    cleanup_empty_directories
    generate_organization_report
    
    echo -e "\n${GREEN}🎉 完整整理流程完成！${NC}"
}

# 预览整理计划
preview_organization() {
    local original_safe_mode="$SAFE_MODE"
    SAFE_MODE="true"
    
    echo -e "\n${BLUE}🔍 预览整理计划...${NC}"
    organize_music_files
    
    SAFE_MODE="$original_safe_mode"
    
    echo -e "\n${CYAN}💡 查看详细计划请检查日志文件: $LOG_FILE${NC}"
}

# 清理临时文件
cleanup_temp_files() {
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
        log_message "INFO" "临时文件清理完成"
    fi
}

# 主函数
main() {
    show_header
    load_config
    check_dependencies
    
    if [ ! -d "$MUSIC_PATH" ]; then
        echo -e "${RED}❌ 音乐目录不存在: $MUSIC_PATH${NC}"
        echo -e "${YELLOW}💡 请检查路径或修改配置${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ 音乐目录: $MUSIC_PATH${NC}"
    
    while true; do
        show_menu
        read -p "请选择操作 (1-8): " choice
        
        case $choice in
            1) preview_organization ;;
            2) organize_music_files ;;
            3) cleanup_empty_directories ;;
            4) generate_organization_report ;;
            5) configure_options ;;
            6) create_backup ;;
            7) full_organization ;;
            8) 
                echo -e "\n${GREEN}👋 感谢使用音乐文件整理工具！${NC}"
                cleanup_temp_files
                exit 0
                ;;
            *) 
                echo -e "${RED}❌ 无效选择，请输入 1-8${NC}"
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