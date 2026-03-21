#!/bin/bash

# 本地版本的动画文件夹重命名脚本
# 通过 Finder 挂载的 SMB 共享进行操作

# 定义日志文件
LOG_DIR="$(dirname "$0")/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/rename_anime_folders_local_$(date +%Y%m%d_%H%M%S).log"

# 日志函数
log() {
  local message="$1"
  local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
  echo "[$timestamp] $message" | tee -a "$LOG_FILE"
}

# 检查挂载点
check_mount() {
  local mount_point="/Volumes/video"
  
  if [ ! -d "$mount_point" ]; then
    log "错误: 未找到挂载点 $mount_point"
    log "请先在 Finder 中连接到 smb://DS920plus._smb._tcp.local/video"
    log "或者手动挂载: open 'smb://DS920plus._smb._tcp.local/video'"
    return 1
  fi
  
  log "找到挂载点: $mount_point"
  return 0
}

# 自动挂载SMB共享
auto_mount() {
  log "尝试自动挂载 SMB 共享..."
  
  # 使用 osascript 打开 SMB 连接
  osascript -e 'tell application "Finder" to open location "smb://DS920plus._smb._tcp.local/video"' 2>/dev/null
  
  # 等待挂载完成
  sleep 3
  
  if check_mount; then
    return 0
  else
    log "自动挂载失败，请手动连接"
    return 1
  fi
}

# 重命名函数
rename_folders() {
  local base_path="/Volumes/video"
  
  # 检查动画目录是否存在
  local anime_path="$base_path/动画"
  if [ ! -d "$anime_path" ]; then
    log "未找到动画目录: $anime_path"
    log "将在 $base_path 中查找英文目录进行重命名"
  fi
  
  log "开始重命名文件夹..."
  
  # 英文文件夹名和对应的中文名称映射
  declare -A folder_map=(
    ["Anime"]="动画"
    ["Animation"]="动画片"
    ["Cartoon"]="卡通"
    ["Japanese_Anime"]="日本动画"
    ["Chinese_Animation"]="国产动画"
    ["Western_Animation"]="欧美动画"
    ["Movies"]="电影"
    ["TV_Series"]="电视剧"
    ["Documentary"]="纪录片"
    ["Kids"]="儿童"
    ["Family"]="家庭"
    ["Action"]="动作"
    ["Comedy"]="喜剧"
    ["Drama"]="剧情"
    ["Horror"]="恐怖"
    ["Sci-Fi"]="科幻"
    ["Fantasy"]="奇幻"
    ["Romance"]="爱情"
    ["Thriller"]="惊悚"
  )
  
  # 获取所有一级目录
  for folder in "$base_path"/*; do
    if [ -d "$folder" ]; then
      folder_name=$(basename "$folder")
      
      # 跳过已经是中文的文件夹
      if [[ "$folder_name" =~ [\u4e00-\u9fff] ]]; then
        log "跳过中文文件夹: $folder_name"
        continue
      fi
      
      # 检查是否在映射列表中
      if [[ -n "${folder_map[$folder_name]}" ]]; then
        chinese_name="${folder_map[$folder_name]}"
        new_path="$base_path/$chinese_name"
        
        # 检查目标文件夹是否已存在
        if [ -d "$new_path" ]; then
          log "警告: 目标文件夹 '$chinese_name' 已存在，跳过重命名 '$folder_name'"
          continue
        fi
        
        # 执行重命名
        if mv "$folder" "$new_path" 2>/dev/null; then
          log "成功: '$folder_name' 已重命名为 '$chinese_name'"
        else
          log "错误: 无法重命名 '$folder_name' 到 '$chinese_name'"
        fi
      else
        log "信息: 未找到 '$folder_name' 的中文映射，保持原名"
      fi
    fi
  done
  
  log "文件夹重命名完成"
}

# 显示当前目录结构
show_structure() {
  local base_path="/Volumes/video"
  
  log "当前目录结构:"
  if [ -d "$base_path" ]; then
    ls -la "$base_path" | while read line; do
      log "  $line"
    done
  else
    log "  无法访问 $base_path"
  fi
}

# 主函数
main() {
  log "=== 开始本地动画文件夹重命名任务 ==="
  
  # 检查挂载点，如果不存在则尝试自动挂载
  if ! check_mount; then
    if ! auto_mount; then
      log "请手动连接到 SMB 共享后重新运行脚本"
      log "连接地址: smb://DS920plus._smb._tcp.local/video"
      exit 1
    fi
  fi
  
  show_structure
  rename_folders
  show_structure
  
  log "=== 本地动画文件夹重命名任务完成 ==="
}

# 执行主函数
main