#!/bin/bash

# 停止 Claude Remote 服务

echo "🛑 停止 Claude Remote 服务..."

# 停止 cloudflared
if [ -f /tmp/claude-remote-cloudflared.pid ]; then
    PID=$(cat /tmp/claude-remote-cloudflared.pid)
    if kill -0 $PID 2>/dev/null; then
        kill $PID
        echo "✅ 已停止内网穿透 (PID: $PID)"
    fi
    rm /tmp/claude-remote-cloudflared.pid
fi

# 停止 node 服务
NODE_PIDS=$(pgrep -f "node src/index.js" 2>/dev/null)
if [ -n "$NODE_PIDS" ]; then
    echo $NODE_PIDS | xargs kill 2>/dev/null
    echo "✅ 已停止主服务"
fi

echo "完成!"
