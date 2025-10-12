@echo off
echo ============================================================
echo 5GHz Cleaner - Suite de Tests Complete
echo ============================================================
echo.

echo [1/2] Tests de securite...
py tests\test_security_core.py
if %errorlevel% neq 0 (
    echo.
    echo ERREUR: Tests de securite echoues!
    pause
    exit /b 1
)

echo.
echo [2/2] Lancement de l'application...
echo.
echo Appuyez sur une touche pour lancer l'application...
pause > nul

py main.py

echo.
echo ============================================================
echo Tests termines!
echo ============================================================
pause
