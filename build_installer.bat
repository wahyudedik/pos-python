@echo off
REM ============================================================================
REM Script untuk membuat installer POS Offline System
REM Requires: PyInstaller, NSIS
REM ============================================================================

setlocal enabledelayedexpansion

REM Set colors
color 0A

echo.
echo ============================================================================
echo POS Offline System - Installer Builder
echo ============================================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher
    pause
    exit /b 1
)

echo [OK] Python found

REM Check if we're in the correct directory
if not exist "src\main.py" (
    echo ERROR: src\main.py not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

echo [OK] Project structure is valid

REM Create build directory
if not exist "build" mkdir build
if not exist "dist" mkdir dist

echo.
echo ============================================================================
echo Step 1: Installing PyInstaller
echo ============================================================================

pip install PyInstaller -q
if %errorlevel% neq 0 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)
echo [OK] PyInstaller installed

echo.
echo ============================================================================
echo Step 2: Building executable with PyInstaller
echo ============================================================================

pyinstaller pos_system.spec --distpath=dist --buildpath=build -y

if %errorlevel% neq 0 (
    echo ERROR: PyInstaller build failed
    echo Check the error messages above
    pause
    exit /b 1
)

echo [OK] Executable built successfully
echo.
echo Executable location: dist\POS-System\POS-System.exe

echo.
echo ============================================================================
echo Step 3: Checking for NSIS (optional)
echo ============================================================================

REM Try to find NSIS
set "NSIS_PATH="

if exist "C:\Program Files\NSIS\makensis.exe" (
    set "NSIS_PATH=C:\Program Files\NSIS\makensis.exe"
) else if exist "C:\Program Files (x86)\NSIS\makensis.exe" (
    set "NSIS_PATH=C:\Program Files (x86)\NSIS\makensis.exe"
)

if defined NSIS_PATH (
    echo [OK] NSIS found at: !NSIS_PATH!
    
    echo.
    echo ============================================================================
    echo Step 4: Building installer with NSIS
    echo ============================================================================
    
    "!NSIS_PATH!" /V4 "installer\POS-System-Installer.nsi"
    
    if %errorlevel% equ 0 (
        echo [OK] Installer created successfully
        echo.
        echo Installer location: dist\POS-System-Installer-v1.0.0.exe
    ) else (
        echo WARNING: NSIS build failed
        echo You can still use the standalone executable from dist\POS-System\POS-System.exe
    )
) else (
    echo [INFO] NSIS not found (optional)
    echo Download from: https://nsis.sourceforge.io
    echo.
    echo You can use the standalone executable without NSIS:
    echo   dist\POS-System\POS-System.exe
)

echo.
echo ============================================================================
echo Build Complete!
echo ============================================================================
echo.
echo Options:
echo 1. Standalone Executable: dist\POS-System\POS-System.exe
echo 2. Installer: dist\POS-System-Installer-v1.0.0.exe (if NSIS installed)
echo.
echo Distribution Guide:
echo - Copy dist\POS-System folder to distribution location
echo - Or use dist\POS-System-Installer-v1.0.0.exe for automated installation
echo.

pause
