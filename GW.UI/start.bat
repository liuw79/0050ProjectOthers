@echo off
chcp 65001 >nul
title Gaowei School UI Dev Server

echo ============================================================
echo    GAOWEI SCHOOL UI PROJECT - QUICK START
echo ============================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo    Please install Python 3.6+ and try again
    echo    Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check if HTML files exist
if not exist "index.html" if not exist "personal-center.html" (
    echo ❌ No HTML files found in current directory
    echo    Please run this script in the project folder
    pause
    exit /b 1
)

echo ✅ Python detected
echo ✅ Project files found
echo.
echo 🚀 Starting development server...
echo.

:: Start the Python server
python start_server.py

pause