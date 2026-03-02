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
        'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'PyQt5.QtNetwork', 'PyQt5-sip',
        'tkinter', 'tkinterdnd2', 'matplotlib', 'scipy', 'torch', 'tensorflow', 'keras',
        'bokeh', 'pyarrow', 'selenium', 'sphinx', 'h5py', 'jedi', 'babel', 'nbformat',
        'IPython', 'zmq', 'pygments', 'docutils', 'PIL', 'lxml', 'cryptography', 'notebook',
        'llvmlite', 'numba', 'pywt', 'skimage', 'tables',
        'PyQt6.QtNetwork', 'PyQt6.QtQml', 'PyQt6.QtQuick', 'PyQt6.QtSql', 'PyQt6.QtXml', 'PyQt6.QtDBus',
        'PyQt6.QtPositioning', 'PyQt6.QtMultimedia', 'PyQt6.QtBluetooth', 'PyQt6.QtSensors'
    ],
    noarchive=False,
    optimize=0,
)

# 불필요한 대형 바이너리 파일 필터링 (LLVM, Qt5, Unused Qt6)
exclude_bin_names = [
    'libqt5', 'libllvm', 'libbrowser', 'libqt6network', 'libqt6qml', 'libqt6quick', 
    'libqt6sql', 'libqt6xml', 'libqt6dbus', 'libqt6multimedia', 'libqt6bluetooth',
    'libqt6positioning', 'libqt6sensors', 'libqt6web', 'libqt6remote'
]

a.binaries = [x for x in a.binaries if not 
              (any(name in x[0].lower() for name in exclude_bin_names) or 
               'libQt5' in x[1] or 
               ('Qt6' in x[1] and any(name[3:] in x[1].lower() for name in exclude_bin_names if name.startswith('libqt6'))))]

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
