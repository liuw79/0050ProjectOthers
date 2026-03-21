#!/bin/bash

# SQLBot 远程服务器部署脚本
# 适用于 Ubuntu/CentOS 服务器

set -e

# 配置变量
PROJECT_NAME="sqlbot"
PROJECT_DIR="/opt/sqlbot"
SERVICE_USER="sqlbot"
SERVICE_PORT="8004"
PYTHON_VERSION="3.8"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否为 root 用户
check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "此脚本需要 root 权限运行"
        log_info "请使用: sudo $0"
        exit 1
    fi
}

# 检测操作系统
detect_os() {
    if [[ -f /etc/redhat-release ]]; then
        OS="centos"
        PKG_MANAGER="yum"
    elif [[ -f /etc/lsb-release ]] || [[ -f /etc/debian_version ]]; then
        OS="ubuntu"
        PKG_MANAGER="apt"
    else
        log_error "不支持的操作系统"
        exit 1
    fi
    log_info "检测到操作系统: $OS"
}

# 安装系统依赖
install_dependencies() {
    log_info "安装系统依赖..."
    
    if [[ $OS == "ubuntu" ]]; then
        apt update
        apt install -y python3 python3-pip python3-venv git nginx supervisor curl
        apt install -y python3-dev build-essential libssl-dev libffi-dev
        # 安装 SQL Server 驱动依赖
        apt install -y unixodbc-dev freetds-dev freetds-bin
    elif [[ $OS == "centos" ]]; then
        yum update -y
        yum install -y python3 python3-pip git nginx supervisor curl
        yum groupinstall -y "Development Tools"
        yum install -y openssl-devel libffi-devel
        # 安装 SQL Server 驱动依赖
        yum install -y unixODBC-devel freetds-devel
    fi
}

# 创建服务用户
create_service_user() {
    log_info "创建服务用户: $SERVICE_USER"
    
    if ! id "$SERVICE_USER" &>/dev/null; then
        useradd -r -s /bin/false -d $PROJECT_DIR $SERVICE_USER
        log_info "用户 $SERVICE_USER 创建成功"
    else
        log_warn "用户 $SERVICE_USER 已存在"
    fi
}

# 创建项目目录
create_project_structure() {
    log_info "创建项目目录结构..."
    
    mkdir -p $PROJECT_DIR/{config,logs,data,static,templates,backup}
    mkdir -p $PROJECT_DIR/data/{sqlbot,postgresql}
    mkdir -p $PROJECT_DIR/data/sqlbot/{excel,images,logs}
    
    # 设置目录权限
    chown -R $SERVICE_USER:$SERVICE_USER $PROJECT_DIR
    chmod -R 755 $PROJECT_DIR
    chmod -R 775 $PROJECT_DIR/{logs,data,backup}
}

# 部署应用代码
deploy_application() {
    log_info "部署应用代码..."
    
    # 创建 Python 虚拟环境
    cd $PROJECT_DIR
    sudo -u $SERVICE_USER python3 -m venv venv
    
    # 激活虚拟环境并安装依赖
    sudo -u $SERVICE_USER bash -c "
        source venv/bin/activate
        pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --upgrade pip
        pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ \
            flask flask-cors pymssql pandas numpy requests python-dotenv openai
    "
    
    log_info "Python 依赖安装完成"
}

# 创建配置文件
create_config_files() {
    log_info "创建配置文件..."
    
    # 创建 .env 配置文件
    cat > $PROJECT_DIR/config/.env << EOF
# SQLBot 生产环境配置

# 服务配置
SERVICE_PORT=$SERVICE_PORT
SERVICE_HOST=0.0.0.0
DEBUG=False
ENVIRONMENT=production

# 数据库配置
DB_HOST=47.115.38.118
DB_PORT=9024
DB_NAME=GW_Course
DB_USER=gw_reader
DB_PASSWORD=gw_reader

# AI 模型配置 (需要根据实际情况配置)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-3.5-turbo

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=$PROJECT_DIR/logs/sqlbot.log

# 安全配置
SECRET_KEY=$(openssl rand -hex 32)
ALLOWED_HOSTS=localhost,127.0.0.1,your_domain.com
EOF

    # 设置配置文件权限
    chown $SERVICE_USER:$SERVICE_USER $PROJECT_DIR/config/.env
    chmod 600 $PROJECT_DIR/config/.env
}

