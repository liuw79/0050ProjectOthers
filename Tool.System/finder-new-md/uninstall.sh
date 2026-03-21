#!/bin/bash

# Finder 右键新建 Markdown 文件功能卸载脚本

set -e

echo "========================================="
echo "  Finder 右键新建 MD 文件 - 卸载程序"
echo "========================================="
echo ""

WORKFLOW_DIR="$HOME/Library/Services"
WORKFLOW_NAME="新建 Markdown 文件.workflow"
WORKFLOW_PATH="${WORKFLOW_DIR}/${WORKFLOW_NAME}"

echo "📝 检查安装状态..."

if [ -d "$WORKFLOW_PATH" ]; then
    echo "✅ 找到已安装的快速操作"
    echo ""
    echo "📝 正在卸载..."
    
    # 删除 workflow
    rm -rf "$WORKFLOW_PATH"
    echo "✅ 已删除快速操作"
    
    # 刷新系统服务
    /System/Library/CoreServices/pbs -flush 2>/dev/null || true
    echo "✅ 已刷新系统服务"
    
    # 可选：重启 Finder
    read -p "是否重启 Finder 使更改立即生效？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        killall Finder
        echo "✅ Finder 已重启"
    fi
    
    echo ""
    echo "========================================="
    echo "  ✅ 卸载完成！"
    echo "========================================="
else
    echo "⚠️  未找到已安装的快速操作"
    echo ""
    echo "可能的原因："
    echo "1. 尚未安装"
    echo "2. 已被手动删除"
    echo ""
fi
