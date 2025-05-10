@echo off
setlocal

:: Set installation folder
set "FOLDER=..\"
set "SCRIPT=%FOLDER%\shortcut_maker.py"

:: Ensure the script runs from the current batch file's directory
cd /d "%~dp0"

:: Check if the virtual environment exists
if not exist "%FOLDER%\env\Scripts\activate.bat" (
    echo Virtual environment not found.
    pause
    exit /b
)

:: Activate the virtual environment
call "%FOLDER%\env\Scripts\activate.bat"

:: Execute the Python script
python "%SCRIPT%" "archive" "name/year" "shortcuts/by_name" "name/year"
python "%SCRIPT%" "archive" "name/year" "shortcuts/by_year" "year/name"

:: Deactivate the virtual environment (optional)
deactivate

pause

endlocal
