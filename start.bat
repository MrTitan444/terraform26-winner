@echo off
title TERRAFORM Server
cd /d "%~dp0"

echo ========================================================
echo   🌱 Starting TERRAFORM Offline Knowledge Base Server
echo ========================================================

where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PYTHON_CMD=python"
    goto :run
)

where py >nul 2>nul
if %errorlevel% equ 0 (
    set "PYTHON_CMD=py"
    goto :run
)

echo [ERROR] Python was not found in PATH. Please install Python 3.
pause
exit /b 1

:run
echo Starting server on http://localhost:8000 ...
echo Press Ctrl+C to stop the server.
echo ========================================================
"%PYTHON_CMD%" run.py serve %*
pause
