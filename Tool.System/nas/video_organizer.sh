#!/bin/bash

# Video File Organizer for NAS with Intelligent Deletion Suggestions
# 视频文件分析和智能删除建议工具
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
CACHE_DIR="${CACHE_DIR:-$(dirname "$0")/cache}"
SUPPORTED_FORMATS="${SUPPORTED_FORMATS:-mp4,mkv,avi,mov,wmv,flv,webm,m4v,3gp,ts,m2ts}"
MIN_FILE_SIZE="${MIN_FILE_SIZE:-10M}"
MAX_FILE_SIZE="${MAX_FILE_SIZE:-50G}"
DRY_RUN="${DRY_RUN:-true}"
CACHE_FILE="$CACHE_DIR/video_analysis_cache.json"
DELETION_SUGGESTIONS_FILE="$CACHE_DIR/deletion_suggestions.json"

# 创建必要的目录
mkdir -p "$LOG_DIR" "$REPORT_DIR" "$CACHE_DIR"

# 日志文件
LOG_FILE="$LOG_DIR/video_analysis_$(date +%Y%m%d_%H%M%S).log"
REPORT_FILE="$REPORT_DIR/video_analysis_$(date +%Y%m%d_%H%M%S).html"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 格式化文件大小
format_size() {
    local size=$1
    if [[ $size -lt 1024 ]]; then
        echo "${size}B"
    elif [[ $size -lt 1048576 ]]; then
        echo "$(( size / 1024 ))KB"
    elif [[ $size -lt 1073741824 ]]; then
        echo "$(( size / 1048576 ))MB"
    elif [[ $size -lt 1099511627776 ]]; then
        echo "$(( size / 1073741824 ))GB"
    else
        echo "$(( size / 1099511627776 ))TB"
    fi
}

# Load cached analysis data
load_cache() {
    if [ -f "$CACHE_FILE" ]; then
        log "Loading cached analysis data..."
        return 0
    else
        log "No cache file found, will perform full analysis"
        echo '{}' > "$CACHE_FILE"
        return 1
    fi
}

# Save file analysis to cache
save_to_cache() {
    local file_path="$1"
    local file_size="$2"
    local duration="$3"
    local resolution="$4"
    local codec="$5"
    local last_modified="$6"
    
    # Create a simple cache entry (in real implementation, would use proper JSON)
    local cache_key=$(echo "$file_path" | md5)
    echo "$cache_key|$file_path|$file_size|$duration|$resolution|$codec|$last_modified" >> "$CACHE_FILE.tmp"
}

# Check if file is in cache and up-to-date
is_cached() {
    local file_path="$1"
    local current_mtime="$2"
    local cache_key=$(echo "$file_path" | md5)
    
    if [ -f "$CACHE_FILE.tmp" ]; then
        grep -q "^$cache_key|" "$CACHE_FILE.tmp" 2>/dev/null
    else
        return 1
    fi
}