# 创建应用启动文件
create_application_file() {
    log_info "创建应用启动文件..."
    
    cat > $PROJECT_DIR/start_sqlbot.py << 'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import pymssql
import pandas as pd
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('/opt/sqlbot/config/.env')

app = Flask(__name__)
CORS(app)

# 配置
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
SERVICE_PORT = int(os.getenv('SERVICE_PORT', 8004))
SERVICE_HOST = os.getenv('SERVICE_HOST', '0.0.0.0')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# 数据库配置
DB_CONFIG = {
    'server': os.getenv('DB_HOST', '47.115.38.118'),
    'port': int(os.getenv('DB_PORT', 9024)),
    'database': os.getenv('DB_NAME', 'GW_Course'),
    'user': os.getenv('DB_USER', 'gw_reader'),
    'password': os.getenv('DB_PASSWORD', 'gw_reader'),
    'charset': 'utf8'
}

# 日志配置
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', '/opt/sqlbot/logs/sqlbot.log')

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
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
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; text-align: center; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.2em; opacity: 0.9; }
        .query-section { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #333; }
        textarea { width: 100%; padding: 15px; border: 2px solid #e1e5e9; border-radius: 8px; font-size: 16px; resize: vertical; min-height: 120px; }
        textarea:focus { outline: none; border-color: #667eea; }
        .btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; transition: transform 0.2s; }
        .btn:hover { transform: translateY(-2px); }
        .result-section { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .result-section h3 { color: #333; margin-bottom: 20px; }
        .loading { text-align: center; padding: 40px; color: #666; }
        .error { background: #fee; border: 1px solid #fcc; color: #c33; padding: 15px; border-radius: 8px; margin: 20px 0; }
        .success { background: #efe; border: 1px solid #cfc; color: #363; padding: 15px; border-radius: 8px; margin: 20px 0; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f8f9fa; font-weight: 600; }
        tr:hover { background: #f8f9fa; }
        .status-info { background: #e3f2fd; border: 1px solid #bbdefb; color: #1976d2; padding: 15px; border-radius: 8px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 SQLBot</h1>
            <p>智能数据查询系统 - 生产环境</p>
        </div>
        
        <div class="query-section">
            <h2>自然语言查询</h2>
            <form id="queryForm">
                <div class="form-group">
                    <label for="query">请输入您的查询需求：</label>
                    <textarea id="query" name="query" placeholder="例如：查询所有学生的姓名和成绩"></textarea>
                </div>
                <button type="submit" class="btn">🔍 执行查询</button>
            </form>
        </div>
        
        <div class="result-section">
            <h3>查询结果</h3>
            <div id="result">
                <div class="status-info">
                    <strong>系统状态：</strong>已连接到数据库 {{ db_info }}<br>
                    <strong>服务时间：</strong>{{ current_time }}<br>
                    <strong>环境：</strong>生产环境
                </div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('queryForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const query = document.getElementById('query').value.trim();
            if (!query) {
                alert('请输入查询内容');
                return;
            }
            
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '<div class="loading">🔄 正在处理查询...</div>';
            
            try {
                const response = await fetch('/api/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: query })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    let html = '<div class="success">✅ 查询成功</div>';
                    html += '<p><strong>生成的SQL：</strong><code>' + data.sql + '</code></p>';
                    
                    if (data.data && data.data.length > 0) {
                        html += '<table><thead><tr>';
                        Object.keys(data.data[0]).forEach(key => {
                            html += '<th>' + key + '</th>';
                        });
                        html += '</tr></thead><tbody>';
                        
                        data.data.forEach(row => {
                            html += '<tr>';
                            Object.values(row).forEach(value => {
                                html += '<td>' + (value || '') + '</td>';
                            });
                            html += '</tr>';
                        });
                        html += '</tbody></table>';
                    } else {
                        html += '<p>查询成功，但没有返回数据。</p>';
                    }
                    
                    resultDiv.innerHTML = html;
                } else {
                    resultDiv.innerHTML = '<div class="error">❌ ' + data.message + '</div>';
                }
            } catch (error) {
                resultDiv.innerHTML = '<div class="error">❌ 请求失败：' + error.message + '</div>';
            }
        });
    </script>
</body>
</html>
'''

def get_db_connection():
    """获取数据库连接"""
    try:
        conn = pymssql.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        return None

def simple_nl_to_sql(query):
    """简单的自然语言到SQL转换"""
    query_lower = query.lower()
    
    # 基础关键词映射
    keyword_mappings = {
        '学生': 'students',
        '课程': 'courses', 
        '成绩': 'grades',
        '教师': 'teachers',
        '班级': 'classes'
    }
    
    # 简单的SQL生成逻辑
    if '查询' in query_lower or '显示' in query_lower or '列出' in query_lower:
        if '学生' in query_lower:
            if '成绩' in query_lower:
                return "SELECT TOP 10 student_name, course_name, score FROM student_grades ORDER BY score DESC"
            else:
                return "SELECT TOP 10 student_id, student_name, class_name FROM students"
        elif '课程' in query_lower:
            return "SELECT TOP 10 course_id, course_name, teacher_name FROM courses"
        elif '成绩' in query_lower:
            return "SELECT TOP 10 student_name, course_name, score FROM student_grades ORDER BY score DESC"
    
    # 默认查询
    return "SELECT TOP 10 * FROM information_schema.tables WHERE table_type = 'BASE TABLE'"

@app.route('/')
def index():
    """主页"""
    db_info = f"{DB_CONFIG['server']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return render_template_string(HTML_TEMPLATE, 
                                db_info=db_info, 
                                current_time=current_time)

@app.route('/api/query', methods=['POST'])
def query_api():
    """查询API接口"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'success': False, 'message': '缺少查询参数'})
        
        user_query = data['query']
        logger.info(f"收到查询请求: {user_query}")
        
        # 转换为SQL
        sql_query = simple_nl_to_sql(user_query)
        logger.info(f"生成SQL: {sql_query}")
        
        # 执行查询
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': '数据库连接失败'})
        
        try:
            df = pd.read_sql(sql_query, conn)
            result_data = df.to_dict('records')
            
            return jsonify({
                'success': True,
                'sql': sql_query,
                'data': result_data,
                'count': len(result_data)
            })
            
        except Exception as e:
            logger.error(f"SQL执行错误: {e}")
            return jsonify({'success': False, 'message': f'SQL执行错误: {str(e)}'})
        
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"API错误: {e}")
        return jsonify({'success': False, 'message': f'服务器错误: {str(e)}'})

@app.route('/health')
def health_check():
    """健康检查接口"""
    try:
        conn = get_db_connection()
        if conn:
            conn.close()
            db_status = "connected"
        else:
            db_status = "disconnected"
        
        return jsonify({
            'service': 'SQLBot',
            'status': 'ok',
            'database': db_status,
            'timestamp': datetime.now().isoformat(),
            'environment': 'production'
        })
    except Exception as e:
        return jsonify({
            'service': 'SQLBot',
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    logger.info(f"SQLBot 启动中... 端口: {SERVICE_PORT}")
    app.run(host=SERVICE_HOST, port=SERVICE_PORT, debug=DEBUG)
EOF

    # 设置文件权限
    chown $SERVICE_USER:$SERVICE_USER $PROJECT_DIR/start_sqlbot.py
    chmod 755 $PROJECT_DIR/start_sqlbot.py
}

# 主函数
main() {
    log_info "开始 SQLBot 远程服务器部署..."
    
    check_root
    detect_os
    install_dependencies
    create_service_user
    create_project_structure
    deploy_application
    create_config_files
    create_application_file
    
    log_info "SQLBot 基础部署完成！"
    log_info "项目目录: $PROJECT_DIR"
    log_info "服务端口: $SERVICE_PORT"
    log_info ""
    log_info "下一步操作："
    log_info "1. 配置 systemd 服务"
    log_info "2. 配置 Nginx 反向代理"
    log_info "3. 配置防火墙规则"
    log_info "4. 启动服务"
}

# 执行主函数
main "$@"