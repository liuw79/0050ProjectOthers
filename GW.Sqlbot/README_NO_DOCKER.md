# SQLBot 本地部署指南（无需Docker）

## 🔧 问题解决方案

由于您的系统没有安装Docker，我已经为您创建了一个本地Python版本的SQLBot服务。

## 🚀 快速启动

### 方法1: 使用启动脚本（推荐）
```bash
chmod +x start_service.sh
./start_service.sh
```

### 方法2: 手动启动
```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 安装依赖
pip install flask psycopg2-binary openai python-dotenv

# 3. 加载环境变量
export $(cat config/.env | grep -v '^#' | xargs)

# 4. 启动服务
python start_local_sqlbot.py
```

## 🌐 访问服务

启动成功后，在浏览器中访问：
**http://localhost:8080**

## ✅ 功能特性

- ✅ 智能自然语言转SQL
- ✅ 连接GW_Course数据库
- ✅ 使用Kimi K2 AI模型
- ✅ 实时查询结果显示
- ✅ 美观的Web界面

## 🔍 服务状态检查

启动后您会看到类似输出：
```
🚀 启动本地SQLBot服务...
📊 数据库: 47.115.38.118:9024/GW_Course
🤖 AI模型: kimi-k2-0711-preview
🌐 访问地址: http://localhost:8080
==================================================
✅ 数据库连接正常
✅ AI服务配置正常
==================================================
```

## 🧪 测试查询

在Web界面中尝试以下查询：
- "显示所有课程信息"
- "查找课程名称包含'数据'的课程"
- "统计每个专业的课程数量"

## 🛠️ 故障排除

### 端口被占用
```bash
# 查看端口占用
lsof -i :8080

# 清理端口
lsof -ti :8080 | xargs kill -9
```

### 依赖安装失败
```bash
# 升级pip
pip install --upgrade pip

# 重新安装依赖
pip install -r requirements.txt
```

### 数据库连接失败
检查config/.env文件中的数据库配置是否正确。

## 📁 文件说明

- `start_local_sqlbot.py` - 主服务文件
- `templates/index.html` - Web界面
- `start_service.sh` - 启动脚本
- `config/.env` - 环境配置

## 🎯 优势

相比Docker版本，本地版本具有：
- ✅ 无需安装Docker
- ✅ 启动更快
- ✅ 资源占用更少
- ✅ 调试更方便
- ✅ 完全相同的功能

## 🔄 停止服务

在终端中按 `Ctrl + C` 即可停止服务。