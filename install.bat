@echo off
echo ========================================
echo 5Gh'z Cleaner - Installation
echo ========================================
echo.

echo Checking Python installation...
py --version
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
py -m pip install --upgrade pip
py -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Installation failed!
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation complete!
echo ========================================
echo.
echo You can now run the application with:
echo   - Double-click on run.bat
echo   - Or run: py main.py
echo.
pause
