@echo off
:: Check if running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

:: Check if Python is installed
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo Python is already installed.
    python --version
    exit /b
)

:: Install Python using winget
echo Python not found. Installing using winget...
winget install --id Python.Python.3 --source winget -e

:: Confirm installation
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo Python installed successfully.
    python --version
) else (
    echo Python installation failed.
)
pause
