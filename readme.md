# Shortcutmaker

Make shortcuts from a folder structure.
Use a .bat file to execute shortcut_make.py

## shortcut_maker.py
Usage: python shortcut_maker.py <target_dir> <target_format> <shortcut_dir> <shortcut_format>

Example: python shortcut_maker.pyt "_all" "name/year" "Shortcuts" "year/name"

**Original folder structure:**
- _all
  - Karel
    - 2016
  - Bertha
    - 2015
    - 2016

**Resulting folder structure:**
- Shortcuts
  - 2015
    - Karel (shortcut to _all/Kerel/2015)
    - Bertha (shortcut to _all/Bertha/2015)
  - 2016
    - Bertha (shortcut to _all/Bertha/2016)
