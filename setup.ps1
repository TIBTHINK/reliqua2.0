<#
setup.ps1

Idempotent Windows setup script:
1. Ensures running as Administrator
2. Installs Python 3 via winget if missing
3. Installs MSYS2 (provides mingw-w64) via winget if missing
4. Ensures pip is available and installs packages from requirements.txt

This script prefers `winget`. If `winget` is not available it will show
instructions to install Python/MSYS2 manually.
#>

Set-StrictMode -Version Latest

function Abort-IfNotAdmin {
    $current = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    if (-not $current.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        Write-Error "This script must be run as Administrator. Right-click and 'Run as administrator'."
        exit 1
    }
}

function Cmd-Exists($cmd) {
    return (Get-Command $cmd -ErrorAction SilentlyContinue) -ne $null
}

function Winget-Install($id, $name) {
    if (-not (Cmd-Exists winget)) {
        Write-Warning "winget not found; cannot auto-install $name."
        return $false
    }

    try {
        Write-Host "Installing $name via winget (id: $id)..."
        winget install --id $id -e --accept-package-agreements --accept-source-agreements --silent
        return $true
    } catch {
        Write-Warning "winget failed to install ${name}: $_"
        return $false
    }
}

function Install-Winget {
    if (Cmd-Exists winget) {
        Write-Host "winget already installed."
        return $true
    }

    Write-Host "winget not found - attempting to install Windows Package Manager from GitHub releases..."

    try {
        $apiUrl = 'https://api.github.com/repos/microsoft/winget-cli/releases/latest'
        $release = Invoke-RestMethod -Uri $apiUrl -Headers @{ 'User-Agent' = 'PowerShell' }
        $asset = $release.assets | Where-Object { $_.name -like '*DesktopAppInstaller*.msixbundle' } | Select-Object -First 1
        if (-not $asset) {
            Write-Warning "Could not find MSIX bundle in winget releases. Please install winget manually from Microsoft Store or https://github.com/microsoft/winget-cli/releases."
            return $false
        }

        $tmp = Join-Path $env:TEMP $asset.name
        Write-Host "Downloading $($asset.name) to $tmp"
        Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $tmp -UseBasicParsing -Headers @{ 'User-Agent' = 'PowerShell' }

        Write-Host "Installing MSIX bundle (requires sideloading permissions on some systems)..."
        Add-AppxPackage -Path $tmp -ErrorAction Stop

        Remove-Item $tmp -ErrorAction SilentlyContinue
        Write-Host "winget (App Installer) installed - please restart the shell if necessary."
        return $true
    } catch {
        Write-Warning "Failed to install winget automatically: $_"
        Write-Host "Please install App Installer (winget) from the Microsoft Store or from: https://github.com/microsoft/winget-cli/releases"
        return $false
    }
}

function Ensure-Python {
    if (Cmd-Exists python -or Cmd-Exists py) {
        Write-Host "Python already installed."
        return $true
    }

    # Try winget Python 3 package
    $candidates = @('Python.Python.3', 'Python.Python.3.11')
    foreach ($id in $candidates) {
        if (Winget-Install $id 'Python 3') {
            return $true
        }
    }

    Write-Warning "Automatic Python installation failed or winget missing."
    Write-Host "Install Python 3 manually from https://www.python.org/downloads/ or install winget."
    return $false
}

function Ensure-MSYS2 {
    # MSYS2 provides mingw-w64 toolchains on Windows
    if ((Test-Path "C:\msys64") -or (Cmd-Exists pacman)) {
        Write-Host "MSYS2 or mingw toolchain seems present."
        return $true
    }

    # Try winget msys2
    if (Winget-Install 'MSYS2.MSYS2' 'MSYS2 (mingw-w64)') {
        Write-Host "MSYS2 installed. You may still need to run msys2 shell and install mingw packages via pacman."
        return $true
    }

    Write-Warning "Automatic MSYS2 installation failed or winget missing."
    Write-Host "If you need mingw-w64, install MSYS2 from https://www.msys2.org/ and then run: pacman -Syu mingw-w64-x86_64-gcc"
    return $false
}

function Ensure-PipAndInstallRequirements {
    # Prefer explicit python executable
    $pyCmd = $null
    if (Cmd-Exists py) { $pyCmd = 'py' }
    elseif (Cmd-Exists python) { $pyCmd = 'python' }
    else { Write-Error "Python not found. Cannot install pip packages."; return $false }

    try {
        & $pyCmd -m ensurepip --upgrade | Out-Null
    } catch {
        Write-Host "ensurepip failed or already present: $_"
    }

    & $pyCmd -m pip install --upgrade pip setuptools wheel

    $req = Join-Path $PSScriptRoot 'requirements.txt'
    if (-not (Test-Path $req)) {
        Write-Warning "requirements.txt not found at $req. Skipping pip install."
        return $true
    }

    Write-Host "Installing Python packages from requirements.txt (system-wide)..."
    try {
        $sysPrefix = & $pyCmd -c "import sys; print(sys.prefix)"
        & $pyCmd -m pip install --upgrade -r $req --prefix $sysPrefix
    } catch {
        Write-Warning "System-wide pip install failed: $_. Falling back to default pip install."
        & $pyCmd -m pip install -r $req
    }
}

# ----- Script start -----
Abort-IfNotAdmin

Write-Host "Starting Windows setup: Python3, MSYS2 (mingw), pip requirements"

if (-not (Cmd-Exists winget)) {
    Write-Host "winget not detected - attempting to install winget (App Installer)..."
    $wingetInstalled = Install-Winget
    if (-not $wingetInstalled) {
        Write-Warning "winget installation failed or was not completed. winget-based installs may not work." 
    }
}

$pythonOk = Ensure-Python
$msysOk = Ensure-MSYS2

if (-not $pythonOk) {
    Write-Host "Python installation was not successful. Aborting pip package installation."
    exit 1
}

Ensure-PipAndInstallRequirements

Write-Host 'Setup completed. If MSYS2 was installed, open MSYS2 shell and run pacman -Syu then install mingw-w64 packages as needed.'
