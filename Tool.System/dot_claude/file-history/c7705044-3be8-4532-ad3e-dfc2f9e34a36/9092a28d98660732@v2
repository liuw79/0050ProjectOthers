#!/bin/bash

# 卸载 Claude Remote 系统服务

echo "🗑️ 卸载 Claude Remote 系统服务..."

# 停止并卸载
launchctl unload ~/Library/LaunchAgents/com.claude-remote.plist 2>/dev/null

# 删除 plist 文件
rm -f ~/Library/LaunchAgents/com.claude-remote.plist

echo "✅ 服务已卸载"
