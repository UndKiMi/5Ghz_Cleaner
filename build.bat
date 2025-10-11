@echo off
echo ========================================
echo 5Gh'z Cleaner - Build Script
echo ========================================
echo.

echo Installing dependencies...
py -m pip install -r requirements.txt
echo.

echo Building executable...
py -m flet pack main.py --name "5Ghz_Cleaner" --add-data "backend;backend" --add-data "frontend;frontend"
echo.

echo ========================================
echo Build complete!
echo Executable location: dist\5Ghz_Cleaner.exe
echo ========================================
pause
