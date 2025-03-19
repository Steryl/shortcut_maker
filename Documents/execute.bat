@echo off
setlocal

:: Execute the Python script with the provided name
python ../shortcut_maker.py "archive" "name/year" "shortcuts/by_name" "year/name"
python ../shortcut_maker.py "archive" "name/year" "shortcuts/by_year" "name/year"

pause

endlocal
