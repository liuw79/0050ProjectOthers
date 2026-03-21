#!/usr/bin/env python3
"""
数据库连接测试脚本
"""

import pymssql
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv('config/.env')

# 数据库配置
DB_CONFIG = {
    'server': os.getenv('DB_HOST', '47.115.38.118'),
    'port': int(os.getenv('DB_PORT', 9024)),
    'database': os.getenv('DB_NAME', 'GW_Course'),
    'user': os.getenv('DB_USER', 'gw_reader'),
    'password': os.getenv('DB_PASSWORD', ''),
    'charset': 'utf8'
}

def test_connection():
    """测试数据库连接"""
    print("🔗 测试数据库连接...")
    print(f"📊 服务器: {DB_CONFIG['server']}:{DB_CONFIG['port']}")
    print(f"📊 数据库: {DB_CONFIG['database']}")
    print(f"👤 用户: {DB_CONFIG['user']}")
    
    try:
        # 连接数据库
        conn = pymssql.connect(**DB_CONFIG)
        print("✅ 数据库连接成功!")
        
        # 测试查询
        cursor = conn.cursor(as_dict=True)
        
        # 查询表信息
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
        tables = cursor.fetchall()
        print(f"📋 数据库中有 {len(tables)} 个表:")
        for table in tables[:10]:  # 只显示前10个
            print(f"  - {table['TABLE_NAME']}")
        
        # 测试Consumer表
        cursor.execute("SELECT COUNT(*) as count FROM Consumer")
        result = cursor.fetchone()
        print(f"👥 Consumer表中有 {result['count']} 条记录")
        
        # 测试查询前5条记录
        cursor.execute("SELECT TOP 5 ConsumerName, Phone, CreateTime FROM Consumer ORDER BY CreateTime DESC")
        records = cursor.fetchall()
        print(f"📝 最近5条Consumer记录:")
        for record in records:
            print(f"  - {record['ConsumerName']} | {record['Phone']} | {record['CreateTime']}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ 数据库连接失败: {str(e)}")
        return False

if __name__ == '__main__':
    test_connection()