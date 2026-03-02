import os
import PyQt6

from PyInstaller.utils.hooks import collect_all

pyqt6_dir = os.path.dirname(PyQt6.__file__)
qt_plugins_dir = os.path.join(pyqt6_dir, "Qt6", "plugins")

# pyreadstat 및 pandas의 모든 데이터를 수집 (바이너리 누락 방지)
datas_ps, binaries_ps, hidden_ps = collect_all('pyreadstat')

a = Analysis(
    ['SPSS_Converter.py'],
    pathex=[],
    binaries=[
        (os.path.join(qt_plugins_dir, "platforms", "*.dylib"), "PyQt6/Qt6/plugins/platforms"),
        (os.path.join(qt_plugins_dir, "styles", "*.dylib"), "PyQt6/Qt6/plugins/styles"),
        (os.path.join(qt_plugins_dir, "imageformats", "*.dylib"), "PyQt6/Qt6/plugins/imageformats"),
        (os.path.join(qt_plugins_dir, "iconengines", "*.dylib"), "PyQt6/Qt6/plugins/iconengines"),
    ] + binaries_ps,
    datas=[] + datas_ps,
    hiddenimports=['PyQt6', 'PyQt6.QtWidgets', 'PyQt6.QtCore', 'PyQt6.QtGui', 'pyreadstat'] + hidden_ps,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'PyQt5.QtNetwork',
        'tkinter', 'tkinterdnd2', 'matplotlib', 'scipy', 'torch', 'tensorflow', 'keras'
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SPSS_Converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['SPSSCSV.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SPSS_Converter',
)
app = BUNDLE(
    coll,
    name='SPSS_Converter.app',
    icon='SPSSCSV.icns',
    bundle_identifier=None,
)
