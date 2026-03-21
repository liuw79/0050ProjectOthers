#!/bin/bash

# 获取当前 Finder 目录
if [ -n "$1" ]; then
    target_dir="$1"
else
    target_dir=$(osascript -e 'tell application "Finder" to POSIX path of (insertion location as alias)')
fi

# 如果是文件，获取其父目录
if [ -f "$target_dir" ]; then
    target_dir=$(dirname "$target_dir")
fi

# 确保路径存在
if [ ! -d "$target_dir" ]; then
    osascript -e 'display notification "无法确定目标目录" with title "新建 Markdown 文件"'
    exit 1
fi

# 生成唯一文件名
base_name="未命名"
extension=".md"
counter=1
file_name="${base_name}${extension}"
file_path="${target_dir}/${file_name}"

while [ -e "$file_path" ]; do
    file_name="${base_name}${counter}${extension}"
    file_path="${target_dir}/${file_name}"
    ((counter++))
done

# 创建文件
cat > "$file_path" << 'EOF'
# 标题

## 简介

内容...

## 详细信息

EOF

# 在 Finder 中显示并选中
osascript <<APPLESCRIPT
    tell application "Finder"
        activate
        reveal POSIX file "$file_path"
        select POSIX file "$file_path"
    end tell
APPLESCRIPT

# 显示通知
osascript -e "display notification \"已创建: ${file_name}\" with title \"新建 Markdown 文件\""

# 进入重命名模式
sleep 0.3
osascript -e 'tell application "System Events" to keystroke return'
