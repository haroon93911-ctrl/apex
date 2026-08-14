@echo off
title Bank Management System Launcher
color 0b
echo ===================================================
echo     Launching Apex Bank Management System...
echo ===================================================
python "%~dp0main.py"
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to run main.py. Please make sure Python is installed.
    pause
)
