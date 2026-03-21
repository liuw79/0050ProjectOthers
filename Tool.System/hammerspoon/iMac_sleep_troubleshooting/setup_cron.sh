#!/bin/bash

# --- Configuration ---
# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MONITOR_SCRIPT_PATH="$SCRIPT_DIR/imac_sleep_monitor.sh"
LAUNCH_AGENT_DIR="$HOME/Library/LaunchAgents"
PLIST_LABEL="com.user.imac.wakeup"
PLIST_FILENAME="$PLIST_LABEL.plist"
PLIST_PATH="$LAUNCH_AGENT_DIR/$PLIST_FILENAME"

# --- Cron Job Setup for Sleep Monitoring ---
CRON_JOB="*/15 * * * * $MONITOR_SCRIPT_PATH"

echo "正在更新用于睡眠监控的 Cron 定时任务..."
# 使用临时文件来安全地更新 crontab，防止重复添加
crontab -l > mycron.tmp 2>/dev/null
# 移除此脚本的任何旧任务
grep -Fv "$MONITOR_SCRIPT_PATH" mycron.tmp > mycron.clean.tmp
# 添加新任务
echo "$CRON_JOB" >> mycron.clean.tmp
# 安装新的 crontab
crontab mycron.clean.tmp
rm mycron.tmp mycron.clean.tmp

if [ $? -eq 0 ]; then
    echo "-> Cron 定时任务已成功更新。"
else
    echo "-> 错误：更新 Cron 定时任务失败。" >&2
fi

# --- Clean Up Old Launch Agent ---
echo "正在清理旧的 Launch Agent (如果存在)..."

if [ -f "$PLIST_PATH" ]; then
    echo "-> 发现旧的 Launch Agent，正在卸载并删除..."
    launchctl unload "$PLIST_PATH" 2>/dev/null
    rm "$PLIST_PATH"
    echo "-> 旧的 Launch Agent 已被移除。"
else
    echo "-> 未发现需要清理的旧 Launch Agent。"
fi

# 加载用于唤醒后恢复服务的 Launch Agent
LAUNCH_AGENT_PLIST="$HOME/Library/LaunchAgents/com.user.wake_up_services.plist"
if [ -f "$LAUNCH_AGENT_PLIST" ]; then
    # 确保脚本有执行权限
    chmod +x "/Users/comdir/SynologyDrive/0050Project/others/Tool.System/hammerspoon/iMac_sleep_troubleshooting/wake_up_services.sh"
    # 加载 Launch Agent
    launchctl load -w "$LAUNCH_AGENT_PLIST"
    echo "-> 用于唤醒后恢复服务的 Launch Agent 已加载。"
fi

echo "设置完成。监控脚本现已更新为在休眠前卸载、唤醒后重载服务。"