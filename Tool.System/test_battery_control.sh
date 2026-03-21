#!/bin/bash

echo "=== 电池控制功能测试 ==="
echo "测试时间: $(date)"
echo ""

echo "1. 测试脚本权限..."
if [ -x "/Users/comdir/SynologyDrive/0050Project/Tool.System/hammerspoon/battery_control_wrapper.sh" ]; then
    echo "✅ 脚本有执行权限"
else
    echo "❌ 脚本没有执行权限"
    exit 1
fi

echo ""
echo "2. 测试脚本功能..."
echo "当前状态:"
sudo /usr/local/bin/batt status | grep -E "(Upper limit|Charge limit|Allow charging)"

echo ""
echo "执行切换..."
/Users/comdir/SynologyDrive/0050Project/Tool.System/hammerspoon/battery_control_wrapper.sh toggle

echo ""
echo "切换后状态:"
sudo /usr/local/bin/batt status | grep -E "(Upper limit|Charge limit|Allow charging)"

echo ""
echo "再次切换..."
/Users/comdir/SynologyDrive/0050Project/Tool.System/hammerspoon/battery_control_wrapper.sh toggle

echo ""
echo "最终状态:"
sudo /usr/local/bin/batt status | grep -E "(Upper limit|Charge limit|Allow charging)"

echo ""
echo "=== 测试完成 ==="