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
from openai import OpenAI

# 加载环境变量
load_dotenv('config/.env')

def generate_sql_with_ai(user_query):
    """使用AI模型生成SQL查询"""
    try:
        # 数据库表结构信息
        schema_info = """
        数据库表结构：
        1. Consumer表（用户/学员表）：
           - ConsumerID: 用户ID
           - ConsumerName: 用户姓名
           - Phone: 电话号码
           - ConsumerType: 用户类型（学员等）
           - CreateTime: 创建时间
           
        2. Course表（课程表）：
           - CourseID: 课程ID
           - CourseName: 课程名称
           - CreateTime: 创建时间
        """
        
        prompt = f"""
        你是一个SQL查询生成专家。根据用户的自然语言查询，生成对应的SQL语句。

        {schema_info}

        用户查询：{user_query}

        请生成一个SQL查询语句，要求：
        1. 只返回SQL语句，不要其他解释
        2. 使用标准的SQL Server语法
        3. 如果查询涉及数量统计，使用COUNT()
        4. 如果查询最近的记录，使用TOP和ORDER BY
        5. 确保SQL语句安全，避免SQL注入

        SQL:
        """
        
        response = AI_CLIENT.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": "你是一个专业的SQL查询生成助手，只返回SQL语句，不要其他内容。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.1
        )
        
        sql = response.choices[0].message.content.strip()
        # 清理SQL语句，移除可能的markdown格式
        if sql.startswith('```sql'):
            sql = sql[6:]
        if sql.startswith('```'):
            sql = sql[3:]
        if sql.endswith('```'):
            sql = sql[:-3]
        
        return sql.strip()
        
    except Exception as e:
        print(f"❌ AI生成SQL失败: {str(e)}")
        # 如果AI失败，回退到简单映射
        sql_mapping = {
            '用户': 'SELECT COUNT(*) as user_count FROM Consumer',
            '学员': 'SELECT COUNT(*) as student_count FROM Consumer WHERE ConsumerType = \'学员\'',
            '课程': 'SELECT COUNT(*) as course_count FROM Course',
            '最近': 'SELECT TOP 10 ConsumerName, Phone, CreateTime FROM Consumer ORDER BY CreateTime DESC'
        }
        
        for keyword, query_sql in sql_mapping.items():
            if keyword in user_query:
                return query_sql
        
        return 'SELECT TOP 5 ConsumerName, Phone, CreateTime FROM Consumer ORDER BY CreateTime DESC'

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

# AI模型配置
AI_CLIENT = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_URL')
)
AI_MODEL = os.getenv('OPENAI_MODEL', 'kimi-k2-0711-preview')

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
        
        print(f"🔍 收到查询: {user_query}")
        
        # 简单的查询映射（实际项目中应该使用 AI 模型）
        sql_mapping = {
            '用户': 'SELECT COUNT(*) as user_count FROM Consumer',
            '学员': 'SELECT COUNT(*) as student_count FROM Consumer WHERE ConsumerType = \'学员\'',
            '课程': 'SELECT COUNT(*) as course_count FROM Course',
            '最近': 'SELECT TOP 10 ConsumerName, Phone, CreateTime FROM Consumer ORDER BY CreateTime DESC'
        }
        
        # 简单匹配生成 SQL
        sql = None
        for keyword, query_sql in sql_mapping.items():
            if keyword in user_query:
                sql = query_sql
                break
        
        if not sql:
            sql = 'SELECT TOP 5 ConsumerName, Phone, CreateTime FROM Consumer ORDER BY CreateTime DESC'
        
        print(f"📝 生成SQL: {sql}")
        
        # 执行查询
        print(f"🔗 连接数据库: {DB_CONFIG['server']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
        conn = pymssql.connect(**DB_CONFIG)
        cursor = conn.cursor(as_dict=True)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        print(f"✅ 查询成功，返回 {len(results)} 条记录")
        
        return jsonify({
            'success': True,
            'sql': sql,
            'data': results,
            'count': len(results)
        })
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ 查询失败: {error_msg}")
        return jsonify({
            'success': False,
            'error': error_msg,
            'sql': sql if 'sql' in locals() else None
        }), 500

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'SQLBot'})

def test_db_connection():
    """测试数据库连接"""
    try:
        conn = pymssql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        return True, "数据库连接成功"
    except Exception as e:
        return False, f"数据库连接失败: {str(e)}"

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8004))
    
    # 测试数据库连接
    db_ok, db_msg = test_db_connection()
    print(f"📊 数据库测试: {db_msg}")
    
    print(f"🚀 SQLBot 启动在端口 {port}")
    print(f"🌐 访问地址: http://localhost:{port}")
    print(f"📊 数据库: {DB_CONFIG['database']} @ {DB_CONFIG['server']}:{DB_CONFIG['port']}")
    
    if not db_ok:
        print("⚠️  警告: 数据库连接失败，服务可能无法正常工作")
    
    app.run(host='0.0.0.0', port=port, debug=True)
