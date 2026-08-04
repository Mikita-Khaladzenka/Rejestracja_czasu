@echo off

set "PROJECT_DIR=%~dp0"
set "PYTHONW=%PROJECT_DIR%.venv\Scripts\pythonw.exe"
set "WATCHDOG=%PROJECT_DIR%Backend\watchdog.py"

if not exist "%PYTHONW%" (
    echo Nie znaleziono interpretera:
    echo %PYTHONW%
    pause
    exit /b 1
)

if not exist "%WATCHDOG%" (
    echo Nie znaleziono pliku:
    echo %WATCHDOG%
    pause
    exit /b 1
)

start "" /D "%PROJECT_DIR%Backend" "%PYTHONW%" "%WATCHDOG%"

exit /b 0