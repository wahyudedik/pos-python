#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Quick build POS System executable
.DESCRIPTION
    Fastest way to build standalone executable
.EXAMPLE
    .\quick_build.ps1
#>

param(
    [ValidateSet('single', 'folder')]
    [string]$OutputType = 'single'
)

Write-Host ""
Write-Host "====================================="
Write-Host "POS System - Quick Build"
Write-Host "====================================="
Write-Host ""

# Verify project structure
if (-not (Test-Path "src\main.py")) {
    Write-Host "ERROR: src\main.py not found" -ForegroundColor Red
    Write-Host "Please run from project root directory"
    exit 1
}

# Install PyInstaller
Write-Host "Installing PyInstaller..." -ForegroundColor Cyan
D:\PROJECT\PYTHON\pos\.venv\Scripts\python.exe -m pip install PyInstaller -q

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install PyInstaller" -ForegroundColor Red
    exit 1
}

Write-Host "PyInstaller installed successfully" -ForegroundColor Green

# Build based on type
Write-Host ""
Write-Host "Building executable..." -ForegroundColor Cyan

if ($OutputType -eq 'single') {
    Write-Host "Mode: Single file EXE (easy to distribute)" -ForegroundColor Gray
    D:\PROJECT\PYTHON\pos\.venv\Scripts\pyinstaller.exe `
        --onefile `
        --windowed `
        --name "POS-System" `
        --distpath=dist `
        src\main.py
}
else {
    Write-Host "Mode: Folder (faster startup)" -ForegroundColor Gray
    D:\PROJECT\PYTHON\pos\.venv\Scripts\pyinstaller.exe `
        --onedir `
        --windowed `
        --name "POS-System" `
        --distpath=dist `
        src\main.py
}

# Check result
Write-Host ""
Write-Host "====================================="
Write-Host ""

$exePath = if ($OutputType -eq 'single') {
    "dist\POS-System.exe"
}
else {
    "dist\POS-System\POS-System.exe"
}

if (Test-Path $exePath) {
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host "Executable: $exePath" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Double-click the executable to test"
    Write-Host "2. Verify database is created"
    Write-Host "3. Test all features (Sales, Inventory, Reports)"
    Write-Host "4. Share the executable with users"
    Write-Host ""
    
    Write-Host "Opening dist folder..." -ForegroundColor Gray
    Invoke-Item "dist\"
}
else {
    Write-Host "FAILED" -ForegroundColor Red
    Write-Host "Executable not created. Check error messages above."
    Write-Host ""
}

Write-Host "====================================="
Write-Host ""
