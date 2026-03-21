#!/bin/bash

# 安装 Claude Remote 为系统服务（自动恢复）

cd "$(dirname "$0")/.."

echo "📦 安装 Claude Remote 系统服务..."

# 停止现有的 node 进程
pkill -f "node src/index.js" 2>/dev/null

# 复制 plist 到 LaunchAgents
cp com.claude-remote.plist ~/Library/LaunchAgents/

# 加载服务
launchctl unload ~/Library/LaunchAgents/com.claude-remote.plist 2>/dev/null
launchctl load ~/Library/LaunchAgents/com.claude-remote.plist

echo "✅ 服务已安装并启动"
echo ""
echo "功能："
echo "  - 开机自动启动"
echo "  - 崩溃后自动重启"
echo "  - 休眠唤醒后自动恢复"
echo ""
echo "日志位置: /tmp/claude-remote.log"
echo ""
echo "管理命令："
echo "  停止: launchctl stop com.claude-remote"
echo "  启动: launchctl start com.claude-remote"
echo "  卸载: ./scripts/uninstall-service.sh"
