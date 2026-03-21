# SQLBot - 智能问数系统

基于 AI 大模型和 RAG 技术的智能数据库查询系统，与 GW.Trackr 使用相同的原生 Python 部署方式，避免 Docker 干扰。

## 快速部署

### 原生 Python 部署（与 GW.Trackr 一致）

```bash
# 进入项目目录
cd GW.Sqlbot

# 运行部署脚本
chmod +x deploy_sqlbot.sh
./deploy_sqlbot.sh
```

## 访问地址

- **Web 界面**: http://localhost:8002
- **健康检查**: http://localhost:8002/health

## 系统配置

### 数据库配置
与 GW.Trackr 使用相同的数据库配置：
- **服务器**: 47.115.38.118
- **端口**: 9024
- **数据库**: GW_Course
- **用户名**: gw_reader
- **密码**: cZ1cM5nX5eX7

### 环境配置
配置文件位置：`config/.env`
```env
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
```

## 功能特性

- 🤖 **自然语言查询**: 支持中文自然语言转 SQL
- 📊 **实时数据查询**: 直接连接 GW_Course 数据库
- 🔍 **智能 SQL 生成**: 基于关键词匹配生成查询语句
- 📱 **响应式设计**: 现代化 Web 界面
- 🔒 **安全访问**: 与 GW.Trackr 共享数据库权限控制
- 🐍 **原生部署**: 使用 Python 虚拟环境，无容器依赖

## 项目结构

```
GW.Sqlbot/
├── deploy_sqlbot.sh      # 部署脚本
├── start_sqlbot.py       # 主程序文件
├── venv/                 # Python 虚拟环境
├── config/
│   └── .env             # 环境配置文件
├── logs/                # 日志目录
├── data/                # 数据目录
├── static/              # 静态文件
└── templates/           # 模板文件
```

## 管理命令

```bash
# 查看运行状态
ps aux | grep start_sqlbot

# 查看端口占用
lsof -i :8002

# 停止服务
kill $(ps aux | grep start_sqlbot | grep -v grep | awk '{print $2}')

# 重启服务
cd GW.Sqlbot
source venv/bin/activate
python start_sqlbot.py &

# 查看日志
tail -f logs/sqlbot.log
```

## 使用示例

### 自然语言查询示例
- "查询用户总数" → `SELECT COUNT(*) as user_count FROM Consumer`
- "查询学员数量" → `SELECT COUNT(*) as student_count FROM Consumer WHERE ConsumerType = '学员'`
- "查询课程总数" → `SELECT COUNT(*) as course_count FROM Course`
- "查询最近数据" → `SELECT TOP 10 * FROM Consumer ORDER BY CreateTime DESC`

### API 调用示例
```bash
# 健康检查
curl http://localhost:8002/health

# 执行查询
curl -X POST http://localhost:8002/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "查询用户总数"}'
```

## 技术架构

- **前端**: HTML + JavaScript (内嵌式)
- **后端**: Python Flask
- **数据库**: SQL Server (GW_Course)
- **依赖管理**: pip + 虚拟环境
- **部署方式**: 原生 Python (与 GW.Trackr 一致)

## 依赖包

主要依赖（使用清华镜像源加速安装）：
- `flask` - Web 框架
- `flask-cors` - 跨域支持
- `pymssql` - SQL Server 连接
- `pandas` - 数据处理
- `numpy` - 数值计算
- `requests` - HTTP 请求
- `python-dotenv` - 环境变量管理
- `openai` - AI 模型接口

## 故障排除

### 常见问题

1. **端口冲突**
   - 检查端口 8002 是否被占用：`lsof -i :8002`
   - 修改 `config/.env` 中的 PORT 配置

2. **数据库连接失败**
   - 确认网络连接到 47.115.38.118:9024
   - 检查 `config/.env` 中的数据库配置
   - 验证数据库用户权限

3. **Python 环境问题**
   - 确保 Python 3.7+ 已安装
   - 检查虚拟环境是否正确激活
   - 重新安装依赖：`pip install -r requirements.txt`

4. **权限问题**
   - 确保部署脚本有执行权限：`chmod +x deploy_sqlbot.sh`
   - 检查目录写入权限

### 日志查看
```bash
# 查看实时日志
tail -f logs/sqlbot.log

# 查看 Flask 输出
python start_sqlbot.py

# 查看系统进程
ps aux | grep start_sqlbot
```

## 与 GW.Trackr 的关系

- **数据库共享**: 使用相同的 GW_Course 数据库
- **部署方式**: 都使用原生 Python 部署
- **配置一致**: 数据库连接配置完全相同
- **端口分离**: SQLBot 使用 8002，GW.Trackr 使用 5001
- **独立运行**: 两个系统互不干扰，可独立启停

## 技术支持

如有问题，请联系技术团队或查看：
- GW.Trackr 项目文档
- 数据库连接配置文档
- Python 虚拟环境配置指南

## 注意事项

⚠️ **重要提示**：
- 这是一个简化版本的演示系统
- 实际生产环境需要配置真实的 AI 模型 API
- 建议根据实际需求扩展查询映射规则
- 生产部署时请加强安全配置和错误处理