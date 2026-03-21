#!/bin/bash

# 最简单的方案：直接在应用程序中创建一个可点击的脚本

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_NAME="新建MD文件.app"
APP_PATH="$HOME/Applications/$APP_NAME"

echo "========================================="
echo "  创建独立应用（最简单方案）"
echo "========================================="
echo ""

# 创建应用包结构
mkdir -p "$APP_PATH/Contents/MacOS"
mkdir -p "$APP_PATH/Contents/Resources"

# 创建主脚本
cat > "$APP_PATH/Contents/MacOS/新建MD文件" << 'MAINSCRIPT'
#!/bin/bash

# 获取当前 Finder 目录
current_dir=$(osascript -e 'tell application "Finder" to POSIX path of (insertion location as alias)' 2>/dev/null)

# 如果获取失败，使用桌面
if [ -z "$current_dir" ] || [ ! -d "$current_dir" ]; then
    current_dir="$HOME/Desktop"
fi

# 生成唯一文件名
base_name="未命名"
extension=".md"
counter=1
file_name="${base_name}${extension}"
file_path="${current_dir}/${file_name}"

while [ -e "$file_path" ]; do
    file_name="${base_name}${counter}${extension}"
    file_path="${current_dir}/${file_name}"
    ((counter++))
done

# 创建文件
cat > "$file_path" << 'EOF'
# 标题

## 简介

内容...

## 详细信息

EOF

# 在 Finder 中显示
open -R "$file_path"

exit 0
MAINSCRIPT

chmod +x "$APP_PATH/Contents/MacOS/新建MD文件"

# 创建 Info.plist
cat > "$APP_PATH/Contents/Info.plist" << 'INFOPLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>新建MD文件</string>
    <key>CFBundleName</key>
    <string>新建MD文件</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleIdentifier</key>
    <string>com.toolsystem.newmd</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>LSUIElement</key>
    <true/>
</dict>
</plist>
INFOPLIST

echo "✅ 应用已创建：$APP_PATH"
echo ""
echo "========================================="
echo "  使用方法"
echo "========================================="
echo ""
echo "方式 1：双击运行"
echo "  打开 ~/Applications/"
echo "  双击「新建MD文件.app」"
echo "  会在当前 Finder 目录创建 MD 文件"
echo ""
echo "方式 2：拖到 Dock"
echo "  将「新建MD文件.app」拖到 Dock"
echo "  需要时点击即可"
echo ""
echo "方式 3：设置快捷键"
echo "  系统设置 → 键盘 → 键盘快捷键 → App 快捷键"
echo "  添加该应用的快捷键"
echo ""
echo "========================================="
echo ""

# 打开应用程序文件夹
open ~/Applications/

echo "✅ 已打开应用程序文件夹，你可以看到「新建MD文件.app」"
