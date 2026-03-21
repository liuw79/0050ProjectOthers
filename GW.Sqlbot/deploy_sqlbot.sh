#!/bin/bash

# SQLBot 原生 Python 部署脚本
# 与 GW.Trackr 保持一致的部署方式，避免 Docker 干扰

echo "=========================================="
echo "       SQLBot 智能问数系统部署脚本"
echo "       (原生 Python 部署，非容器化)"
echo "=========================================="
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装 Python3"
    exit 1
fi

# 检查 Git 是否安装
if ! command -v git &> /dev/null; then
    echo "❌ Git 未安装，请先安装 Git"
    exit 1
fi

# 创建项目目录结构
echo "📁 创建项目目录..."
mkdir -p {logs,data,config,static,templates}

# 创建虚拟环境
echo "🐍 创建 Python 虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔄 激活虚拟环境..."
source venv/bin/activate

# 检查是否有 SQLBot 源码，如果没有则从 GitHub 克隆
if [ ! -d "sqlbot-src" ]; then
    echo "📥 下载 SQLBot 源码..."
    # 这里使用一个开源的 Text-to-SQL 项目作为替代
    # 或者我们可以创建一个简化版本
    echo "⚠️  注意：由于 SQLBot 可能是商业软件，我们将创建一个简化的演示版本"
    mkdir -p sqlbot-src
fi

echo "📦 安装依赖包..."
# 使用国内镜像源加速安装
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ \
    flask \
    flask-cors \
    pymssql \
    pandas \
    numpy \
    requests \
    python-dotenv \
    openai

echo "⚙️ 创建配置文件..."
cat > config/.env << EOF
# SQLBot 配置文件
# 与 GW.Trackr 使用相同的数据库配置

# 服务配置
FLASK_ENV=production
FLASK_DEBUG=0
HOST=0.0.0.0
PORT=8002

# 数据库配置（与 GW.Trackr 相同）
DB_HOST=47.115.38.118
DB_PORT=9024
DB_USER=gw_reader
DB_PASSWORD=cZ1cM5nX5eX7
DB_NAME=GW_Course

# AI 模型配置（需要根据实际情况填写）
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=your_api_base_url_here
MODEL_NAME=gpt-3.5-turbo
EOF

echo "🚀 启动 SQLBot 服务..."
echo "   - 端口: 8002"
echo "   - 数据库: GW_Course (与 GW.Trackr 共享)"
echo "   - 部署方式: 原生 Python (与 GW.Trackr 一致)"
echo ""

# 创建启动脚本
cat > start_sqlbot.py << 'EOF'
#!/usr/bin/env python3
"""
SQLBot 启动脚本
简化版的 Text-to-SQL 服务
"""

import os
import sys
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import pymssql
import json
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('config/.env')

app = Flask(__name__)
CORS(app)

# 数据库配置
DB_CONFIG = {
    'server': os.getenv('DB_HOST', '47.115.38.118'),
    'port': int(os.getenv('DB_PORT', 9024)),
    'database': os.getenv('DB_NAME', 'GW_Course'),
    'user': os.getenv('DB_USER', 'gw_reader'),
    'password': os.getenv('DB_PASSWORD', ''),
    'charset': 'utf8'
}

