# Shortcutmaker

This script will make shortcut folders in a specified structure.
The script can be triggered from a bat file to use in Windows explorer.

When executed this script will create a folder structure in the given directory. If the given directory doesn't exist it will create it. You can execute multiple commands after each other to define different order categories, see also the example in Documents/execute.bat. Good practice is to put all shortcut directories in the same parent folder. This program will clean the shortcut folders, if any of the original target folders have been moved or deleted their shortcut will also be deleted. Use the shortcut directory exclusively for shortcuts to prevent unexpected behavior to your files.

## requirements & setup

- Python 3.11
- Virtual Environment
- Python packages from requirements.txt

### 1. **Install Python 3.11**

- Download Python 3.11 from:  
  [https://www.python.org/downloads/release/python-3110/](https://www.python.org/downloads/release/python-3110/)

- During installation:
  - Check the box that says `Add Python to PATH`
  - Then click 'Install Now'

### 2. **Create a Virtual Environment**

#### Option 1: Execute the `install.bat` file

- This will automatically create a virtual environment and install the required packages.

#### Option 2: Manual setup
1. Open a **Command Prompt** window.
2. Navigate to your project folder where `requirements.txt` is located.
3. Run the following commands:

```cmd
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
deactivate
```

## Options
The script can be executed like this with the following options:<br>
`python shortcut_maker.py <target_dir> <target_format> <shortcut_dir> <shortcut_format>`

- `target_dir`: Parent folder of your original folder structure<br>
  - `Documents\archive`
- `target_format`: Description of your original folder structure<br>
  - `name\year`
- `shortcut_dir`: Parent folder of your shortcut structure<br>
  - `Documents\shortcuts`
- `shortcut_format`: Description of your shortcut folder structure<br>
  - `year\name`



## Usage example

Your administration is stored like this: `Documents\archive\2016\Bertha` and you want to access your same documents through the shortcut: `Documents\shortcuts\Bertha\2016`.

### Option 1: python script

You can use the python script directly to make a shortcut structure:
1. Open a cmd window and navigate to the `shortcut_maker` directory.
2. Activate the **Virtual Environment**
3. Execute the `shortcut_maker.py` with the right options.
4. Deactivate the **Virtual Environment**

```cmd
env\Scripts\activate
python shortcut_maker.py "Documents\archive" "year\name" "Documents\shortcuts" "name\year"
deactivate
```
### Option 2: bat file

You can place a bat file in a folder for repeated use. Just execute the bat file to adjust your shortcuts. There is an example of one in the 'Documents' folder in this project. You easily execute multiple shortcut structures like this.

#### Setup

1. Open Windows Explorer and go to the `shortcut_maker\Documents` directory.
2. Right-click `execute.bat` and click `edit`, you see here the setup for the current folder structure. 
3. Set the location of `shortcut_maker` folder, it is now set to `..\`
3. Setup your commands for the shortcut structure. It is now set to make one structure by year and one by name.
4. Save the file.

#### Run
1. Open Windows Explorer and go to the `shortcut_maker\Documents` directory.
2. Run `execute.bat`, it will now create or update the shortcut folders that have been previously setup.

#### Custom setup

You can copy and edit the bat file to multiple locations to organise those folders. For example to organise your administration,  photos or inventory.

1. Save the `shortcut_maker` folder in a fixed location like `C:\software\shortcut_maker`.
2. Edit `shortcut_maker\Documents\execute.bat`, change the line for the folder location to the current location:<br>
`set "FOLDER=C:\software\shortcut_maker"`
3. Save the bat file.
4. Copy the bat file to your own folders that you want to organise.
5. Edit each bat file to specify the shortcut structure that you want the create for that folder.

#### Multi-level organisation

In our example we used two levels for organisation, but you can use more. So 






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
