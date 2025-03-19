@echo off
setlocal

:: Execute the Python script with the provided name
python ../shortcut_maker.py "archive" "name/year" "shortcuts/by_name" "name/year"
python ../shortcut_maker.py "archive" "name/year" "shortcuts/by_year" "year/name"

pause

endlocal
