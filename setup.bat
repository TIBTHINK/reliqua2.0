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

    set PYTHON_INSTALLER=%TEMP%\python-installer.exe
    set PYTHON_URL=https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe

    powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%'"

    echo Running Python installer...
    "%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1

    del /f /q "%PYTHON_INSTALLER%"
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
