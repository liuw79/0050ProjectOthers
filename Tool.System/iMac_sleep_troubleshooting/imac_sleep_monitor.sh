#!/bin/bash

# iMac 睡眠状态监控与分析工具
# 版本: 2.0
# 更新日志:
# v2.0 - 2023-10-27: 增加详细的函数注释、错误处理和代码模块化。
#                   - 引入常量和更安全的路径处理。
#                   - 优化日志格式，增加时间戳和进程ID。
#                   - 改进HTML报告生成逻辑，使其更健壮。
# v1.0 - 初始版本。

# --- 全局常量与配置 ---
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
readonly LOG_FILE="$SCRIPT_DIR/imac_sleep_log.txt"
readonly REPORT_TEMPLATE="$SCRIPT_DIR/report_template.html"
readonly REPORT_FILE="$SCRIPT_DIR/sleep_report.html"

# --- 函数定义 ---

# 函数：记录日志条目
# $1: 日志级别 (e.g., INFO, WARN, ERROR)
# $2: 日志消息
log_message() {
    local level="$1"
    local message="$2"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
}

# 函数：重启蓝牙服务
restart_bluetooth_service() {
    log_message "INFO" "检测到 bluetoothd 阻止睡眠，尝试重启蓝牙服务..."
    if launchctl kickstart -k system/com.apple.bluetoothd; then
        log_message "INFO" "蓝牙服务重启成功。"
    else
        log_message "ERROR" "蓝牙服务重启失败。请检查SIP状态或系统日志。"
    fi
}

# 函数：记录当前阻止睡眠的进程
log_sleep_blockers() {
    # 确保日志文件存在，如果不存在则创建
    touch "$LOG_FILE" || { echo "致命错误: 无法创建日志文件 $LOG_FILE"; exit 1; }

    local blockers
    blockers=$(pmset -g assertions | grep 'PreventUserIdleSystemSleep' | sed -n 's/.*pid [0-9]*(\([^)]*\)).*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')

    if [ -n "$blockers" ]; then
        log_message "WARN" "睡眠被阻止，来源: $blockers"
        
        # 检查并处理已知的睡眠阻止者
        if echo ",$blockers," | grep -q ",bluetoothd,"; then
            restart_bluetooth_service
        fi
    else
        log_message "INFO" "未发现活动的 'PreventUserIdleSystemSleep' 断言。系统可以正常睡眠。"
    fi
}

# 函数：生成HTML报告
generate_html_report() {
    if [ ! -f "$REPORT_TEMPLATE" ]; then
        log_message "ERROR" "HTML模板文件 '$REPORT_TEMPLATE' 不存在，无法生成报告。"
        return 1
    fi

    # 创建一个临时目录来存放所有临时文件，并确保在脚本退出时清理
    local temp_dir
    temp_dir=$(mktemp -d)
    trap 'rm -rf "$temp_dir"' EXIT

    # 准备统计数据
    local stats_file="$temp_dir/stats.txt"
    # 使用更健壮的awk脚本来处理可能包含空格的进程名
    grep '来源:' "$LOG_FILE" | \
    awk -F '来源: ' '{print $2}' | \
    tr ',' '\n' | \
    sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | \
    grep -v '^$' | \
    sort | uniq -c | sort -rn | \
    awk '{
        name = "";
        for (i=2; i<=NF; i++) name = name (i>2 ? " " : "") $i;
        printf "<tr><td>%s</td><td>%d</td></tr>\n", name, $1;
    }' > "$stats_file"

    if [ ! -s "$stats_file" ]; then
        echo '<tr class="placeholder"><td colspan="2">恭喜！在日志记录期间未发现任何睡眠阻止者。</td></tr>' > "$stats_file"
    fi

    # 准备日志摘要
    local log_summary_file="$temp_dir/log_summary.txt"
    # 增加HTML转义以防止注入
    tail -n 50 "$LOG_FILE" | sed 's/&/&amp;/g; s/</&lt;/g; s/>/&gt;/g; s/"/&quot;/g' > "$log_summary_file"

    # 使用perl生成最终报告
    perl -e '
        use strict;
        use warnings;
        
        # 读取模板
        open(my $template, "<", $ARGV[0]) or die "无法打开模板文件: $!";
        my $html = do { local $/; <$template> };
        close($template);
        
        # 读取统计数据
        open(my $stats, "<", $ARGV[1]) or die "无法打开统计数据文件: $!";
        my $stats_data = do { local $/; <$stats> };
        close($stats);
        
        # 读取日志数据
        open(my $log, "<", $ARGV[2]) or die "无法打开日志摘要文件: $!";
        my $log_data = do { local $/; <$log> };
        close($log);
        
        # 替换占位符
        my $time = `date "+%Y-%m-%d %H:%M:%S"`;
        chomp($time);
        $html =~ s/<!-- STATS_TABLE_ROWS -->/$stats_data/s;
        $html =~ s/<!-- RAW_LOG_SUMMARY -->/$log_data/s;
        $html =~ s/<!-- GENERATION_TIME -->/$time/g;
        
        # 输出结果
        open(my $out, ">", $ARGV[3]) or die "无法写入报告文件: $!";
        print $out $html;
        close($out);
    ' "$REPORT_TEMPLATE" "$stats_file" "$log_summary_file" "$REPORT_FILE"

    log_message "INFO" "HTML报告已成功生成: $REPORT_FILE"
}

# 函数：在终端显示统计报告
show_summary() {
    if [ ! -f "$LOG_FILE" ]; then
        echo "错误: 日志文件 '$LOG_FILE' 不存在。请先运行脚本进行记录。"
        return 1
    fi

    echo "--- iMac 睡眠阻止者统计报告 ---"
    local first_log_entry
    first_log_entry=$(head -n 1 "$LOG_FILE" | cut -d' ' -f1,2)
    echo "(统计自: $first_log_entry)"
    echo
    
    # 使用与HTML报告相同的健壮逻辑
    grep '来源:' "$LOG_FILE" | \
    awk -F '来源: ' '{print $2}' | \
    tr ',' '\n' | \
    sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | \
    grep -v '^$' | \
    sort | uniq -c | sort -rn | \
    awk '{printf "  - %-20s: %d 次\n", substr($0, 9), $1}'

    echo
    echo "--- 日志路径 ---"
    echo "$LOG_FILE"
}

# 函数：显示帮助信息
show_help() {
    cat << EOF
用法: $0 [选项]

iMac 睡眠状态监控与分析工具。

选项:
  (无)              记录当前睡眠阻止者到日志并生成HTML报告。
  -s, --summary     在终端显示统计报告。
  -r, --report      仅生成并打开HTML格式的图形化报告。
  -h, --help        显示此帮助信息。

报告和日志将保存在脚本所在目录:
  - 日志: $LOG_FILE
  - 报告: $REPORT_FILE
EOF
}

# --- 主逻辑 ---
main() {
    case "$1" in
        -s|--summary)
            show_summary
            ;;
        -r|--report)
            generate_html_report
            open "$REPORT_FILE"
            ;;
        -h|--help)
            show_help
            ;;
        "")
            log_sleep_blockers
            generate_html_report
            ;;
        *)
            echo "错误: 未知选项 '$1'"
            show_help
            exit 1
            ;;
    esac
}

# --- 脚本执行入口 ---
main "$@"