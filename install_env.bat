@echo off
setlocal

:: Set project folder to current directory
cd /d "%~dp0"

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not added to PATH.
    pause
    exit /b
)

:: Create virtual environment if it doesn't exist
if not exist "env\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv env
)

:: Activate the virtual environment
call "env\Scripts\activate.bat"

:: Install requirements
if exist "requirements.txt" (
    echo Installing required packages...
    pip install -r "requirements.txt"
) else (
    echo No requirements.txt file found.
)

:: Deactivate the virtual environment
deactivate

echo Done.
pause
endlocal
