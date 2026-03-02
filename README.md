# SPSS Converter

A simple Python GUI tool to convert SPSS (`.sav`) files to CSV format. 
Works on both macOS and Windows.

## Features
- Clean and simple GUI interface.
- One-click conversion from `.sav` to `.csv`.
- Cross-platform support (macOS/Windows).

## Requirements
To run this script, you need to have Python installed along with the following libraries:

```bash
pip install pandas pyreadstat
```

## How to Use
1. Run the script:
   ```bash
   python3 SPSS_Converter.py
   ```
2. Click "Select & Convert".
3. Choose your `.sav` file.
4. The converted `.csv` file will be saved in the same directory.

## Build as Executable
You can use `PyInstaller` to create a standalone application:

```bash
# For macOS (.app)
pyinstaller --onefile --windowed --icon=SPSSCSV.icns SPSS_Converter.py

# For Windows (.exe)
pyinstaller --onefile --windowed SPSS_Converter.py
```
