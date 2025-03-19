# Shortcutmaker

Make shortcuts from a folder structure.
Use a .bat file to execute shortcut_make.py

When executed this program will create a folder structure in the given directory. If the directory doesn't exist it will create it. You can execute multiple commands after each other to define different order categories, see also the example in Documents/execute.bat. Good practice is to put all shortcut directories in the same parent folder. This program will clean the shortcut folders, if any of the original target folders have been moved or deleted their reference will also be deleted. Use the shortcut directory exclusively for shortcuts to prevent unexpected behavior.

## requirements

- Python 3.11
- pywin32 on cmd

## shortcut_maker.py
Usage: `python shortcut_maker.py <target_dir> <target_format> <shortcut_dir> <shortcut_format>`

Example: 

`python shortcut_maker.pyt "archive" "name/year" "shortcuts" "year/name"`

**Original folder structure:**
- archive
  - Bertha
    - 2016
  - Eileen
    - 2016
    - 2020
  - Karel
    - 2020
    - 2021

**Resulting folder structure:**
- shortcuts
  - 2016
    - Bertha ( -> archive/Bertha/2016)
    - Eileen ( -> archive/Eileen/2016)
  - 2020
    - Eileen ( -> archive/Eileen/2020)
    - Karel ( -> archive/Karel/2020)
  - 2021
    - Karel ( -> archive/Karel/2021)
