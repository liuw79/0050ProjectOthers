#!/bin/bash

# 脚本：在系统唤醒时重新加载必要的服务

LOG_FILE="/Users/liuwei/SynologyDrive/0050Project/Tool.System/iMac_sleep_troubleshooting/imac_sleep_log.txt"
CURRENT_TIME=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$CURRENT_TIME] 系统唤醒，正在重新加载服务..." >> "$LOG_FILE"

# 重新加载 coreaudiod 服务
sudo launchctl load /System/Library/LaunchDaemons/com.apple.audio.coreaudiod.plist 2>>"$LOG_FILE"

echo "[$CURRENT_TIME] coreaudiod 服务已重新加载。" >> "$LOG_FILE"