# 智能内容识别和分析
intelligent_content_analysis() {
    local file_path="$1"
    local file_size="$2"
    local duration="$3"
    local resolution="$4"
    local codec="$5"
    
    local score=0
    local suggestions=()
    local content_type="未知"
    local series_info=""
    local duplicate_risk="低"
    
    # 基于文件名的内容识别
    local filename=$(basename "$file_path")
    local dirname=$(dirname "$file_path")
    local parent_dir=$(basename "$dirname")
    
    # 动画片/连续剧识别
    if [[ "$filename" =~ (第[0-9]+集|EP?[0-9]+|S[0-9]+E[0-9]+|[0-9]+话) ]] || 
       [[ "$parent_dir" =~ (动画|动漫|anime|series|连续剧|电视剧) ]]; then
        content_type="连续剧/动画"
        series_info="检测到系列内容，可能存在多集"
        score=$((score + 15))
        suggestions+=("系列内容，建议整体评估")
    fi
    
    # 电影识别
    if [[ "$filename" =~ (电影|movie|film|[0-9]{4}年|BluRay|BDRip|DVDRip) ]]; then
        content_type="电影"
        if [ "$file_size" -gt 21474836480 ]; then  # 20GB+
            suggestions+=("超高清电影，文件过大")
            score=$((score + 20))
        fi
    fi
    
    # 纪录片识别
    if [[ "$filename" =~ (纪录片|documentary|记录|探索|发现) ]]; then
        content_type="纪录片"
        score=$((score - 10))  # 纪录片通常有保存价值
    fi
    
    # 教育内容识别
    if [[ "$filename" =~ (教程|tutorial|课程|lesson|学习|教学) ]]; then
        content_type="教育内容"
        score=$((score - 15))  # 教育内容价值较高
    fi
    
    # 重复文件识别
    if [[ "$filename" =~ (copy|副本|备份|backup|duplicate|\([0-9]+\)) ]]; then
        duplicate_risk="高"
        suggestions+=("疑似重复文件")
        score=$((score + 40))
    fi
    
    # 临时文件识别
    if [[ "$filename" =~ (temp|tmp|test|sample|demo|preview) ]]; then
        suggestions+=("临时或测试文件")
        score=$((score + 35))
    fi
    
    # 低质量内容识别
    if [[ "$filename" =~ (cam|ts|枪版|抢先版|tc|scr) ]]; then
        suggestions+=("低质量版本，可能有更好版本")
        score=$((score + 25))
    fi
    
    # 文件大小异常分析
    if [ "$file_size" -gt 53687091200 ]; then  # 50GB+
        suggestions+=("文件极大，占用大量存储空间")
        score=$((score + 30))
    elif [ "$file_size" -lt 10485760 ]; then  # 10MB以下
        suggestions+=("文件过小，可能损坏或无用")
        score=$((score + 40))
    fi
    
    # 时长异常分析
    if [[ "$duration" =~ ^[0-9]+\.?[0-9]*$ ]]; then
        duration_int=$(echo "$duration" | cut -d'.' -f1)
        if [ "$duration_int" -lt 60 ]; then
            suggestions+=("视频过短，可能是片段或预告")
            score=$((score + 20))
        elif [ "$duration_int" -gt 14400 ]; then  # 4小时+
            suggestions+=("视频过长，可能需要分割")
            score=$((score + 15))
        fi
    fi
    
    # 分辨率质量分析
    if [[ "$resolution" =~ ^[0-9]+x[0-9]+$ ]]; then
        width=$(echo "$resolution" | cut -d'x' -f1)
        if [ "$width" -lt 720 ]; then
            suggestions+=("分辨率较低，画质一般")
            score=$((score + 15))
        elif [ "$width" -gt 3840 ]; then  # 4K+
            suggestions+=("超高清视频，文件较大")
            score=$((score + 10))
        fi
    fi
    
    # 编码格式分析
    case "$codec" in
        "wmv"|"flv"|"3gp"|"rm"|"rmvb")
            suggestions+=("过时编码格式，兼容性差")
            score=$((score + 20))
            ;;
        "h265"|"hevc")
            score=$((score - 5))  # 新编码格式，压缩率好
            ;;
    esac
    
    # 生成智能建议
    local priority="低"
    if [ "$score" -ge 60 ]; then
        priority="高"
    elif [ "$score" -ge 30 ]; then
        priority="中"
    fi
    
    # 返回分析结果
    if [ "$score" -ge 25 ]; then
        local suggestion_text=$(IFS='; '; echo "${suggestions[*]}")
        echo "$file_path|$score|$content_type|$duplicate_risk|$priority|$suggestion_text|$series_info"
    fi
}

# Analyze file for deletion suggestions (保持向后兼容)
analyze_for_deletion() {
    intelligent_content_analysis "$@"
}

# 错误处理
error_exit() {
    log "错误: $1"
    exit 1
}

