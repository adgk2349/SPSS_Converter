# SPSS Converter (SPSS SAV to CSV)

A Python GUI tool to convert SPSS (`.sav`) files to CSV format, built with PyQt6.  
SPSS (`.sav`) 파일을 CSV 형식으로 변환해주는 파이썬 GUI 도구입니다. (PyQt6 기반)

---

## 🇺🇸 English Instructions

### Features
- **Frameless rounded UI** — Native transparent rounded corners on macOS (PyQt6)
- **Drag & Drop** — Drop `.sav` files directly onto the app window
- **One-Click Conversion** — Select and convert instantly
- **Status indicator** — Live conversion status in the app (no popup)
- **Cross-Platform** — macOS and Windows

### Requirements
```bash
pip install PyQt6 pandas pyreadstat
```

### How to Use
1. **Run the script**:
   ```bash
   python3 SPSS_Converter.py
   ```
2. **Drag & Drop** a `.sav` file onto the drop zone, or click **직접 선택 (Select File)**.
3. **Done** — The `.csv` file is saved in the same directory as the original.

### Build as Executable
The app must be built using the `.spec` file to ensure correct Qt6 plugin mapping:

```bash
# macOS (.app)
/Users/seungminlee/anaconda3/bin/python -m PyInstaller --clean Converter.spec --noconfirm
```

*Note: Avoid using `pyinstaller SPSS_Converter.py` directly as it may cause Qt plugin version conflicts.*

---

## 🇰🇷 한국어 설명

### 주요 기능
- **프레임리스 라운드 UI** — macOS에서 진짜 투명 모서리 처리 (PyQt6)
- **드래그 앤 드롭** — `.sav` 파일을 앱 창에 바로 드롭
- **원클릭 변환** — 버튼 클릭으로 즉시 변환
- **상태 표시** — 변환 결과를 앱 하단에 표시 (팝업 없음)
- **교차 플랫폼** — macOS 및 Windows 지원

### 설치 요구사항
```bash
pip install PyQt6 pandas pyreadstat
```

### 사용 방법
1. **스크립트 실행**:
   ```bash
   python3 SPSS_Converter.py
   ```
2. **드래그 앤 드롭**: `.sav` 파일을 드롭존에 끌어다 놓거나, **직접 선택 (Select File)** 버튼 클릭.
3. **완료**: 변환된 `.csv` 파일이 원본과 같은 폴더에 저장됩니다.

### 실행 파일 만들기
Qt6 플러그인 충돌을 방지하기 위해 반드시 `.spec` 설정을 사용하여 빌드해야 합니다:

```bash
# 맥용 (.app)
/Users/seungminlee/anaconda3/bin/python -m PyInstaller --clean Converter.spec --noconfirm
```

*참고: `pyinstaller SPSS_Converter.py`를 직접 실행하면 Qt 플러그인 버전 오류가 발생할 수 있습니다.*
