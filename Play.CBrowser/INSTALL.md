# 安装说明

由于您的系统没有安装C编译器，请按照以下步骤安装编译环境：

## 方法1：安装MinGW-w64 (推荐)

### 使用winget安装（Windows 10/11）
```bash
winget install mingw
```

### 手动安装
1. 访问 https://www.mingw-w64.org/downloads/
2. 下载 "MingW-W64-builds" 或 "w64devkit"
3. 解压到 `C:\mingw64`
4. 将 `C:\mingw64\bin` 添加到系统PATH环境变量

### 验证安装
```bash
gcc --version
```

## 方法2：安装Visual Studio Community

1. 访问 https://visualstudio.microsoft.com/zh-hans/vs/community/
2. 下载并安装 Visual Studio Community（免费）
3. 安装时选择 "使用C++的桌面开发" 工作负载
4. 安装完成后，使用 "开发者命令提示符" 编译

## 方法3：使用在线编译器

如果不想安装编译器，可以使用在线C编译器：

1. 访问 https://www.onlinegdb.com/online_c_compiler
2. 复制 `simple_browser.c` 的内容
3. 在线编译并下载可执行文件

注意：在线编译器可能不支持Windows特定的API，建议本地安装编译器。

## 编译步骤

安装编译器后：

1. 打开命令提示符或PowerShell
2. 导航到项目目录
3. 运行编译命令：
   ```bash
   gcc -o simple_browser.exe simple_browser.c -lwininet -lcomctl32 -luser32 -lgdi32 -lkernel32 -mwindows
   ```
4. 运行程序：
   ```bash
   .\simple_browser.exe
   ```

## 故障排除

### 问题：找不到gcc命令
**解决方案：**
- 确保已正确安装MinGW-w64
- 检查PATH环境变量是否包含gcc路径
- 重启命令提示符或PowerShell

### 问题：编译错误
**解决方案：**
- 确保所有库文件都可用
- 检查Windows SDK是否安装
- 尝试使用Visual Studio编译器

### 问题：程序无法运行
**解决方案：**
- 确保Windows版本兼容（Windows 7+）
- 检查网络连接
- 以管理员身份运行

## 快速测试

如果想快速测试程序功能，可以先安装一个轻量级的编译器：

### TDM-GCC（推荐用于快速测试）
1. 访问 https://jmeubank.github.io/tdm-gcc/
2. 下载并安装 TDM-GCC
3. 安装后即可使用gcc命令

### Dev-C++（图形界面）
1. 访问 https://www.bloodshed.net/devcpp.html
2. 下载并安装 Dev-C++
3. 创建新项目，粘贴代码，编译运行

---

**提示：** 如果您主要用于学习目的，推荐安装Visual Studio Community，它提供了完整的开发环境和调试工具。