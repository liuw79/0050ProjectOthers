#!/bin/bash

# 使用 AppleScript 方式创建快速操作的替代安装方案

set -e

echo "========================================="
echo "  方案 B: AppleScript 方式安装"
echo "========================================="
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APPLESCRIPT_PATH="${SCRIPT_DIR}/create_new_md.scpt"

# 编译 AppleScript
echo "📝 步骤 1: 编译 AppleScript..."
if [ -f "$APPLESCRIPT_PATH" ]; then
    osacompile -o "${SCRIPT_DIR}/create_new_md.scptd" "$APPLESCRIPT_PATH"
    echo "✅ AppleScript 已编译"
else
    echo "❌ 找不到 AppleScript 文件"
    exit 1
fi

# Automator 工作流路径
WORKFLOW_DIR="$HOME/Library/Services"
WORKFLOW_NAME="新建 Markdown 文件 v2.workflow"
WORKFLOW_PATH="${WORKFLOW_DIR}/${WORKFLOW_NAME}"

echo ""
echo "📝 步骤 2: 创建 Automator 快速操作（AppleScript 版本）..."

mkdir -p "$WORKFLOW_DIR"
mkdir -p "$WORKFLOW_PATH/Contents"

# 创建 Info.plist
cat > "$WORKFLOW_PATH/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSServices</key>
    <array>
        <dict>
            <key>NSBackgroundColorName</key>
            <string>background</string>
            <key>NSIconName</key>
            <string>NSTouchBarCompose</string>
            <key>NSMenuItem</key>
            <dict>
                <key>default</key>
                <string>新建 Markdown 文件 v2</string>
            </dict>
            <key>NSMessage</key>
            <string>runWorkflowAsService</string>
            <key>NSRequiredContext</key>
            <dict>
                <key>NSApplicationIdentifier</key>
                <string>com.apple.finder</string>
            </dict>
        </dict>
    </array>
</dict>
</plist>
EOF

# 创建 document.wflow（使用 AppleScript）
cat > "$WORKFLOW_PATH/Contents/document.wflow" << 'WFLOW'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>actions</key>
    <array>
        <dict>
            <key>action</key>
            <dict>
                <key>ActionBundlePath</key>
                <string>/System/Library/Automator/Run AppleScript.action</string>
                <key>ActionName</key>
                <string>运行 AppleScript</string>
                <key>ActionParameters</key>
                <dict>
                    <key>source</key>
                    <string>on run {input, parameters}
    -- 获取 Finder 当前目录
    tell application "Finder"
        try
            set currentFolder to (insertion location as alias)
        on error
            set currentFolder to (path to desktop folder)
        end try
        set targetPath to POSIX path of currentFolder
    end tell
    
    -- 生成唯一文件名
    set baseName to "未命名"
    set fileExtension to ".md"
    set counter to 0
    set fileName to baseName & fileExtension
    set filePath to targetPath & fileName
    
    tell application "System Events"
        repeat while exists disk item filePath
            set counter to counter + 1
            set fileName to baseName & counter & fileExtension
            set filePath to targetPath & fileName
        end repeat
    end tell
    
    -- 创建文件
    set fileContent to "# 标题

## 简介

内容...

## 详细信息

"
    
    try
        set fileRef to open for access POSIX file filePath with write permission
        set eof fileRef to 0
        write fileContent to fileRef as «class utf8»
        close access fileRef
    on error errMsg
        try
            close access POSIX file filePath
        end try
        return input
    end try
    
    -- 在 Finder 中显示
    tell application "Finder"
        reveal POSIX file filePath
        select POSIX file filePath
    end tell
    
    display notification "已创建: " & fileName with title "新建 Markdown 文件"
    
    delay 0.3
    tell application "System Events"
        keystroke return
    end tell
    
    return input
end run</string>
                </dict>
            </dict>
        </dict>
    </array>
    <key>connectors</key>
    <dict/>
    <key>workflowMetaData</key>
    <dict>
        <key>serviceApplicationBundleID</key>
        <string>com.apple.finder</string>
        <key>serviceInputTypeIdentifier</key>
        <string>com.apple.Automator.nothing</string>
        <key>serviceOutputTypeIdentifier</key>
        <string>com.apple.Automator.nothing</string>
        <key>workflowTypeIdentifier</key>
        <string>com.apple.Automator.servicesMenu</string>
    </dict>
</dict>
</plist>
WFLOW

echo "✅ 快速操作已创建"

echo ""
echo "📝 步骤 3: 在 Automator 中打开并保存..."
open -a Automator "$WORKFLOW_PATH"

echo ""
echo "========================================="
echo "  ⚠️  重要：请完成以下操作"
echo "========================================="
echo ""
echo "1. 等待 Automator 打开"
echo "2. 按 ⌘S 保存"
echo "3. 关闭 Automator"
echo "4. 在 Finder 右键菜单中查找"
echo "   「快速操作」→「新建 Markdown 文件 v2」"
echo ""
echo "如果仍然不显示，请尝试："
echo "• 注销并重新登录（最有效）"
echo "• 或运行: killall Finder"
echo ""
