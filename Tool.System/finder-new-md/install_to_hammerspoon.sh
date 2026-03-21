#!/bin/bash

# 自动安装到 Hammerspoon

set -e

echo "========================================="
echo "  Hammerspoon 方案安装"
echo "========================================="
echo ""

# 检查 Hammerspoon 是否安装
if [ ! -d "$HOME/.hammerspoon" ]; then
    echo "❌ 未找到 Hammerspoon 配置目录"
    echo ""
    echo "请先安装 Hammerspoon:"
    echo "  https://www.hammerspoon.org/"
    echo ""
    echo "或者你的 Hammerspoon 配置在其他位置，"
    echo "请手动按照文档配置。"
    exit 1
fi

echo "✅ 找到 Hammerspoon 配置目录"

# 源文件路径
SPOON_SOURCE="/Users/comdir/SynologyDrive/0050Project/others/Tool.System/hammerspoon/Spoons/NewMarkdownFile.spoon"
SPOON_TARGET="$HOME/.hammerspoon/Spoons/NewMarkdownFile.spoon"
INIT_FILE="$HOME/.hammerspoon/init.lua"

# 创建 Spoons 目录
mkdir -p "$HOME/.hammerspoon/Spoons"

# 复制 Spoon
echo ""
echo "📝 步骤 1: 复制 Spoon..."
if [ -d "$SPOON_TARGET" ]; then
    echo "⚠️  Spoon 已存在，正在备份..."
    mv "$SPOON_TARGET" "$SPOON_TARGET.backup.$(date +%Y%m%d%H%M%S)"
fi

cp -r "$SPOON_SOURCE" "$SPOON_TARGET"
echo "✅ Spoon 已复制"

# 检查 init.lua 中是否已有配置
echo ""
echo "📝 步骤 2: 配置 init.lua..."

if grep -q "NewMarkdownFile" "$INIT_FILE" 2>/dev/null; then
    echo "⚠️  init.lua 中已有 NewMarkdownFile 配置"
    echo "   请手动检查配置是否正确"
else
    # 添加配置
    cat >> "$INIT_FILE" << 'EOF'

-- ========================================
-- 新建 Markdown 文件快捷键 (⌘⇧M)
-- ========================================
hs.loadSpoon("NewMarkdownFile")
spoon.NewMarkdownFile:bindHotkeys({
    createMarkdown = {{"cmd", "shift"}, "M"}
})

EOF
    echo "✅ 已添加配置到 init.lua"
fi

# 重新加载 Hammerspoon
echo ""
echo "📝 步骤 3: 重新加载 Hammerspoon..."

osascript <<'APPLESCRIPT' 2>/dev/null || true
tell application "Hammerspoon"
    execute lua code "hs.reload()"
end tell
APPLESCRIPT

echo "✅ 已发送重新加载命令"

echo ""
echo "========================================="
echo "  ✅ 安装完成！"
echo "========================================="
echo ""
echo "🚀 使用方法:"
echo "  在 Finder 中按 ⌘⇧M 创建 Markdown 文件"
echo ""
echo "💡 提示:"
echo "  1. 确保 Hammerspoon 正在运行（菜单栏有图标）"
echo "  2. 如果没有自动重新加载，请手动:"
echo "     点击 Hammerspoon 图标 → Reload Config"
echo "  3. 应该会看到提示:「新建 MD 快捷键已启用」"
echo ""
echo "🔧 自定义快捷键:"
echo "  编辑 ~/.hammerspoon/init.lua"
echo "  修改快捷键配置部分"
echo ""
echo "========================================="
echo ""
