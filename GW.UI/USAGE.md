# 使用指南

## 🚀 快速启动

### 方法一：自动化脚本启动（推荐）

#### Windows用户
```bash
# 双击运行
start.bat

# 或命令行运行
start.bat
```

#### Mac/Linux用户
```bash
# 命令行运行
./start.sh

# 或者
bash start.sh
```

#### 直接Python启动
```bash
# Python 3
python3 start_server.py

# 或 Python 2/3
python start_server.py
```

### 方法二：简单HTTP服务器
```bash
# Python 3
python3 -m http.server 8080

# Python 2
python -m SimpleHTTPServer 8080
```

## 📋 访问地址

启动成功后，在浏览器中访问：

- **项目首页**: http://localhost:8080/
- **个人中心**: http://localhost:8080/personal-center.html

## 🛠️ 项目结构

```
GW.UI/
├── index.html              # 项目导航首页
├── personal-center.html    # 个人中心页面
├── personal-center.css     # 样式表
├── start_server.py         # Python服务器启动器
├── start.bat               # Windows启动脚本
├── start.sh                # Mac/Linux启动脚本
├── README.md               # 项目说明
├── progress.md             # 进度跟踪
└── USAGE.md               # 使用指南
```

## 🎯 功能特色

### 项目导航首页
- 现代化卡片式布局
- 项目状态标识
- 响应式设计
- 品牌色彩规范

### 个人中心页面
- 扁平化设计理念
- 完整功能模块
- 移动端适配
- 交互动画效果

### 自动化启动
- 自动端口检测
- 浏览器自动打开
- 跨平台兼容
- 友好错误提示

## 💡 使用技巧

### 移动端预览
启动服务器后，在同一网络下的移动设备上访问：
```
http://[你的IP地址]:8080
```

### 自定义端口
编辑 `start_server.py` 文件，修改 `DEFAULT_PORT` 变量：
```python
DEFAULT_PORT = 3000  # 改为你想要的端口
```

### 关闭服务器
在终端中按 `Ctrl+C` 停止服务器

## 🔧 故障排除

### Python未安装
- **Windows**: 从 https://www.python.org/downloads/ 下载安装
- **Mac**: `brew install python3`
- **Ubuntu**: `sudo apt install python3`

### 端口被占用
脚本会自动检测并使用下一个可用端口（8080-8180）

### 文件权限问题（Mac/Linux）
```bash
chmod +x start.sh
```

### 浏览器未自动打开
手动访问终端中显示的地址

## 📱 移动端测试

推荐在以下设备/浏览器中测试：
- iPhone Safari
- Android Chrome
- iPad Safari
- 各种屏幕尺寸的模拟器

## 🌟 开发建议

1. **实时预览**: 修改代码后刷新浏览器即可看到变化
2. **移动端调试**: 使用浏览器开发者工具的设备模拟器
3. **性能测试**: 使用Lighthouse进行性能评估
4. **兼容性测试**: 在不同浏览器中测试

---

**更新时间**: 2024年  
**适用版本**: v1.0.0+ 