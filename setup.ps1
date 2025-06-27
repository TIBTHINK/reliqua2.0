# Check for administrator privileges
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(`
    [Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Error "You must run this script as Administrator!"
    exit 1
}

# Function to install Python via official installer
function Install-Python {
    Write-Output "Downloading and installing Python..."
    $installerPath = "$env:TEMP\python-installer.exe"
    $pythonUrl = "https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe"

    Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath

    Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_pip=1" -Wait

    Remove-Item $installerPath
}

# Check for python3 and pip3
$pythonExists = Get-Command python3 -ErrorAction SilentlyContinue
$pipExists = Get-Command pip -ErrorAction SilentlyContinue

if (-not $pythonExists -or -not $pipExists) {
    Write-Output "python3 or pip not found. Installing..."
    Install-Python
} else {
    Write-Output "python3 and pip are already installed."
}

# Refresh environment in case Python was just installed
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)

# Check for requirements.txt and install
if (Test-Path ".\requirements.txt") {
    Write-Output "Installing Python packages from requirements.txt..."
    python3 -m pip install --upgrade pip
    python3 -m pip install -r .\requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to install requirements."
        exit 1
    }
} else {
    Write-Error "requirements.txt not found."
    exit 1
}

Write-Output "Script completed successfully."