@echo off
setlocal

:: Ensure the script runs from the current batch file's directory
cd /d "%~dp0"

set "SCRIPT=%~dp0..\shortcut_maker.py"

:: Execute the Python script with the provided name
python "%SCRIPT%" "archive" "name/year" "shortcuts/by_name" "name/year"
python "%SCRIPT%" "archive" "name/year" "shortcuts/by_year" "year/name"

pause

endlocal
