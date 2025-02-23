@echo off

:: Check if running as Administrator
NET SESSION >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo This script requires Administrator privileges. Please run as Administrator.
    exit /b 1
)

:: Check if Python is installed
where python >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python not found. Installing...
    powershell -Command "Start-Process msiexec.exe -ArgumentList '/i https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1' -Wait"
) ELSE (
    echo Python is already installed.
)

:: Check if pip is installed
where pip >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo pip not found. Installing...
    python -m ensurepip --default-pip
) ELSE (
    echo pip is already installed.
    echo Checking for pip updates...
    python -m pip install --upgrade pip
)

:: Install dependencies if requirements.txt exists
IF EXIST requirements.txt (
    echo Installing requirements from requirements.txt...
    pip install -r requirements.txt
) ELSE (
    echo requirements.txt not found.
    exit /b 1
)

echo Script completed successfully.