# 检查依赖
check_dependencies() {
    log "检查依赖工具..."
    
    local missing_tools=()
    
    # 检查 ffprobe (用于视频信息获取)
    if ! command -v ffprobe &> /dev/null; then
        missing_tools+=("ffprobe (ffmpeg)")
    fi
    
    # 检查 mediainfo (备选工具)
    if ! command -v mediainfo &> /dev/null && ! command -v ffprobe &> /dev/null; then
        missing_tools+=("mediainfo")
    fi
    
    if [[ ${#missing_tools[@]} -gt 0 ]]; then
        log "缺少以下工具: ${missing_tools[*]}"
        log "请安装: brew install ffmpeg mediainfo"
        return 1
    fi
    
    log "依赖检查完成"
    return 0
}

# 获取视频信息
get_video_info() {
    local file="$1"
    local info_file="$2"
    
    if command -v ffprobe &> /dev/null; then
        ffprobe -v quiet -print_format json -show_format -show_streams "$file" > "$info_file" 2>/dev/null
    elif command -v mediainfo &> /dev/null; then
        mediainfo --Output=JSON "$file" > "$info_file" 2>/dev/null
    else
        echo '{}' > "$info_file"
    fi
}

# 分析视频文件
analyze_videos() {
    log "开始分析视频文件..."
    
    # 加载缓存
    load_cache
    
    local total_files=0
    local total_size=0
    local format_stats=()
    local resolution_stats=()
    local duration_stats=()
    local large_files=()
    local small_files=()
    local duplicate_candidates=()
    local deletion_candidates=()
    
    # 创建临时文件
    local temp_dir="$(mktemp -d)"
    local file_list="$temp_dir/files.txt"
    local size_list="$temp_dir/sizes.txt"
    local format_list="$temp_dir/formats.txt"
    
    # 初始化临时缓存文件
    > "$CACHE_FILE.tmp"
    > "$DELETION_SUGGESTIONS_FILE.tmp"
    
    log "扫描目录: $VIDEO_BASE_PATH"
    
    # 查找所有视频文件
    find "$VIDEO_BASE_PATH" -type f \( \
        -iname "*.mp4" -o -iname "*.mkv" -o -iname "*.avi" -o \
        -iname "*.mov" -o -iname "*.wmv" -o -iname "*.flv" -o \
        -iname "*.webm" -o -iname "*.m4v" -o -iname "*.3gp" -o \
        -iname "*.ts" -o -iname "*.m2ts" \
    \) > "$file_list"
    
    total_files=$(wc -l < "$file_list")
    log "找到 $total_files 个视频文件"
    
    # 分析每个文件
    local count=0
    while IFS= read -r file; do
        ((count++))
        
        # 显示进度
        if ((count % 100 == 0)); then
            log "已处理 $count/$total_files 个文件..."
        fi
        
        # 获取文件信息
        local size=$(stat -f%z "$file" 2>/dev/null || echo 0)
        local last_modified=$(stat -f%m "$file" 2>/dev/null || echo "0")
        local ext="${file##*.}"
        ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')  # 转小写
        
        total_size=$((total_size + size))
        
        # 记录格式统计
        echo "$ext" >> "$format_list"
        
        # 检查是否需要重新分析
        if ! is_cached "$file" "$last_modified"; then
            # 获取视频信息
            local duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$file" 2>/dev/null || echo "N/A")
            local resolution=$(ffprobe -v error -show_entries stream=width,height -of default=noprint_wrappers=1:nokey=1 "$file" 2>/dev/null | tr '\n' 'x' | sed 's/x$//' || echo "N/A")
            local codec=$(ffprobe -v error -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "$file" 2>/dev/null | head -n 1 || echo "N/A")
            
            # 保存到缓存
            save_to_cache "$file" "$size" "$duration" "$resolution" "$codec" "$last_modified"
            
            # 分析删除建议
            local suggestion=$(analyze_for_deletion "$file" "$size" "$duration" "$resolution" "$codec")
            if [ ! -z "$suggestion" ]; then
                deletion_candidates+=("$suggestion")
                echo "$suggestion" >> "$DELETION_SUGGESTIONS_FILE.tmp"
            fi
        fi
        
        # 检查大文件和小文件
        if [[ $size -gt 5368709120 ]]; then  # 5GB
            large_files+=("$file:$size")
        elif [[ $size -lt 10485760 ]]; then  # 10MB
            small_files+=("$file:$size")
        fi
        
        # 记录文件大小
        echo "$size" >> "$size_list"
        
    done < "$file_list"
    
    # 更新缓存文件
    if [ -f "$CACHE_FILE.tmp" ]; then
        mv "$CACHE_FILE.tmp" "$CACHE_FILE"
    fi
    
    if [ -f "$DELETION_SUGGESTIONS_FILE.tmp" ]; then
        mv "$DELETION_SUGGESTIONS_FILE.tmp" "$DELETION_SUGGESTIONS_FILE"
    fi
    
    log "分析完成"
    log "发现 ${#deletion_candidates[@]} 个可能需要删除的文件"
    
    # 生成统计报告
    generate_analysis_report "$temp_dir" "$total_files" "$total_size" "${large_files[@]}" "${small_files[@]}"
    
    # 清理临时文件
    rm -rf "$temp_dir"
}

# 生成分析报告
generate_analysis_report() {
    local temp_dir="$1"
    local total_files="$2"
    local total_size="$3"
    shift 3
    local large_files=("$@")
    
    log "生成分析报告..."
    
    # 计算总大小（人类可读格式）
    local total_size_human=$(format_size $total_size)
    
    # 格式统计
    local format_stats=$(sort "$temp_dir/formats.txt" | uniq -c | sort -nr)
    
    # 生成HTML报告
    cat > "$REPORT_FILE" << EOF
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>视频文件分析报告</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1, h2 { color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }
        .stat-card { background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #4CAF50; }
        .stat-number { font-size: 2em; font-weight: bold; color: #4CAF50; }
        .stat-label { color: #666; margin-top: 5px; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #4CAF50; color: white; }
        tr:hover { background-color: #f5f5f5; }
        .warning { color: #ff6b6b; font-weight: bold; }
        .success { color: #4CAF50; font-weight: bold; }
        .info { color: #3498db; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📹 视频文件分析报告</h1>
        <p><strong>生成时间:</strong> $(date '+%Y-%m-%d %H:%M:%S')</p>
        <p><strong>分析路径:</strong> $VIDEO_BASE_PATH</p>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">$total_files</div>
                <div class="stat-label">总文件数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">$total_size_human</div>
                <div class="stat-label">总大小</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">$(echo "$format_stats" | wc -l)</div>
                <div class="stat-label">文件格式种类</div>
            </div>
        </div>
        
        <h2>📊 格式分布</h2>
        <table>
            <tr><th>格式</th><th>文件数量</th><th>占比</th></tr>
EOF
    
    # 添加格式统计
    while read -r count format; do
        local percentage=$(echo "scale=2; $count * 100 / $total_files" | bc)
        echo "            <tr><td>.$format</td><td>$count</td><td>$percentage%</td></tr>" >> "$REPORT_FILE"
    done <<< "$format_stats"
    
    cat >> "$REPORT_FILE" << EOF
        </table>
        
        <h2>🤖 智能内容分析与删除建议</h2>
        <div style='background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0;'>
            <h4>📋 基于内容分析的智能识别结果</h4>
            <p>以下文件根据内容类型、重复性分析、文件特征等维度进行智能识别，仅显示前100个最大文件的分析结果：</p>
        </div>
EOF
    
    # 智能分析结果列表
    if [[ -f "$DELETION_SUGGESTIONS_FILE" && -s "$DELETION_SUGGESTIONS_FILE" ]]; then
        echo "        <table id='deletionSuggestions'><tr><th>文件路径</th><th>内容类型</th><th>重复风险</th><th>优先级</th><th>文件大小</th><th>建议原因</th><th>系列信息</th><th>操作</th></tr>" >> "$REPORT_FILE"
        # 按文件大小排序，只显示前100个
        sort -t'|' -k2 -nr "$DELETION_SUGGESTIONS_FILE" | head -100 | while IFS='|' read -r file_path score content_type duplicate_risk priority reasons series_info; do
            if [ ! -z "$file_path" ]; then
                local file_display=$(basename "$file_path")
                local file_size_human=$(format_size $(stat -f%z "$file_path" 2>/dev/null || echo 0))
                local priority_class="info"
                case "$priority" in
                    "高") priority_class="warning" ;;
                    "中") priority_class="info" ;;
                    "低") priority_class="success" ;;
                esac
                local duplicate_class="success"
                if [ "$duplicate_risk" = "高" ]; then
                    duplicate_class="warning"
                fi
                local score_class="info"
                if [[ $score -ge 70 ]]; then
                    score_class="warning"
                elif [[ $score -ge 50 ]]; then
                    score_class="info"
                fi
                echo "            <tr><td title='$file_path'>$file_display</td><td>$content_type</td><td class='$duplicate_class'>$duplicate_risk</td><td class='$priority_class'>$priority</td><td>$file_size_human</td><td>$reasons</td><td>$series_info</td><td><button onclick='markForDeletion(\"$file_path\", $score)'>标记删除</button></td></tr>" >> "$REPORT_FILE"
            fi
        done
        echo "        </table>" >> "$REPORT_FILE"
    else
        echo "        <p class='success'>✅ 未发现需要特别关注的文件</p>" >> "$REPORT_FILE"
    fi
    
    cat >> "$REPORT_FILE" << EOF
        
        <h2>⚠️ 需要注意的文件</h2>
EOF
    
    # 大文件列表
    if [[ ${#large_files[@]} -gt 0 ]]; then
        echo "        <h3>大文件 (>5GB)</h3>" >> "$REPORT_FILE"
        echo "        <table><tr><th>文件路径</th><th>大小</th></tr>" >> "$REPORT_FILE"
        for file_info in "${large_files[@]}"; do
            local file="${file_info%:*}"
            local size="${file_info#*:}"
            local size_human=$(format_size $size)
            echo "            <tr><td>$file</td><td class='warning'>$size_human</td></tr>" >> "$REPORT_FILE"
        done
        echo "        </table>" >> "$REPORT_FILE"
    fi
    
    cat >> "$REPORT_FILE" << EOF
        
        <h2>📁 目录结构分析</h2>
EOF
    
    # 目录大小统计
    echo "        <table><tr><th>目录</th><th>文件数</th><th>大小</th></tr>" >> "$REPORT_FILE"
    for dir in "$VIDEO_BASE_PATH"/*/; do
        if [[ -d "$dir" ]]; then
            local dir_name=$(basename "$dir")
            local dir_files=$(find "$dir" -type f \( -iname "*.mp4" -o -iname "*.mkv" -o -iname "*.avi" \) | wc -l)
            local dir_size=$(du -sh "$dir" 2>/dev/null | cut -f1)
            echo "            <tr><td>$dir_name</td><td>$dir_files</td><td>$dir_size</td></tr>" >> "$REPORT_FILE"
        fi
    done
    
    cat >> "$REPORT_FILE" << EOF
        
        <div style="margin-top: 30px; padding: 15px; background-color: #e8f5e8; border-radius: 5px;">
            <h3>💡 整理建议</h3>
            <ul>
                <li>考虑将大文件进行压缩或转码以节省空间</li>
                <li>检查重复文件并删除不需要的副本</li>
                <li>按年份、类型或质量重新组织目录结构</li>
                <li>定期清理回收站和临时文件</li>
                <li>考虑使用更高效的编码格式（如H.265）</li>
            </ul>
        </div>
        
        <div style='margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 5px;'>
            <h3>🗑️ 删除操作</h3>
            <p>已标记 <span id='markedCount'>0</span> 个文件待删除</p>
            <button onclick='confirmDeletion()' style='background: #dc3545; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;'>确认删除标记的文件</button>
            <button onclick='clearMarked()' style='background: #6c757d; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-left: 10px;'>清除标记</button>
        </div>
    </div>
    
    <script>
        let markedFiles = [];
        
        function markForDeletion(filePath, score) {
            if (markedFiles.some(f => f.path === filePath)) {
                alert('文件已经标记过了');
                return;
            }
            
            const fileName = filePath.split('/').pop();
            const riskLevel = score >= 60 ? '高风险' : score >= 30 ? '中风险' : '低风险';
            
            if (confirm(`确定要标记这个文件用于删除吗？\n\n文件: ${fileName}\n路径: ${filePath}\n风险评分: ${score} (${riskLevel})`)) {
                markedFiles.push({
                    path: filePath,
                    name: fileName,
                    score: score,
                    riskLevel: riskLevel
                });
                updateMarkedCount();
                
                // 更新按钮状态
                event.target.textContent = '已标记';
                event.target.disabled = true;
                event.target.style.backgroundColor = '#dc3545';
                event.target.style.color = 'white';
            }
        }
        
        function updateMarkedCount() {
            const countElement = document.getElementById('markedCount');
            if (countElement) {
                countElement.textContent = markedFiles.length;
            }
            
            // 更新标记列表显示
            updateMarkedList();
        }
        
        function updateMarkedList() {
            const listElement = document.getElementById('markedList');
            if (listElement && markedFiles.length > 0) {
                listElement.innerHTML = '<h4>已标记的文件:</h4>' +
                    markedFiles.map(f => 
                        `<div style="margin: 5px 0; padding: 5px; background: #f8f9fa; border-radius: 3px;">
                            <strong>${f.name}</strong> (评分: ${f.score}, ${f.riskLevel})
                            <button onclick="unmarkFile('${f.path}')" style="margin-left: 10px; font-size: 12px;">取消标记</button>
                        </div>`
                    ).join('');
            } else if (listElement) {
                listElement.innerHTML = '';
            }
        }
        
        function unmarkFile(filePath) {
            markedFiles = markedFiles.filter(f => f.path !== filePath);
            updateMarkedCount();
            
            // 重置对应按钮
            const buttons = document.querySelectorAll('button[onclick*="' + filePath.replace(/"/g, '\\"') + '"]');
            buttons.forEach(btn => {
                if (btn.textContent === '已标记') {
                    btn.textContent = '标记删除';
                    btn.disabled = false;
                    btn.style.backgroundColor = '';
                    btn.style.color = '';
                }
            });
        }
        
        function clearMarked() {
            markedFiles = [];
            updateMarkedCount();
            
            // 重置所有按钮
            const buttons = document.querySelectorAll('button[onclick^="markForDeletion"]');
            buttons.forEach(btn => {
                btn.textContent = '标记删除';
                btn.disabled = false;
                btn.style.backgroundColor = '';
                btn.style.color = '';
            });
        }
        
        function confirmDeletion() {
            if (markedFiles.length === 0) {
                alert('没有标记任何文件');
                return;
            }
            
            const totalSize = markedFiles.reduce((sum, f) => sum + (f.score || 0), 0);
            const highRiskCount = markedFiles.filter(f => f.score >= 60).length;
            
            const message = `确定要删除 ${markedFiles.length} 个文件吗？\n\n` +
                          `高风险文件: ${highRiskCount} 个\n` +
                          `总风险评分: ${totalSize}\n\n` +
                          '文件列表:\n' +
                          markedFiles.map(f => `• ${f.name} (${f.riskLevel})`).join('\n');
            
            if (confirm(message)) {
                generateDeletionScript();
            }
        }
        
        function generateDeletionScript() {
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const script = '#!/bin/bash\n\n' +
                          '# 智能视频分析 - 自动生成的删除脚本\n' +
                          '# 生成时间: ' + new Date().toLocaleString() + '\n' +
                          `# 标记文件数: ${markedFiles.length}\n` +
                          `# 高风险文件数: ${markedFiles.filter(f => f.score >= 60).length}\n\n` +
                          '# 备份原始文件列表\n' +
                          'echo "开始删除操作..."\n' +
                          'echo "删除的文件将记录到 deletion_log_' + timestamp + '.txt"\n\n' +
                          markedFiles.map(f => 
                              `# ${f.name} (评分: ${f.score}, ${f.riskLevel})\n` +
                              `echo "删除: ${f.path}" >> deletion_log_${timestamp}.txt\n` +
                              `rm "${f.path}"`
                          ).join('\n\n') + '\n\n' +
                          'echo "删除操作完成"\n';
            
            const blob = new Blob([script], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `delete_marked_files_${timestamp}.sh`;
            a.click();
            URL.revokeObjectURL(url);
            
            alert('删除脚本已生成并下载，请仔细检查后执行！\n\n注意：删除操作不可逆，请确保备份重要文件。');
        }
        
        // 页面加载完成后初始化
        document.addEventListener('DOMContentLoaded', function() {
            // 添加标记文件显示区域
            const container = document.querySelector('.container');
            if (container) {
                const markedDiv = document.createElement('div');
                markedDiv.innerHTML = `
                    <div style="position: fixed; top: 20px; right: 20px; background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 300px; z-index: 1000;">
                        <h4>标记统计</h4>
                        <p>已标记文件: <span id="markedCount">0</span> 个</p>
                        <button onclick="confirmDeletion()" style="margin-right: 10px;">确认删除</button>
                        <button onclick="clearMarked()">清空标记</button>
                        <div id="markedList" style="margin-top: 10px; max-height: 200px; overflow-y: auto;"></div>
                    </div>
                `;
                document.body.appendChild(markedDiv);
            }
        });
    </script>
</body>
</html>
EOF
    
    log "报告已生成: $REPORT_FILE"
}

# 主函数
main() {
    log "=== 视频文件分析工具启动 ==="
    log "配置文件: $CONFIG_FILE"
    log "视频目录: $VIDEO_BASE_PATH"
    log "日志目录: $LOG_DIR"
    log "报告目录: $REPORT_DIR"
    
    # 检查视频目录是否存在
    if [[ ! -d "$VIDEO_BASE_PATH" ]]; then
        error_exit "视频目录不存在: $VIDEO_BASE_PATH"
    fi
    
    # 检查依赖
    if ! check_dependencies; then
        error_exit "依赖检查失败"
    fi
    
    # 开始分析
    analyze_videos
    
    log "=== 分析完成 ==="
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
视频文件分析工具

用法: $0 [选项]

选项:
  -h, --help     显示此帮助信息
  -c, --config   指定配置文件路径
  -d, --dry-run  仅分析，不进行任何修改
  -v, --verbose  详细输出

示例:
  $0                    # 使用默认配置进行分析
  $0 -c custom.conf     # 使用自定义配置文件
  $0 --dry-run          # 仅分析模式

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
        -v|--verbose)
            VERBOSE="true"
            shift
            ;;
        \#*|先分析|*分析*)
            # 忽略注释和中文描述
            shift
            ;;
        *)
            # 如果参数包含中文或看起来像注释，忽略它
            if [[ "$1" =~ [\u4e00-\u9fff] ]] || [[ "$1" == *"分析"* ]] || [[ "$1" == *"#"* ]]; then
                shift
            else
                echo "未知选项: $1"
                show_help
                exit 1
            fi
            ;;
    esac
done

# 运行主函数
main