#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Build POS Offline System installer
.DESCRIPTION
    Creates standalone executable and NSIS installer for POS System
.EXAMPLE
    .\build_installer.ps1
#>

param(
    [ValidateSet('all', 'exe', 'nsis')]
    [string]$BuildType = 'all',
    
    [switch]$CleanBuild,
    
    [switch]$SkipNSIS
)

Set-StrictMode -Version 3.0
$ErrorActionPreference = 'Stop'

# Colors
function Write-Header {
    param([string]$Text)
    Write-Host ""
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host $Text -ForegroundColor Cyan
    Write-Host "=" * 80 -ForegroundColor Cyan
}

function Write-Ok {
    param([string]$Text)
    Write-Host "[OK]" -ForegroundColor Green -NoNewline
    Write-Host " $Text"
}

function Write-Info {
    param([string]$Text)
    Write-Host "[INFO]" -ForegroundColor Yellow -NoNewline
    Write-Host " $Text"
}

function Write-Error {
    param([string]$Text)
    Write-Host "[ERROR]" -ForegroundColor Red -NoNewline
    Write-Host " $Text"
}

Write-Header "POS Offline System - Installer Builder"

# Check Python
Write-Host ""
Write-Host "Checking prerequisites..."

try {
    $pythonVersion = python --version 2>&1
    Write-Ok $pythonVersion
}
catch {
    Write-Error "Python not found or not in PATH"
    Write-Host "Please install Python 3.10 or higher"
    exit 1
}

# Verify project structure
if (-not (Test-Path "src\main.py")) {
    Write-Error "src\main.py not found"
    Write-Host "Please run this script from the project root directory"
    exit 1
}
Write-Ok "Project structure is valid"

# Clean build
if ($CleanBuild) {
    Write-Host ""
    Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
    
    if (Test-Path "build") {
        Remove-Item -Recurse -Force "build" | Out-Null
        Write-Ok "Cleaned build directory"
    }
    
    if (Test-Path "dist") {
        Remove-Item -Recurse -Force "dist" | Out-Null
        Write-Ok "Cleaned dist directory"
    }
}

# Create directories
@('build', 'dist') | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ | Out-Null
    }
}
Write-Ok "Build directories ready"

# Build executable
if ($BuildType -in @('all', 'exe')) {
    Write-Header "Step 1: Building Executable with PyInstaller"
    
    Write-Host "Installing PyInstaller..." -ForegroundColor Gray
    python -m pip install PyInstaller -q
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to install PyInstaller"
        exit 1
    }
    Write-Ok "PyInstaller installed"
    
    Write-Host ""
    Write-Host "Building executable..." -ForegroundColor Gray
    pyinstaller pos_system.spec --distpath=dist --buildpath=build -y
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "PyInstaller build failed"
        exit 1
    }
    
    Write-Ok "Executable built successfully"
    Write-Host "Location: .\dist\POS-System\POS-System.exe" -ForegroundColor Green
}

# Build NSIS installer
if (($BuildType -in @('all', 'nsis')) -and -not $SkipNSIS) {
    Write-Header "Step 2: Building Installer with NSIS"
    
    # Find NSIS
    $nsisPath = @(
        'C:\Program Files\NSIS\makensis.exe',
        'C:\Program Files (x86)\NSIS\makensis.exe'
    ) | Where-Object { Test-Path $_ } | Select-Object -First 1
    
    if ($nsisPath) {
        Write-Ok "NSIS found at: $nsisPath"
        
        Write-Host ""
        Write-Host "Building installer..." -ForegroundColor Gray
        & $nsisPath /V4 "installer\POS-System-Installer.nsi"
        
        if ($LASTEXITCODE -eq 0) {
            Write-Ok "Installer created successfully"
            Write-Host "Location: .\dist\POS-System-Installer-v1.0.0.exe" -ForegroundColor Green
        }
        else {
            Write-Info "NSIS build had warnings/errors"
        }
    }
    else {
        Write-Info "NSIS not found (optional)"
        Write-Host "Download from: https://nsis.sourceforge.io"
    }
}

# Summary
Write-Header "Build Summary"

Write-Host ""
Write-Host "Available files:" -ForegroundColor Cyan

if (Test-Path "dist\POS-System\POS-System.exe") {
    Write-Host "✓ Standalone Executable" -ForegroundColor Green
    Write-Host "  Location: .\dist\POS-System\POS-System.exe"
}

if (Test-Path "dist\POS-System-Installer-v1.0.0.exe") {
    Write-Host "✓ NSIS Installer" -ForegroundColor Green
    Write-Host "  Location: .\dist\POS-System-Installer-v1.0.0.exe"
}

Write-Host ""
Write-Host "Distribution options:" -ForegroundColor Cyan
Write-Host "1. Copy dist\POS-System folder to users"
Write-Host "2. Use dist\POS-System-Installer-v1.0.0.exe for automated installation"
Write-Host ""

Write-Host "Build completed successfully!" -ForegroundColor Green
