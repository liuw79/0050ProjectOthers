#!/bin/bash

echo "🔋 电池控制快捷键测试"
echo "===================="
echo ""
echo "📋 测试步骤："
echo "1. 确保 Hammerspoon 正在运行"
echo "2. 按下快捷键 Cmd+Shift+B"
echo "3. 观察是否出现电池控制提示"
echo ""

# 检查 Hammerspoon 状态
if pgrep -f "Hammerspoon" > /dev/null; then
    echo "✅ Hammerspoon 正在运行"
else
    echo "❌ Hammerspoon 未运行，请先启动 Hammerspoon"
    exit 1
fi

# 显示当前电池状态
echo ""
echo "📊 当前电池状态："
if command -v batt &> /dev/null; then
    batt status
else
    echo "❌ batt 命令未找到"
fi

echo ""
echo "🎯 现在请按下快捷键 Cmd+Shift+B 来测试电池控制功能"
echo "如果快捷键不工作，可能的原因："
echo "- 其他应用程序占用了相同的快捷键"
echo "- 需要在系统偏好设置中给 Hammerspoon 辅助功能权限"
echo "- 可以尝试使用不同的快捷键组合"

echo ""
echo "💡 替代方案："
echo "如果快捷键不工作，可以直接运行脚本："
echo "   ./battery_control_wrapper.sh toggle"