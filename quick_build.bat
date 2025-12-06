@echo off
REM Perintah cepat untuk build installer

cd /d "%~dp0"

echo.
echo ============================================================
echo POS System - Quick Build
echo ============================================================
echo.

echo Installing dependencies...
D:\PROJECT\PYTHON\pos\.venv\Scripts\python.exe -m pip install PyInstaller -q

echo Building executable...
D:\PROJECT\PYTHON\pos\.venv\Scripts\pyinstaller.exe ^
    --name POS-System ^
    --onefile ^
    --windowed ^
    --icon=src\assets\icon.ico ^
    src\main.py

echo.
echo ============================================================
if exist dist\POS-System.exe (
    echo SUCCESS! Executable created at: dist\POS-System.exe
) else (
    echo Build completed. Check output above for errors.
)
echo ============================================================
echo.

pause
