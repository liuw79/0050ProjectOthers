@echo off
echo 正在启动高维学堂庆祝页面...
echo.
echo 如果浏览器没有自动打开，请手动打开以下文件：
echo %~dp0index.html
echo.
start "" "%~dp0index.html"
echo.
echo 页面已在默认浏览器中打开！
echo 按任意键退出...
pause >nul