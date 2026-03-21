#!/bin/bash

# NAS 连接测试脚本
# 用于诊断 SSH 连接问题

# 配置变量
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONNECTION_CONFIG="$SCRIPT_DIR/nas_connection.conf"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 加载连接配置
load_connection_config() {
    if [ ! -f "$CONNECTION_CONFIG" ]; then
        echo -e "${RED}❌ 连接配置文件不存在: $CONNECTION_CONFIG${NC}"
        exit 1
    fi
    
    source "$CONNECTION_CONFIG"
    
    # 验证必要的配置
    if [ -z "$NAS_HOST" ] || [ -z "$NAS_USERNAME" ] || [ -z "$NAS_PASSWORD" ] || [ -z "$NAS_SSH_PORT" ]; then
        echo -e "${RED}❌ 连接配置不完整${NC}"
        exit 1
    fi
}

# 显示横幅
show_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🔍 NAS 连接诊断工具                        ║"
    echo "║                                                              ║"
    echo "║  诊断 SSH 连接问题并提供解决建议                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# 显示连接信息
show_connection_info() {
    echo -e "${BLUE}📋 连接信息:${NC}"
    echo -e "  主机: ${YELLOW}$NAS_HOST${NC}"
    echo -e "  端口: ${YELLOW}$NAS_SSH_PORT${NC}"
    echo -e "  用户: ${YELLOW}$NAS_USERNAME${NC}"
    echo -e "  密码: ${YELLOW}[已配置]${NC}"
    echo
}

# 测试网络连通性
test_network_connectivity() {
    echo -e "${BLUE}🌐 测试网络连通性...${NC}"
    
    # Ping 测试
    echo -e "${YELLOW}  正在 ping $NAS_HOST...${NC}"
    if ping -c 3 -W 3000 "$NAS_HOST" >/dev/null 2>&1; then
        echo -e "  ${GREEN}✅ Ping 成功${NC}"
    else
        echo -e "  ${RED}❌ Ping 失败 - 网络不通或主机不存在${NC}"
        return 1
    fi
    
    # 端口测试
    echo -e "${YELLOW}  正在测试端口 $NAS_SSH_PORT...${NC}"
    if nc -z -w 5 "$NAS_HOST" "$NAS_SSH_PORT" 2>/dev/null; then
        echo -e "  ${GREEN}✅ 端口 $NAS_SSH_PORT 可达${NC}"
    else
        echo -e "  ${RED}❌ 端口 $NAS_SSH_PORT 不可达${NC}"
        echo -e "  ${YELLOW}可能原因:${NC}"
        echo -e "    - SSH 服务未启用"
        echo -e "    - 端口配置错误"
        echo -e "    - 防火墙阻止连接"
        return 1
    fi
    
    echo
    return 0
}

# 测试 SSH 服务
test_ssh_service() {
    echo -e "${BLUE}🔐 测试 SSH 服务...${NC}"
    
    # 测试 SSH 横幅
    echo -e "${YELLOW}  正在获取 SSH 横幅...${NC}"
    local ssh_banner
    ssh_banner=$(timeout 10 telnet "$NAS_HOST" "$NAS_SSH_PORT" 2>/dev/null | head -1)
    
    if [[ "$ssh_banner" == *"SSH"* ]]; then
        echo -e "  ${GREEN}✅ SSH 服务正在运行${NC}"
        echo -e "  ${CYAN}SSH 横幅: $ssh_banner${NC}"
    else
        echo -e "  ${RED}❌ SSH 服务可能未运行${NC}"
        echo -e "  ${YELLOW}请检查 NAS 的 SSH 设置${NC}"
        return 1
    fi
    
    echo
    return 0
}

# 测试 SSH 认证
test_ssh_authentication() {
    echo -e "${BLUE}🔑 测试 SSH 认证...${NC}"
    
    # 检查 sshpass
    if ! command -v sshpass &> /dev/null; then
        echo -e "  ${RED}❌ sshpass 未安装${NC}"
        echo -e "  ${YELLOW}正在安装 sshpass...${NC}"
        if command -v brew &> /dev/null; then
            brew install sshpass
        else
            echo -e "  ${RED}❌ 无法安装 sshpass，请手动安装${NC}"
            return 1
        fi
    fi
    
    echo -e "  ${GREEN}✅ sshpass 已安装${NC}"
    
    # 测试认证（详细模式）
    echo -e "${YELLOW}  正在测试用户名和密码...${NC}"
    
    local ssh_result
    ssh_result=$(sshpass -p "$NAS_PASSWORD" ssh -p "$NAS_SSH_PORT" -o ConnectTimeout=10 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -v "$NAS_USERNAME@$NAS_HOST" "echo 'SSH认证成功'" 2>&1)
    local ssh_exit_code=$?
    
    if [ $ssh_exit_code -eq 0 ]; then
        echo -e "  ${GREEN}✅ SSH 认证成功${NC}"
        echo -e "  ${GREEN}✅ 可以执行远程命令${NC}"
        return 0
    else
        echo -e "  ${RED}❌ SSH 认证失败${NC}"
        echo -e "  ${YELLOW}错误详情:${NC}"
        echo "$ssh_result" | grep -E "(Permission denied|Authentication failed|Connection refused|No route to host)" | head -3
        
        # 分析错误原因
        if echo "$ssh_result" | grep -q "Permission denied"; then
            echo -e "  ${YELLOW}可能原因: 用户名或密码错误${NC}"
        elif echo "$ssh_result" | grep -q "Connection refused"; then
            echo -e "  ${YELLOW}可能原因: SSH 服务未启用或端口错误${NC}"
        elif echo "$ssh_result" | grep -q "No route to host"; then
            echo -e "  ${YELLOW}可能原因: 网络不通或主机地址错误${NC}"
        fi
        
        return 1
    fi
}

