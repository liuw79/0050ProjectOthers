@echo off
chcp 65001 >nul
echo 正在为您提供MinGW-w64安装方案...
echo.

echo 由于winget安装失败，请选择以下安装方案之一：
echo.
echo 方案1：手动下载安装（推荐）
echo ================================
echo 1. 访问：https://www.mingw-w64.org/downloads/
echo 2. 选择 "MingW-W64-builds" 或 "w64devkit"
echo 3. 下载并解压到 C:\mingw64
echo 4. 将 C:\mingw64\bin 添加到系统PATH环境变量
echo.
echo 方案2：使用MSYS2安装
echo ========================
echo 1. 访问：https://www.msys2.org/
echo 2. 下载并安装MSYS2
echo 3. 在MSYS2终端中运行：
echo    pacman -S mingw-w64-x86_64-gcc
echo    pacman -S mingw-w64-x86_64-make
echo.
echo 方案3：使用TDM-GCC（最简单）
echo ==============================
echo 1. 访问：https://jmeubank.github.io/tdm-gcc/
echo 2. 下载TDM-GCC安装程序
echo 3. 运行安装程序，选择默认设置
echo 4. 安装完成后重启命令提示符
echo.
echo 方案4：使用Visual Studio（功能最全）
echo ====================================
echo 1. 访问：https://visualstudio.microsoft.com/zh-hans/vs/community/
echo 2. 下载Visual Studio Community（免费）
echo 3. 安装时选择"使用C++的桌面开发"工作负载
echo 4. 使用"开发者命令提示符"编译程序
echo.
echo 推荐顺序：TDM-GCC > Visual Studio > MSYS2 > 手动安装
echo.
echo 安装完成后，请重启命令提示符并运行：
echo gcc --version
echo.
echo 然后使用以下命令编译程序：
echo gcc -o simple_browser.exe simple_browser.c -lwininet -lcomctl32 -luser32 -lgdi32 -lkernel32 -mwindows
echo.
pause