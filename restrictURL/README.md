# 网址限制器

一个简单的桌面应用程序，用于限制访问特定网站，特别适用于防止儿童访问不适宜的网站。

## 功能特点

- 系统托盘驻留，长期运行在后台
- 简单的代理服务器，监控和过滤网络请求
- 可视化管理界面，添加/移除限制的网址
- 访问日志记录，查看访问历史
- 轻量级SQLite数据库存储

## 安装和使用

### 安装依赖

```bash
npm install
```

### 启动应用

#### 方式一：使用命令行
```bash
npm start
```

#### 方式二：使用启动脚本（Windows）
双击项目根目录下的 `start.bat` 文件

### 配置代理

1. 启动应用程序
2. 点击系统托盘图标，选择"显示主窗口"
3. 确保代理服务器状态为"运行中"
4. 在系统网络设置中配置HTTP代理：
   - 地址：127.0.0.1
   - 端口：8080

## 开发

### 项目结构

```
restrictURL/
├── package.json          # 项目配置和依赖
├── main.js               # Electron主进程
├── preload.js            # 预加载脚本
├── start.bat             # Windows启动脚本
├── renderer/             # 前端界面
│   ├── index.html        # 主界面HTML
│   ├── styles.css        # 样式文件
│   └── renderer.js       # 前端逻辑
├── proxy/                # 代理服务
│   └── proxy.js          # 代理服务器实现
├── database/             # 数据库
│   └── db.js             # SQLite数据库操作
└── assets/               # 资源文件
    └── icon.png.placeholder # 图标占位符（需替换为真实图标）
```

### 开发模式

```bash
npm run dev
```

### 打包应用

```bash
npm run build
```

## 技术栈

- **Electron**: 跨平台桌面应用框架
- **Node.js**: 后端运行时
- **Express**: Web框架
- **http-proxy-middleware**: 代理中间件
- **SQLite3**: 轻量级数据库
- **HTML/CSS/JavaScript**: 前端技术

## 注意事项

- 此应用通过代理服务器方式工作，需要配置系统代理设置
- HTTPS请求处理可能需要安装证书（未来版本改进）
- 应用默认限制了一些常见的短视频网站
- 可以通过管理界面添加或移除限制的网址

## 许可证

MIT