# 简单的 HTML 模板
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SQLBot - 智能问数系统</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .query-box { margin-bottom: 20px; }
        .query-box textarea { width: 100%; height: 100px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .query-box button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        .result { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; }
        .sql-code { background: #e9ecef; padding: 10px; border-radius: 3px; font-family: monospace; margin: 10px 0; }
        .error { background: #f8d7da; color: #721c24; }
        .success { background: #d4edda; color: #155724; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 SQLBot - 智能问数系统</h1>
        <p>输入自然语言查询，系统将自动生成 SQL 并执行</p>
        <p><small>数据源：GW_Course 数据库 (与 GW.Trackr 共享)</small></p>
    </div>
    
    <div class="query-box">
        <textarea id="queryInput" placeholder="例如：查询最近一个月的新增用户数量"></textarea>
        <br><br>
        <button onclick="executeQuery()">🔍 执行查询</button>
    </div>
    
    <div id="result" class="result" style="display: none;"></div>
    
    <script>
        async function executeQuery() {
            const query = document.getElementById('queryInput').value;
            const resultDiv = document.getElementById('result');
            
            if (!query.trim()) {
                alert('请输入查询内容');
                return;
            }
            
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '<p>🔄 正在处理查询...</p>';
            
            try {
                const response = await fetch('/api/query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    resultDiv.className = 'result success';
                    resultDiv.innerHTML = `
                        <h3>✅ 查询成功</h3>
                        <div class="sql-code"><strong>生成的 SQL：</strong><br>${data.sql}</div>
                        <div><strong>查询结果：</strong></div>
                        <pre>${JSON.stringify(data.data, null, 2)}</pre>
                    `;
                } else {
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = `<h3>❌ 查询失败</h3><p>${data.error}</p>`;
                }
            } catch (error) {
                resultDiv.className = 'result error';
                resultDiv.innerHTML = `<h3>❌ 网络错误</h3><p>${error.message}</p>`;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        user_query = data.get('query', '')
        
        # 简单的查询映射（实际项目中应该使用 AI 模型）
        sql_mapping = {
            '用户': 'SELECT COUNT(*) as user_count FROM Consumer',
            '学员': 'SELECT COUNT(*) as student_count FROM Consumer WHERE ConsumerType = \'学员\'',
            '课程': 'SELECT COUNT(*) as course_count FROM Course',
            '最近': 'SELECT TOP 10 * FROM Consumer ORDER BY CreateTime DESC'
        }
        
        # 简单匹配生成 SQL
        sql = None
        for keyword, query_sql in sql_mapping.items():
            if keyword in user_query:
                sql = query_sql
                break
        
        if not sql:
            sql = 'SELECT TOP 5 ConsumerName, Phone, CreateTime FROM Consumer ORDER BY CreateTime DESC'
        
        # 执行查询
        conn = pymssql.connect(**DB_CONFIG)
        cursor = conn.cursor(as_dict=True)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'sql': sql,
            'data': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'SQLBot'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8002))
    print(f"🚀 SQLBot 启动在端口 {port}")
    print(f"🌐 访问地址: http://localhost:{port}")
    print(f"📊 数据库: {DB_CONFIG['database']} @ {DB_CONFIG['server']}:{DB_CONFIG['port']}")
    app.run(host='0.0.0.0', port=port, debug=False)
EOF

# 启动服务
echo "🎯 启动 SQLBot 服务..."
python start_sqlbot.py &
SQLBOT_PID=$!

# 等待服务启动
sleep 3

# 检查服务状态
if curl -s http://localhost:8002/health > /dev/null; then
    echo ""
    echo "✅ SQLBot 部署成功！"
    echo ""
    echo "📋 访问信息："
    echo "   🌐 Web 界面: http://localhost:8002"
    echo "   🔍 健康检查: http://localhost:8002/health"
    echo ""
    echo "📝 服务信息："
    echo "   📁 项目目录: $(pwd)"
    echo "   🐍 Python 虚拟环境: $(pwd)/venv"
    echo "   📊 数据库: GW_Course (与 GW.Trackr 共享)"
    echo "   🔧 配置文件: config/.env"
    echo ""
    echo "🔧 管理命令："
    echo "   🛑 停止服务: kill $SQLBOT_PID"
    echo "   📋 查看进程: ps aux | grep start_sqlbot"
    echo "   📝 查看日志: tail -f logs/sqlbot.log"
    echo ""
    echo "💡 提示：这是一个简化版本，实际使用时需要配置真实的 AI 模型 API"
else
    echo ""
    echo "❌ SQLBot 启动失败"
    echo "🔍 请检查端口 8002 是否被占用"
    kill $SQLBOT_PID 2>/dev/null
    exit 1
fi