#!/bin/bash

# Hammerspoon 电池控制包装脚本
# 用于处理 batt 命令的权限问题

BATT_PATH="/usr/local/bin/batt"

# 使用 osascript 来处理 sudo 密码输入
run_with_sudo() {
    local cmd="$1"
    osascript -e "do shell script \"$cmd\" with administrator privileges"
}

case "$1" in
    "status")
        # 获取电池状态
        run_with_sudo "$BATT_PATH status"
        ;;
    "toggle")
        # 使用状态文件来跟踪当前状态
        STATE_FILE="/tmp/battery_limit_state"
        
        if [ -f "$STATE_FILE" ] && [ "$(cat "$STATE_FILE")" = "80" ]; then
            # 当前是80%限制，切换到100%
            if run_with_sudo "$BATT_PATH limit 100" >/dev/null 2>&1; then
                echo "100" > "$STATE_FILE"
                echo "🔋 电池充电限制已取消，可充满至100%"
            else
                echo "❌ 取消限制失败"
                exit 1
            fi
        else
            # 当前不是80%限制，设置为80%
            if run_with_sudo "$BATT_PATH limit 80" >/dev/null 2>&1; then
                echo "80" > "$STATE_FILE"
                echo "🔋 电池充电限制已设为80%"
            else
                echo "❌ 设置限制失败"
                exit 1
            fi
        fi
        ;;
    *)
        echo "用法: $0 {status|toggle}"
        echo "  status - 显示当前电池状态"
        echo "  toggle - 切换充电限制 (80% <-> 100%)"
        exit 1
        ;;
esac