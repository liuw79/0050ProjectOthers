#!/bin/bash
# reset_media_keys.sh — 重新生成 macOS 的媒体键快捷键表（F7-F9）
# 使用场景：F7-F9 必须按 Fn 键才工作，或媒体键失效时。
# 说明：执行后需要注销/重启才能完全生效。

set -e

echo "[reset_media_keys] 删除 AppleSymbolicHotKeys..."
# 删除全局 AppleSymbolicHotKeys 表（若不存在会返回错误码 1，忽略）
defaults delete com.apple.symbolichotkeys AppleSymbolicHotKeys 2>/dev/null || true

echo "[reset_media_keys] 重启 cfprefsd 缓存进程..."
killall cfprefsd || true

echo "[reset_media_keys] 已完成。请注销或重启电脑后测试 F7-F9 是否直接触发媒体控制。"