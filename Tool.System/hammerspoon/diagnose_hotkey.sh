#!/bin/bash

echo "🔍 Hammerspoon 快捷键诊断工具"
echo "================================"

# 检查 Hammerspoon 是否运行
echo "1. 检查 Hammerspoon 进程..."
if pgrep -f "Hammerspoon" > /dev/null; then
    echo "✅ Hammerspoon 正在运行"
    ps aux | grep -i hammerspoon | grep -v grep
else
    echo "❌ Hammerspoon 未运行"
    exit 1
fi

echo ""

# 检查配置文件
echo "2. 检查配置文件..."
HAMMERSPOON_CONFIG="$HOME/.hammerspoon"
if [ -d "$HAMMERSPOON_CONFIG" ]; then
    echo "✅ Hammerspoon 配置目录存在: $HAMMERSPOON_CONFIG"
    if [ -f "$HAMMERSPOON_CONFIG/init.lua" ]; then
        echo "✅ init.lua 文件存在"
    else
        echo "❌ init.lua 文件不存在"
    fi
else
    echo "❌ Hammerspoon 配置目录不存在"
fi

echo ""

# 检查当前目录的配置
echo "3. 检查当前目录配置..."
CURRENT_CONFIG="$(pwd)"
echo "📍 当前配置目录: $CURRENT_CONFIG"
if [ -f "$CURRENT_CONFIG/init.lua" ]; then
    echo "✅ 当前目录有 init.lua"
else
    echo "❌ 当前目录没有 init.lua"
fi

echo ""

# 检查电池控制脚本
echo "4. 检查电池控制脚本..."
BATTERY_SCRIPT="$CURRENT_CONFIG/battery_control_wrapper.sh"
if [ -f "$BATTERY_SCRIPT" ]; then
    echo "✅ 电池控制脚本存在: $BATTERY_SCRIPT"
    if [ -x "$BATTERY_SCRIPT" ]; then
        echo "✅ 脚本有执行权限"
    else
        echo "⚠️  脚本没有执行权限"
    fi
else
    echo "❌ 电池控制脚本不存在"
fi

echo ""

# 提供解决方案
echo "5. 解决方案建议..."
echo "如果快捷键不工作，可能的原因："
echo "- 其他应用程序占用了相同的快捷键"
echo "- Hammerspoon 配置没有正确加载"
echo "- 需要重新加载 Hammerspoon 配置"

echo ""
echo "建议操作："
echo "1. 打开 Hammerspoon 应用"
echo "2. 点击菜单栏的 Hammerspoon 图标"
echo "3. 选择 'Reload Config'"
echo "4. 或者尝试不同的快捷键组合"