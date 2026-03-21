#!/bin/bash

# DataEase SQLBot AI模型配置脚本
# 配置Kimi K2 AI模型

echo "=== DataEase SQLBot AI模型配置 ==="

# 检查容器状态
echo "1. 检查DataEase SQLBot容器状态..."
docker ps | grep dataease/sqlbot

# 重启容器以应用新的环境变量配置
echo "2. 重启容器以应用AI模型配置..."
docker restart dataease-sqlbot 2>/dev/null || echo "容器可能使用不同名称"

# 等待容器启动
echo "3. 等待容器启动..."
sleep 10

# 检查容器日志
echo "4. 检查容器启动日志..."
docker logs --tail 20 dataease-sqlbot 2>/dev/null || docker logs --tail 20 $(docker ps | grep sqlbot | awk '{print $1}') 2>/dev/null

# 验证AI模型配置
echo "5. 验证AI模型配置..."
echo "配置的AI模型信息："
echo "- API Key: $(grep OPENAI_API_KEY config/.env | head -1)"
echo "- Base URL: $(grep OPENAI_BASE_URL config/.env | head -1)"
echo "- Model Name: $(grep MODEL_NAME config/.env | head -1)"

echo ""
echo "=== 配置完成 ==="
echo "请访问 http://localhost:8080 测试AI智能问数功能"
echo ""
echo "测试建议："
echo "1. 在问数界面输入自然语言查询，如：'显示所有课程信息'"
echo "2. 检查AI是否能正确生成SQL查询"
echo "3. 验证查询结果是否正确"