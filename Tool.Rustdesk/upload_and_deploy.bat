@echo off
chcp 65001
echo === Rustdesk 服务器部署工具 ===
echo.

set SERVER=root@op.gaowei.com
set SCRIPT_DIR=%~dp0

echo 正在上传部署脚本到服务器...
echo.

REM 上传快速部署脚本
scp "%SCRIPT_DIR%quick_deploy.sh" %SERVER%:/tmp/
if %errorlevel% neq 0 (
    echo 错误: 上传失败，请检查SSH连接
    pause
    exit /b 1
)

echo 脚本上传成功！
echo.
echo 现在请手动执行以下命令:
echo.
echo 1. 连接到服务器:
echo    ssh %SERVER%
echo.
echo 2. 执行部署脚本:
echo    chmod +x /tmp/quick_deploy.sh
echo    /tmp/quick_deploy.sh
echo.
echo 3. 部署完成后，记录显示的公钥用于客户端配置
echo.
echo 按任意键继续...
pause > nul

REM 尝试直接连接SSH
echo 尝试直接连接到服务器...
ssh %SERVER%

echo.
echo 部署完成！
pause