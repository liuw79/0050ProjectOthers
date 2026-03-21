#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

# 基础配置
app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'sqlbot-production-key'
SERVICE_PORT = 8004
SERVICE_HOST = '0.0.0.0'

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/opt/sqlbot/logs/sqlbot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# HTML 模板
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SQLBot - 智能数据查询系统</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f7fa; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { color: #2c3e50; font-size: 2.5em; margin-bottom: 10px; }
        .header p { color: #7f8c8d; font-size: 1.2em; }
        .status { background: #27ae60; color: white; padding: 10px 20px; border-radius: 5px; display: inline-block; margin: 20px 0; }
        .info { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 SQLBot</h1>
            <p>智能数据查询系统 - 生产环境</p>
            <div class="status">✅ 服务运行正常</div>
        </div>
        
        <div class="info">
            <h3>🚀 部署信息</h3>
            <p><strong>服务器:</strong> op.gaowei.com</p>
            <p><strong>端口:</strong> 8004</p>
            <p><strong>环境:</strong> 生产环境</p>
            <p><strong>部署时间:</strong> {{ timestamp }}</p>
        </div>
        
        <div class="info">
            <h3>📊 API 接口</h3>
            <p><strong>健康检查:</strong> <a href="/health">/health</a></p>
            <p><strong>查询接口:</strong> POST /api/query</p>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/health')
def health():
    return jsonify({
        'service': 'SQLBot',
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'environment': 'production',
        'server': 'op.gaowei.com'
    })

@app.route('/api/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        query_text = data.get('query', '')
        
        # 模拟查询响应
        return jsonify({
            'status': 'success',
            'query': query_text,
            'result': '查询功能正在开发中...',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    logger.info(f"SQLBot 启动中... 端口: {SERVICE_PORT}")
    app.run(host=SERVICE_HOST, port=SERVICE_PORT, debug=False)