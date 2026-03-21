#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地SQLBot服务启动脚本
不依赖Docker，直接使用Python运行
"""

import os
import sys
from flask import Flask, render_template, request, jsonify
import psycopg2
from openai import OpenAI
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 从环境变量或配置文件读取配置
def load_config():
    config = {}
    
    # 数据库配置
    config['DB_HOST'] = os.getenv('DB_HOST', '47.115.38.118')
    config['DB_PORT'] = int(os.getenv('DB_PORT', '9024'))
    config['DB_USER'] = os.getenv('DB_USER', 'gw_reader')
    config['DB_PASSWORD'] = os.getenv('DB_PASSWORD', 'cZ1cM5nX5eX7')
    config['DB_NAME'] = os.getenv('DB_NAME', 'GW_Course')
    
    # AI模型配置
    config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'sk-22XL5TLeclRZyzj3lVAY0UYLy1S1NJJO45cKWTzWljMQDK8R')
    config['OPENAI_BASE_URL'] = os.getenv('OPENAI_BASE_URL', 'https://api.moonshot.cn/v1')
    config['MODEL_NAME'] = os.getenv('MODEL_NAME', 'kimi-k2-0711-preview')
    
    return config

# 全局配置
CONFIG = load_config()

# 初始化AI客户端
try:
    ai_client = OpenAI(
        api_key=CONFIG['OPENAI_API_KEY'],
        base_url=CONFIG['OPENAI_BASE_URL']
    )
    logger.info("AI客户端初始化成功")
except Exception as e:
    logger.error(f"AI客户端初始化失败: {e}")
    ai_client = None

# 数据库连接
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=CONFIG['DB_HOST'],
            port=CONFIG['DB_PORT'],
            user=CONFIG['DB_USER'],
            password=CONFIG['DB_PASSWORD'],
            database=CONFIG['DB_NAME']
        )
        return conn
    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        return None

# 获取数据库表结构
def get_database_schema():
    conn = get_db_connection()
    if not conn:
        return "无法连接到数据库"
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name, column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema = 'public' 
            ORDER BY table_name, ordinal_position
        """)
        
        schema_info = {}
        for row in cursor.fetchall():
            table_name, column_name, data_type = row
            if table_name not in schema_info:
                schema_info[table_name] = []
            schema_info[table_name].append(f"{column_name} ({data_type})")
        
        schema_text = "数据库表结构:\n"
        for table, columns in schema_info.items():
            schema_text += f"\n表 {table}:\n"
            for column in columns:
                schema_text += f"  - {column}\n"
        
        return schema_text
    except Exception as e:
        logger.error(f"获取数据库结构失败: {e}")
        return "获取数据库结构失败"
    finally:
        conn.close()

# AI生成SQL查询
def generate_sql_with_ai(question):
    if not ai_client:
        return None, "AI服务未配置"
    
    try:
        schema = get_database_schema()
        
        prompt = f"""
你是一个SQL查询专家。根据用户的自然语言问题，生成对应的PostgreSQL查询语句。

数据库信息：
{schema}

用户问题：{question}

请生成准确的SQL查询语句，只返回SQL代码，不要包含其他解释。
"""
        
        response = ai_client.chat.completions.create(
            model=CONFIG['MODEL_NAME'],
            messages=[
                {"role": "system", "content": "你是一个专业的SQL查询生成助手。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.1
        )
        
        sql_query = response.choices[0].message.content.strip()
        
        # 清理SQL查询（移除markdown标记等）
        if sql_query.startswith('```sql'):
            sql_query = sql_query[6:]
        if sql_query.endswith('```'):
            sql_query = sql_query[:-3]
        
        return sql_query.strip(), None
        
    except Exception as e:
        logger.error(f"AI生成SQL失败: {e}")
        return None, f"AI生成失败: {str(e)}"

# 执行SQL查询
def execute_sql_query(sql_query):
    conn = get_db_connection()
    if not conn:
        return None, "数据库连接失败"
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        
        if sql_query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return {'columns': columns, 'data': results}, None
        else:
            conn.commit()
            return {'message': '查询执行成功'}, None
            
    except Exception as e:
        logger.error(f"SQL执行失败: {e}")
        return None, f"SQL执行失败: {str(e)}"
    finally:
        conn.close()

# 路由定义
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def api_query():
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': '请输入问题'}), 400
        
        # 生成SQL
        sql_query, error = generate_sql_with_ai(question)
        if error:
            return jsonify({'error': error}), 500
        
        # 执行SQL
        results, error = execute_sql_query(sql_query)
        if error:
            return jsonify({'error': error, 'sql': sql_query}), 500
        
        return jsonify({
            'sql': sql_query,
            'results': results,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"API查询失败: {e}")
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

@app.route('/api/health')
def health_check():
    db_status = "正常" if get_db_connection() else "连接失败"
    ai_status = "正常" if ai_client else "未配置"
    
    return jsonify({
        'status': 'running',
        'database': db_status,
        'ai_model': ai_status,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 启动本地SQLBot服务...")
    print(f"📊 数据库: {CONFIG['DB_HOST']}:{CONFIG['DB_PORT']}/{CONFIG['DB_NAME']}")
    print(f"🤖 AI模型: {CONFIG['MODEL_NAME']}")
    print(f"🌐 访问地址: http://localhost:8080")
    print("=" * 50)
    
    # 测试数据库连接
    if get_db_connection():
        print("✅ 数据库连接正常")
    else:
        print("❌ 数据库连接失败")
    
    # 测试AI服务
    if ai_client:
        print("✅ AI服务配置正常")
    else:
        print("❌ AI服务配置失败")
    
    print("=" * 50)
    
    # 启动Flask应用
    app.run(host='0.0.0.0', port=8080, debug=False)