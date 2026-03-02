# SPSS Converter (SPSS SAV to CSV)

A simple Python GUI tool to convert SPSS (`.sav`) files to CSV format.  
SPSS (`.sav`) 파일을 CSV 형식으로 변환해주는 간단한 파이썬 GUI 도구입니다.

---

## 🇺🇸 English Instructions

### Features
- **Simple GUI**: Clean and easy-to-use interface.
- **One-Click Conversion**: Select and convert instantly.
- **Cross-Platform**: Works on both macOS and Windows.

### Requirements
To run this script, you need to have Python installed along with the following libraries:

```bash
pip install pandas pyreadstat
```

### How to Use
1. **Run the script**:
   ```bash
   python3 SPSS_Converter.py
   ```
2. **Select & Convert**: Click the button and choose your `.sav` file.
3. **Success**: The converted `.csv` file will be saved in the same directory.

### Build as Executable
You can use `PyInstaller` to create a standalone application:

```bash
# For macOS (.app)
pyinstaller --onefile --windowed --icon=SPSSCSV.icns SPSS_Converter.py

# For Windows (.exe)
pyinstaller --onefile --windowed SPSS_Converter.py
```

---

## 🇰🇷 한국어 설명

### 주요 기능
- **간단한 GUI**: 깔끔하고 사용하기 쉬운 인터페이스.
- **원클릭 변환**: 클릭 한 번으로 즉시 변환.
- **교차 플랫폼**: 맥(macOS)과 윈도우(Windows) 모두 지원.

### 설치 요구사항
이 스크립트를 실행하려면 파이썬과 아래 라이브러리 설치가 필요합니다:

```bash
pip install pandas pyreadstat
```

### 사용 방법
1. **스크립트 실행**:
   ```bash
   python3 SPSS_Converter.py
   ```
2. **파일 선택 및 변환**: 버튼을 클릭하고 `.sav` 파일을 선택하세요.
3. **완료**: 변환된 `.csv` 파일이 같은 폴더에 저장됩니다.

### 실행 파일 만들기
`PyInstaller`를 사용하여 독립 실행 파일을 만들 수 있습니다:

```bash
# 맥용 (.app)
pyinstaller --onefile --windowed --icon=SPSSCSV.icns SPSS_Converter.py

# 윈도우용 (.exe)
pyinstaller --onefile --windowed SPSS_Converter.py
```
