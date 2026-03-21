#!/bin/bash

# 创建新 Markdown 文件（不需要辅助功能权限的版本）

# 获取当前 Finder 目录
if [ -n "$1" ]; then
    target_dir="$1"
else
    target_dir=$(osascript -e 'tell application "Finder" to POSIX path of (insertion location as alias)' 2>/dev/null)
fi

# 如果获取失败，使用桌面
if [ -z "$target_dir" ] || [ ! -d "$target_dir" ]; then
    target_dir="$HOME/Desktop"
fi

# 如果是文件，获取其父目录
if [ -f "$target_dir" ]; then
    target_dir=$(dirname "$target_dir")
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

# 在 Finder 中显示并选中（不使用 System Events，避免权限问题）
osascript <<APPLESCRIPT 2>/dev/null
    tell application "Finder"
        reveal POSIX file "$file_path"
        select POSIX file "$file_path"
    end tell
APPLESCRIPT

# 显示通知
osascript -e "display notification \"已创建: ${file_name}，按回车键重命名\" with title \"新建 Markdown 文件\"" 2>/dev/null

exit 0
