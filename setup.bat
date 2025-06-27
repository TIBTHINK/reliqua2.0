@echo off
setlocal enabledelayedexpansion

:: Check for administrator privileges
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if %errorlevel% NEQ 0 (
    echo.
    echo This script requires Administrator privileges.
    echo Right-click this file and select "Run as administrator".
    pause
    exit /b
)

:: Check if Python is installed
where python >nul 2>&1
if %errorlevel% NEQ 0 (
    echo Python not found. Downloading and installing Python...

    python3
    echo Running Python installer...


) else (
    echo Python is already installed.
)

:: Refresh environment
set PATH=%PATH%;%ProgramFiles%\Python312\Scripts;%ProgramFiles%\Python312\

:: Upgrade pip
echo Upgrading pip...
python -m ensurepip
python -m pip install --upgrade pip

:: Install requirements
if exist requirements.txt (
    echo Installing packages from requirements.txt...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install some packages.
        exit /b 1
    )
) else (
    echo requirements.txt not found.
    exit /b 1
)

echo.
echo Script completed successfully.
pause
