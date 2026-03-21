@echo off
for /f "delims=" %%i in ('dir /b /a:-d "%userprofile%\Desktop\*.lnk"') do (
   move "%userprofile%\Desktop\%%i" C:\backup\icons

)
pause
