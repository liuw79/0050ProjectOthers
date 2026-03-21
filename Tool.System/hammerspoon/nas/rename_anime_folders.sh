#!/bin/bash

# 加载NAS连接配置
source "$(dirname "$0")/nas_connection.conf"

# 定义日志文件
LOG_DIR="$(dirname "$0")/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/rename_anime_folders_$(date +%Y%m%d_%H%M%S).log"

# 日志函数
log() {
  local message="$1"
  local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
  echo "[$timestamp] $message" | tee -a "$LOG_FILE"
}

# 检查SSH连接
check_connection() {
  log "检查NAS连接..."
  if ! eval "$NAS_SSH_CONNECTION 'echo Connection successful'" &>/dev/null; then
    log "错误: 无法连接到NAS，请检查网络连接和凭据"
    exit 1
  fi
  log "NAS连接成功"
}

# 重命名函数
rename_folders() {
  local video_path="$NAS_REMOTE_PATH/video"
  
  log "开始重命名动画文件夹..."
  
  # 英文文件夹名和对应的中文名称映射
  declare -A folder_map=(
    ["Anime"]="动画"
    ["Animation"]="动画"
    ["Cartoon"]="卡通"
    ["Japanese_Anime"]="日本动画"
    ["Chinese_Animation"]="国产动画"
    ["Western_Animation"]="欧美动画"
    ["Movies"]="电影"
    ["TV_Series"]="电视剧"
    ["Documentary"]="纪录片"
  )
  
  # 获取视频目录下的所有文件夹
  local folders=$(eval "$NAS_SSH_CONNECTION 'find $video_path -maxdepth 1 -type d -not -path "$video_path"'")
  
  if [ -z "$folders" ]; then
    log "警告: 未找到任何文件夹"
    return
  fi
  
  # 遍历所有文件夹并重命名
  echo "$folders" | while read folder; do
    folder_name=$(basename "$folder")
    
    # 检查是否在映射列表中
    for eng_name in "${!folder_map[@]}"; do
      if [ "$folder_name" = "$eng_name" ]; then
        chinese_name="${folder_map[$eng_name]}"
        parent_dir=$(dirname "$folder")
        new_path="$parent_dir/$chinese_name"
        
        # 检查目标文件夹是否已存在
        if eval "$NAS_SSH_CONNECTION '[ -d "$new_path" ]'" &>/dev/null; then
          log "警告: 目标文件夹 '$chinese_name' 已存在，跳过重命名 '$folder_name'"
          continue
        fi
        
        # 执行重命名
        if eval "$NAS_SSH_CONNECTION 'mv "$folder" "$new_path"'" &>/dev/null; then
          log "成功: '$folder_name' 已重命名为 '$chinese_name'"
        else
          log "错误: 无法重命名 '$folder_name' 到 '$chinese_name'"
        fi
        break
      fi
    done
  done
  
  log "文件夹重命名完成"
}

# 主函数
main() {
  log "=== 开始动画文件夹重命名任务 ==="
  check_connection
  rename_folders
  log "=== 动画文件夹重命名任务完成 ==="
}

# 执行主函数
main