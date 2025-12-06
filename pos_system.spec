# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file untuk POS Offline System
Digunakan untuk membuat executable standalone application
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(r'D:\PROJECT\PYTHON\pos')
sys.path.insert(0, str(project_root))

block_cipher = None

a = Analysis(
    [str(project_root / 'src' / 'main.py')],
    pathex=[str(project_root)],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtPrintSupport',
        'sqlalchemy',
        'sqlalchemy.orm',
        'midtransclient',
        'dotenv',
        'qdarkstyle',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='POS-System',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False untuk GUI app tanpa console window
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / 'src' / 'assets' / 'icon.ico') if (project_root / 'src' / 'assets' / 'icon.ico').exists() else None,
)

# Untuk membuat folder distribusi (optional)
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='POS-System'
# )
