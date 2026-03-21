@echo off
echo 正在编译简单浏览器...
echo.

:: 检查是否有gcc编译器
gcc --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到GCC编译器
    echo 请安装MinGW-w64或使用以下命令安装：
    echo winget install mingw
    echo.
    echo 或者下载并安装：
    echo https://www.mingw-w64.org/downloads/
    pause
    exit /b 1
)

:: 清理旧文件
if exist simple_browser.exe del simple_browser.exe

:: 编译程序
echo 编译中...
gcc -o simple_browser.exe simple_browser.c -lwininet -lcomctl32 -luser32 -lgdi32 -lkernel32 -mwindows

if errorlevel 1 (
    echo.
    echo 编译失败！
    pause
    exit /b 1
)

echo.
echo 编译成功！生成文件：simple_browser.exe
echo.
echo 按任意键运行程序...
pause >nul

:: 运行程序
start simple_browser.exe

echo 程序已启动！
pause