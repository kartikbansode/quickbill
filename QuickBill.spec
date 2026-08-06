# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],

    binaries=[
        (
            r'C:\Users\smart\AppData\Local\Programs\Python\Python311\Lib\site-packages\pyzbar\libiconv.dll',
            'pyzbar'
        ),
        (
            r'C:\Users\smart\AppData\Local\Programs\Python\Python311\Lib\site-packages\pyzbar\libzbar-64.dll',
            'pyzbar'
        ),
    ],

    datas=[
        ('assets', 'assets'),
    ] + collect_data_files('reportlab'),

    hiddenimports=
        collect_submodules('reportlab')
        + collect_submodules('pyzbar'),

    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='QuickBill',

    debug=False,
    bootloader_ignore_signals=False,
    strip=False,

    upx=True,
    upx_exclude=[],

    console=False,

    disable_windowed_traceback=False,

    icon='assets/images/logo.ico',

    version='version/version_info.txt',
)
