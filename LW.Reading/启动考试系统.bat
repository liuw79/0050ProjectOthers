@echo off
chcp 65001 >nul
echo ==============================
echo 考试系统启动器
echo ==============================
echo.
echo 选择要启动的版本:
echo 1. 命令行版本 (推荐)
echo 2. 图形界面版本
echo 3. 退出
echo.
set /p choice=请输入选择 (1-3): 

if "%choice%"=="1" (
    echo.
    echo 正在启动命令行版本...
    python simple_exam.py
) else if "%choice%"=="2" (
    echo.
    echo 正在启动图形界面版本...
    python exam_system.py
) else if "%choice%"=="3" (
    echo 再见!
    exit
) else (
    echo 无效选择，请重新运行。
)

pause