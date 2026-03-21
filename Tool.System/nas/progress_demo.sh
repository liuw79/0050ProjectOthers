#!/bin/bash

# 进度条演示脚本
# 展示新增的进度条功能

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# 进度条相关变量
PROGRESS_BAR_WIDTH=50
PROGRESS_CHAR="█"
EMPTY_CHAR="░"

# 进度条函数
show_progress() {
    local current=$1
    local total=$2
    local message="$3"
    local percent=$((current * 100 / total))
    local filled=$((current * PROGRESS_BAR_WIDTH / total))
    local empty=$((PROGRESS_BAR_WIDTH - filled))
    
    printf "\r${CYAN}%s${NC} [" "$message"
    printf "%*s" $filled | tr ' ' "$PROGRESS_CHAR"
    printf "%*s" $empty | tr ' ' "$EMPTY_CHAR"
    printf "] %d%% (%d/%d)" $percent $current $total
}

# 完成进度条显示
complete_progress() {
    local message="$1"
    printf "\r${GREEN}%s${NC} [" "$message"
    printf "%*s" $PROGRESS_BAR_WIDTH | tr ' ' "$PROGRESS_CHAR"
    printf "] 100%%\n"
}

# 显示标题
show_header() {
    clear
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                  📊 NAS 清理脚本进度条演示                   ║"
    echo "║                                                              ║"
    echo "║  展示新增的进度条功能 • 实时进度显示 • 美观界面             ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}\n"
}

# 演示基本进度条
demo_basic_progress() {
    echo -e "${BLUE}🔍 演示1: 基本进度条${NC}"
    echo "模拟文件扫描过程..."
    
    for i in {1..10}; do
        show_progress $i 10 "扫描文件"
        sleep 0.3
    done
    
    complete_progress "扫描完成"
    echo ""
}

# 演示多步骤进度条
demo_multi_step_progress() {
    echo -e "${BLUE}🔍 演示2: 多步骤进度条${NC}"
    echo "模拟完整的清理过程..."
    
    # 步骤1: 分析磁盘
    echo -e "\n${YELLOW}📊 清理进度:${NC}"
    show_progress 1 5 "分析磁盘使用情况"
    sleep 1
    
    # 步骤2: 查找大文件
    show_progress 2 5 "查找大文件"
    sleep 1
    
    # 步骤3: 查找重复文件
    show_progress 3 5 "查找重复文件"
    sleep 1.5
    
    # 步骤4: 查找临时文件
    show_progress 4 5 "查找临时文件"
    sleep 0.8
    
    # 步骤5: 生成报告
    show_progress 5 5 "生成清理报告"
    sleep 0.5
    
    complete_progress "清理分析完成"
    echo ""
}

# 演示不同类型的进度条
demo_different_types() {
    echo -e "${BLUE}🔍 演示3: 不同类型的操作${NC}"
    
    # 快速操作
    echo -e "\n${CYAN}⚡ 快速操作:${NC}"
    for i in {1..5}; do
        show_progress $i 5 "快速扫描"
        sleep 0.1
    done
    complete_progress "快速扫描完成"
    
    # 中等速度操作
    echo -e "\n${YELLOW}🔄 中等速度操作:${NC}"
    for i in {1..8}; do
        show_progress $i 8 "文件分析"
        sleep 0.4
    done
    complete_progress "文件分析完成"
    
    # 慢速操作
    echo -e "\n${RED}🐌 慢速操作 (模拟大文件处理):${NC}"
    for i in {1..6}; do
        show_progress $i 6 "处理大文件"
        sleep 0.8
    done
    complete_progress "大文件处理完成"
    echo ""
}

# 演示实际使用场景
demo_real_scenario() {
    echo -e "${BLUE}🔍 演示4: 实际使用场景${NC}"
    echo "模拟真实的NAS清理过程..."
    
    # 模拟扫描临时文件
    echo -e "\n${YELLOW}🗑️  临时文件清理:${NC}"
    
    local temp_patterns=("*.tmp" "*.cache" "*.log" "*.bak" "*~" ".DS_Store")
    local total=${#temp_patterns[@]}
    
    for i in "${!temp_patterns[@]}"; do
        local current=$((i + 1))
        show_progress $current $total "扫描 ${temp_patterns[$i]} 文件"
        sleep 0.5
    done
    
    complete_progress "临时文件扫描完成"
    echo -e "${GREEN}✅ 找到 127 个临时文件${NC}"
    
    # 模拟删除过程
    echo -e "\n${RED}🗑️  删除进度:${NC}"
    for i in {1..127}; do
        if (( i % 10 == 0 )) || (( i == 127 )); then
            show_progress $i 127 "删除临时文件"
        fi
        sleep 0.02
    done
    
    complete_progress "删除完成"
    echo -e "${GREEN}✅ 成功删除 127 个临时文件，释放空间 2.3GB${NC}"
    echo ""
}

# 显示功能说明
show_features() {
    echo -e "${PURPLE}📋 新增功能特性:${NC}"
    echo -e "${GREEN}✅${NC} 实时进度显示 - 清楚了解操作进度"
    echo -e "${GREEN}✅${NC} 美观的进度条 - 使用Unicode字符显示"
    echo -e "${GREEN}✅${NC} 彩色状态提示 - 不同颜色表示不同状态"
    echo -e "${GREEN}✅${NC} 详细统计信息 - 显示处理的文件数量和大小"
    echo -e "${GREEN}✅${NC} 多步骤进度 - 复杂操作分步显示进度"
    echo -e "${GREEN}✅${NC} 完成状态确认 - 明确显示操作完成状态"
    echo ""
}

# 主函数
main() {
    show_header
    
    echo -e "${CYAN}🎯 这个演示将展示NAS清理脚本中新增的进度条功能${NC}"
    echo -e "${YELLOW}⏱️  整个演示大约需要 30 秒${NC}"
    echo ""
    
    read -p "按 Enter 开始演示..."
    
    demo_basic_progress
    sleep 1
    
    demo_multi_step_progress
    sleep 1
    
    demo_different_types
    sleep 1
    
    demo_real_scenario
    sleep 1
    
    show_features
    
    echo -e "${GREEN}🎉 演示完成！${NC}"
    echo -e "${CYAN}💡 提示: 现在您可以在实际的NAS清理脚本中看到这些进度条功能${NC}"
    echo -e "${YELLOW}📝 使用方法:${NC}"
    echo "   • 运行 ./interactive_nas_cleanup.sh 体验交互式清理"
    echo "   • 运行 ./nas_cleanup.sh 体验自动化清理"
    echo ""
}

# 信号处理
trap 'echo -e "\n${YELLOW}演示被中断${NC}"; exit 1' INT TERM

# 运行主函数
main "$@"