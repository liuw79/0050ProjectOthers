#!/bin/bash

echo "🌐 测试 DataEase SQLBot 访问状态"
echo "==============================="

# 测试8080端口
echo "测试 http://localhost:8080 ..."

# 使用curl测试
if command -v curl &> /dev/null; then
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080 --connect-timeout 5)
    case $RESPONSE in
        200|302|404)
            echo "✅ 服务正在运行 (HTTP $RESPONSE)"
            echo "🌐 访问地址: http://localhost:8080"
            ;;
        000)
            echo "❌ 连接失败 - 服务可能未启动"
            ;;
        *)
            echo "⚠️  服务响应异常 (HTTP $RESPONSE)"
            ;;
    esac
else
    echo "curl命令不可用，使用其他方法测试..."
fi

# 使用nc测试端口
if command -v nc &> /dev/null; then
    if nc -z localhost 8080 2>/dev/null; then
        echo "✅ 8080端口正在监听"
    else
        echo "❌ 8080端口未监听"
    fi
fi

# 检查进程
echo ""
echo "检查相关进程..."
ps aux | grep -E "(docker|sqlbot|dataease)" | grep -v grep || echo "未找到相关进程"

echo ""
echo "💡 如果服务未运行，请执行："
echo "   chmod +x quick_fix.sh && ./quick_fix.sh"