# 测试远程命令执行
test_remote_commands() {
    echo -e "${BLUE}⚙️ 测试远程命令执行...${NC}"
    
    # 测试基本命令
    echo -e "${YELLOW}  测试基本命令 (whoami)...${NC}"
    local whoami_result
    whoami_result=$(sshpass -p "$NAS_PASSWORD" ssh -p "$NAS_SSH_PORT" -o ConnectTimeout=10 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$NAS_USERNAME@$NAS_HOST" "whoami" 2>/dev/null)
    
    if [ -n "$whoami_result" ]; then
        echo -e "  ${GREEN}✅ 当前用户: $whoami_result${NC}"
    else
        echo -e "  ${RED}❌ 无法执行基本命令${NC}"
        return 1
    fi
    
    # 测试文件系统访问
    echo -e "${YELLOW}  测试文件系统访问...${NC}"
    local ls_result
    ls_result=$(sshpass -p "$NAS_PASSWORD" ssh -p "$NAS_SSH_PORT" -o ConnectTimeout=10 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$NAS_USERNAME@$NAS_HOST" "ls -la /volume1 2>/dev/null | head -5" 2>/dev/null)
    
    if [ -n "$ls_result" ]; then
        echo -e "  ${GREEN}✅ 可以访问 /volume1${NC}"
        echo -e "  ${CYAN}目录内容预览:${NC}"
        echo "$ls_result" | while read -r line; do
            echo "    $line"
        done
    else
        echo -e "  ${YELLOW}⚠️ 无法访问 /volume1，可能权限不足${NC}"
    fi
    
    # 测试磁盘信息
    echo -e "${YELLOW}  测试磁盘信息获取...${NC}"
    local df_result
    df_result=$(sshpass -p "$NAS_PASSWORD" ssh -p "$NAS_SSH_PORT" -o ConnectTimeout=10 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$NAS_USERNAME@$NAS_HOST" "df -h /volume1" 2>/dev/null)
    
    if [ -n "$df_result" ]; then
        echo -e "  ${GREEN}✅ 磁盘信息获取成功${NC}"
        echo -e "  ${CYAN}磁盘使用情况:${NC}"
        echo "$df_result" | while read -r line; do
            echo "    $line"
        done
    else
        echo -e "  ${YELLOW}⚠️ 无法获取磁盘信息${NC}"
    fi
    
    echo
    return 0
}

# 提供解决建议
show_troubleshooting_tips() {
    echo -e "${PURPLE}🛠️ 故障排除建议:${NC}"
    echo
    echo -e "${YELLOW}1. 检查 NAS 设置:${NC}"
    echo "   - 登录 NAS 管理界面"
    echo "   - 进入 控制面板 > 终端机和 SNMP"
    echo "   - 确保 '启用 SSH 服务' 已勾选"
    echo "   - 检查 SSH 端口设置 (默认 22，您配置的是 $NAS_SSH_PORT)"
    echo
    echo -e "${YELLOW}2. 检查用户权限:${NC}"
    echo "   - 确保用户 '$NAS_USERNAME' 存在"
    echo "   - 确保用户有 SSH 登录权限"
    echo "   - 检查用户密码是否正确"
    echo
    echo -e "${YELLOW}3. 检查网络设置:${NC}"
    echo "   - 确保 NAS 和本机在同一网络"
    echo "   - 检查防火墙设置"
    echo "   - 尝试从其他设备连接测试"
    echo
    echo -e "${YELLOW}4. 手动测试命令:${NC}"
    echo "   ssh -p $NAS_SSH_PORT $NAS_USERNAME@$NAS_HOST"
    echo
}

# 主函数
main() {
    # 加载配置
    load_connection_config
    
    # 显示横幅
    show_banner
    
    # 显示连接信息
    show_connection_info
    
    local all_tests_passed=true
    
    # 执行测试
    if ! test_network_connectivity; then
        all_tests_passed=false
    fi
    
    if ! test_ssh_service; then
        all_tests_passed=false
    fi
    
    if ! test_ssh_authentication; then
        all_tests_passed=false
    fi
    
    if $all_tests_passed; then
        test_remote_commands
        echo -e "${GREEN}🎉 所有测试通过！NAS 连接正常${NC}"
        echo -e "${GREEN}您现在可以使用远程清理工具了${NC}"
    else
        echo -e "${RED}❌ 连接测试失败${NC}"
        show_troubleshooting_tips
    fi
}

# 检查是否直接运行脚本
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi