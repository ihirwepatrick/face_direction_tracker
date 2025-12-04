# PowerShell script to set up Python 3.10.11 virtual environment

# Check if Python 3.10.11 is available
try {
    $null = py -3.10 --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $pythonCmd = "py -3.10"
        Write-Host "Python 3.10.11 found!" -ForegroundColor Green
    } else {
        throw
    }
} catch {
    Write-Host "Python 3.10.11 not found. Please install it first:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://www.python.org/downloads/release/python-31011/" -ForegroundColor Cyan
    Write-Host "2. Or use: winget install Python.Python.3.10" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "For now, using available Python version..." -ForegroundColor Yellow
    
    # Try to use Python 3.12 or 3.13
    try {
        $null = py -3.12 --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonCmd = "py -3.12"
        } else {
            throw
        }
    } catch {
        try {
            $null = py -3.13 --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $pythonCmd = "py -3.13"
            } else {
                $pythonCmd = "python"
            }
        } catch {
            $pythonCmd = "python"
        }
    }
}

Write-Host "Creating virtual environment with: $pythonCmd" -ForegroundColor Cyan

# Create virtual environment
Invoke-Expression "$pythonCmd -m venv venv"

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

# Install required packages
Write-Host "Installing required packages..." -ForegroundColor Cyan
pip install opencv-python mediapipe pyserial

Write-Host ""
Write-Host "Setup complete! To activate the environment in the future, run:" -ForegroundColor Green
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow

