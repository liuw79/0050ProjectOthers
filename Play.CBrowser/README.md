# 简单浏览器 (Simple Browser)

一个极简的Windows浏览器，使用纯C语言和Windows API开发，不依赖任何现代浏览器引擎。

## 特性

- **极简设计**：纯文本显示，无CSS、JavaScript支持
- **基本导航**：地址栏、前进、后退、刷新功能
- **HTTP支持**：可以访问基本的HTTP网站
- **自动协议补全**：自动添加http://前缀
- **搜索功能**：输入关键词自动跳转到Google搜索
- **历史记录**：支持前进后退导航
- **HTML解析**：基本的HTML标签移除和实体解码

## 系统要求

- Windows 7 或更高版本
- 网络连接

## 编译要求

- MinGW-w64 (GCC编译器)
- Windows SDK

## 快速开始

### 1. 安装编译器

使用winget安装MinGW：
```bash
winget install mingw
```

或者手动下载安装：
- 访问 https://www.mingw-w64.org/downloads/
- 下载并安装MinGW-w64

### 2. 编译程序

双击运行 `compile.bat` 或在命令行中执行：
```bash
compile.bat
```

### 3. 运行程序

编译成功后会自动启动 `simple_browser.exe`

## 使用说明

1. **输入网址**：在地址栏输入网址，例如：
   - `baidu.com`
   - `www.example.com`
   - `http://www.google.com`

2. **搜索**：直接输入关键词进行Google搜索

3. **导航**：使用前进、后退、刷新按钮

4. **查看内容**：网页内容会以纯文本形式显示在下方区域

## 功能限制

⚠️ **重要提醒**：这是一个极简浏览器，存在以下限制：

- **仅支持纯文本**：不显示图片、视频等媒体内容
- **无CSS支持**：网页样式不会显示
- **无JavaScript**：动态内容和交互功能不可用
- **基础HTML**：只进行简单的标签移除
- **HTTP协议**：主要支持HTTP，HTTPS支持有限
- **编码问题**：可能无法正确显示某些字符编码

## 适用场景

- 学习Windows API编程
- 了解浏览器基本原理
- 访问简单的文本网站
- 快速查看网页源码内容
- 在资源受限环境下浏览网页

## 技术实现

- **语言**：C语言
- **API**：Windows API + WinINet
- **网络**：HTTP请求通过WinINet实现
- **界面**：Win32控件 (Edit, Button, Static)
- **HTML解析**：自定义简单解析器

## 文件结构

```
Play.CBrowser/
├── simple_browser.c    # 主程序源码
├── compile.bat         # 编译脚本
├── README.md          # 说明文档
└── LICENSE.txt        # 许可证
```

## 编译命令

手动编译命令：
```bash
gcc -o simple_browser.exe simple_browser.c -lwininet -lcomctl32 -luser32 -lgdi32 -lkernel32 -mwindows
```

## 故障排除

### 编译错误
- 确保已安装MinGW-w64
- 检查PATH环境变量是否包含gcc路径
- 尝试重新安装编译器

### 运行错误
- 检查网络连接
- 确保Windows版本兼容
- 尝试以管理员身份运行

### 网页无法加载
- 检查URL格式是否正确
- 尝试添加http://前缀
- 某些HTTPS网站可能无法访问

## 许可证

MIT License - 详见 LICENSE.txt 文件

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

---

**注意**：这是一个教育性质的项目，不建议用作日常浏览器使用。对于现代网页浏览，请使用Chrome、Firefox、Edge等成熟浏览器。