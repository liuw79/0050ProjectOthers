#!/bin/bash

# Hammerspoon 电池控制命令行脚本
# 用于在没有菜单栏图标时通过命令行控制电池功能

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 显示帮助信息
show_help() {
    echo -e "${BLUE}🔋 Hammerspoon 电池控制脚本${NC}"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  status          显示电池状态"
    echo "  protect on      启用充电保护"
    echo "  protect off     禁用充电保护"
    echo "  limit <数值>    设置充电限制 (60-100)"
    echo "  discharge <数值> 设置放电限制 (10-40)"
    echo "  monitor         实时监控电池状态"
    echo "  help            显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 status                # 显示电池状态"
    echo "  $0 protect on           # 启用充电保护"
    echo "  $0 limit 80             # 设置充电限制为80%"
    echo "  $0 discharge 20         # 设置放电限制为20%"
    echo ""
}

# 获取电池状态
get_battery_status() {
    local battery_info=$(pmset -g batt)
    local percentage=$(echo "$battery_info" | grep -o '[0-9]*%' | head -1 | tr -d '%')
    local charging_status=$(echo "$battery_info" | grep -o 'AC Power\|Battery Power')
    local is_charging=$(echo "$battery_info" | grep -o 'charging\|charged\|discharging')
    
    echo -e "${GREEN}🔋 电池状态${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "电量: ${YELLOW}${percentage}%${NC}"
    
    case "$is_charging" in
        "charging")
            echo -e "状态: ${GREEN}🔌 充电中${NC}"
            ;;
        "charged")
            echo -e "状态: ${GREEN}🔋 已充满${NC}"
            ;;
        "discharging")
            echo -e "状态: ${YELLOW}🔋 使用电池${NC}"
            ;;
    esac
    
    echo -e "电源: ${charging_status}"
    echo ""
}

# 发送 Hammerspoon 命令
send_hs_command() {
    local command="$1"
    if command -v hs >/dev/null 2>&1; then
        hs -c "$command"
    else
        echo -e "${RED}❌ Hammerspoon 命令行工具未安装${NC}"
        echo "请在 Hammerspoon 中安装 IPC 命令行工具"
        return 1
    fi
}

# 启用/禁用充电保护
toggle_protection() {
    local action="$1"
    case "$action" in
        "on")
            echo -e "${GREEN}✅ 启用充电保护${NC}"
            send_hs_command "toggleChargeProtection()"
            ;;
        "off")
            echo -e "${YELLOW}❌ 禁用充电保护${NC}"
            send_hs_command "toggleChargeProtection()"
            ;;
        *)
            echo -e "${RED}错误: 请指定 'on' 或 'off'${NC}"
            return 1
            ;;
    esac
}

# 设置充电限制
set_charge_limit() {
    local limit="$1"
    if [[ "$limit" =~ ^[0-9]+$ ]] && [ "$limit" -ge 60 ] && [ "$limit" -le 100 ]; then
        echo -e "${GREEN}🔋 设置充电限制为 ${limit}%${NC}"
        send_hs_command "setChargeLimit($limit)"
    else
        echo -e "${RED}错误: 充电限制必须是 60-100 之间的数字${NC}"
        return 1
    fi
}

# 设置放电限制
set_discharge_limit() {
    local limit="$1"
    if [[ "$limit" =~ ^[0-9]+$ ]] && [ "$limit" -ge 10 ] && [ "$limit" -le 40 ]; then
        echo -e "${GREEN}🔋 设置放电限制为 ${limit}%${NC}"
        send_hs_command "setDischargeLimit($limit)"
    else
        echo -e "${RED}错误: 放电限制必须是 10-40 之间的数字${NC}"
        return 1
    fi
}

# 实时监控电池状态
monitor_battery() {
    echo -e "${BLUE}🔍 开始实时监控电池状态 (按 Ctrl+C 退出)${NC}"
    echo ""
    
    while true; do
        clear
        echo -e "${BLUE}🔋 电池实时监控${NC}"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "$(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        get_battery_status
        echo ""
        echo -e "${YELLOW}按 Ctrl+C 退出监控${NC}"
        sleep 5
    done
}

# 主程序
main() {
    case "$1" in
        "status")
            get_battery_status
            ;;
        "protect")
            toggle_protection "$2"
            ;;
        "limit")
            set_charge_limit "$2"
            ;;
        "discharge")
            set_discharge_limit "$2"
            ;;
        "monitor")
            monitor_battery
            ;;
        "help"|"--help"|"-h"|"")
            show_help
            ;;
        *)
            echo -e "${RED}错误: 未知选项 '$1'${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# 运行主程序
main "$@"