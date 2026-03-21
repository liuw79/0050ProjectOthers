@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo 🤖 微信自动化脚本启动器
echo ========================================
echo.

echo 正在启动微信自动化脚本...
echo 请确保微信已经启动并登录
echo.

:: 使用Anaconda Python运行脚本
"C:\Users\28919\anaconda3\python.exe" quick_start.py

echo.
echo 脚本执行完成
pause