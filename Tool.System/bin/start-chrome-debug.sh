#!/bin/bash
# 启动 Chrome 并开启 CDP 调试端口
# 用于 OpenClaw/Clawdbot 浏览器自动化

DEBUG_PORT=${1:-9222}

echo "启动 Chrome 调试模式 (端口: $DEBUG_PORT)..."

# 检查是否已经在运行
if lsof -i :$DEBUG_PORT > /dev/null 2>&1; then
    echo "端口 $DEBUG_PORT 已被占用，可能 Chrome 调试模式已在运行"
    echo "如需重启，请先关闭现有 Chrome 窗口"
    exit 1
fi

# macOS 启动 Chrome
if [[ "$OSTYPE" == "darwin"* ]]; then
    # 使用用户数据目录，保持登录状态
    /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
        --remote-debugging-port=$DEBUG_PORT \
        --user-data-dir="$HOME/.chrome-debug-profile" \
        &
else
    # Linux
    google-chrome \
        --remote-debugging-port=$DEBUG_PORT \
        --user-data-dir="$HOME/.chrome-debug-profile" \
        &
fi

echo "Chrome 已启动!"
echo "调试地址: http://127.0.0.1:$DEBUG_PORT"
echo ""
echo "现在可以启动 clawdbot gateway:"
echo "  clawdbot gateway"
