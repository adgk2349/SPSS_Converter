# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['SPSS_Converter.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['PyQt6', 'PyQt6.QtWidgets', 'PyQt6.QtCore', 'PyQt6.QtGui', 'pyreadstat'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Converter',
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
    name='Converter',
)
app = BUNDLE(
    coll,
    name='SPSS_Converter.app',
    icon='SPSSCSV.icns',
    bundle_identifier=None,
)
