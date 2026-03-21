#!/bin/bash

# 创建新 Markdown 文件的脚本
# 用于 Finder 右键快速操作

# 获取当前 Finder 目录
if [ -n "$1" ]; then
    # 如果传入了参数，使用传入的路径
    target_dir="$1"
else
    # 否则获取当前 Finder 窗口的路径
    target_dir=$(osascript -e 'tell application "Finder" to POSIX path of (insertion location as alias)')
fi

# 如果 target_dir 是文件而不是目录，获取其父目录
if [ -f "$target_dir" ]; then
    target_dir=$(dirname "$target_dir")
fi

# 确保路径存在
if [ ! -d "$target_dir" ]; then
    osascript -e 'display notification "无法确定目标目录" with title "新建 Markdown 文件"'
    exit 1
fi

# 生成文件名
base_name="未命名"
extension=".md"
counter=1
file_name="${base_name}${extension}"
file_path="${target_dir}/${file_name}"

# 如果文件已存在，添加数字后缀
while [ -e "$file_path" ]; do
    file_name="${base_name}${counter}${extension}"
    file_path="${target_dir}/${file_name}"
    ((counter++))
done

# 创建文件并写入基本模板
cat > "$file_path" << 'EOF'
# 标题

## 简介

内容...

## 详细信息

EOF

# 在 Finder 中显示并选中新文件
osascript <<-APPLESCRIPT
    tell application "Finder"
        activate
        reveal POSIX file "$file_path"
        select POSIX file "$file_path"
    end tell
APPLESCRIPT

# 显示通知
osascript -e "display notification \"已创建: ${file_name}\" with title \"新建 Markdown 文件\""

# 延迟后自动进入重命名模式
sleep 0.3
osascript -e 'tell application "System Events" to keystroke return'

exit 0
