#!/bin/bash

# 手动刷新系统服务的完整脚本

echo "========================================="
echo "  刷新 Finder 快速操作"
echo "========================================="
echo ""

WORKFLOW_PATH="$HOME/Library/Services/新建 Markdown 文件.workflow"

if [ ! -d "$WORKFLOW_PATH" ]; then
    echo "❌ 错误：找不到 workflow 文件"
    echo "请先运行 install.sh"
    exit 1
fi

echo "✅ Workflow 文件存在"
echo ""

echo "📝 步骤 1: 刷新系统服务数据库..."
/System/Library/CoreServices/pbs -flush 2>/dev/null || true
/System/Library/CoreServices/pbs -update 2>/dev/null || true
echo "✅ 完成"

echo ""
echo "📝 步骤 2: 更新文件时间戳..."
touch "$WORKFLOW_PATH"
touch "$WORKFLOW_PATH/Contents/Info.plist"
touch "$WORKFLOW_PATH/Contents/document.wflow"
echo "✅ 完成"

echo ""
echo "📝 步骤 3: 重启 Finder..."
killall Finder
echo "✅ Finder 已重启"

echo ""
echo "📝 步骤 4: 在 Automator 中打开并保存..."
echo "正在打开 Automator..."
open -a Automator "$WORKFLOW_PATH"

echo ""
echo "========================================="
echo "  ⚠️  请完成以下操作"
echo "========================================="
echo ""
echo "1. 等待 Automator 打开（可能需要几秒钟）"
echo "2. 在 Automator 中按 ⌘S 保存"
echo "3. 关闭 Automator"
echo "4. 回到 Finder，在任意文件夹右键测试"
echo ""
echo "如果仍然看不到，请尝试："
echo "• 注销并重新登录"
echo "• 或重启电脑"
echo ""
echo "========================================="
echo ""
