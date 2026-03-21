@echo off
chcp 65001 >nul
echo Compiling Simple Browser...
echo.

REM Check if gcc is available
gcc --version >nul 2>&1
if errorlevel 1 (
    echo Error: GCC compiler not found
    echo Please install MinGW-w64 or use:
    echo winget install mingw
    echo.
    echo Or download from:
    echo https://www.mingw-w64.org/downloads/
    pause
    exit /b 1
)

REM Clean old files
if exist simple_browser.exe del simple_browser.exe

REM Compile program
echo Compiling...
gcc -o simple_browser.exe simple_browser.c -lwininet -lcomctl32 -luser32 -lgdi32 -lkernel32 -mwindows

if errorlevel 1 (
    echo.
    echo Compilation failed!
    pause
    exit /b 1
)

echo.
echo Compilation successful! Generated: simple_browser.exe
echo.
echo Press any key to run the program...
pause >nul

REM Run program
start simple_browser.exe

echo Program started!
pause