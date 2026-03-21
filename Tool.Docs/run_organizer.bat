@echo off
chcp 65001
echo ===================================
echo       WPS文档整理工具
echo ===================================
echo.
echo 正在启动文档整理程序...
echo.

cd /d "c:\Users\28919\SynologyDrive\0050Project\Tool.Docs"

REM 尝试使用anaconda环境的Python
if exist "C:\Users\28919\anaconda3\python.exe" (
    echo 使用Anaconda Python环境
    "C:\Users\28919\anaconda3\python.exe" document_organizer.py
) else (
    REM 如果anaconda不存在，尝试系统Python
    echo 使用系统Python环境
    python document_organizer.py
)

echo.
echo 程序执行完成！
echo 按任意键退出...
pause >nul