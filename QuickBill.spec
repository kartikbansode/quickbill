# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules, collect_data_files


# ============================================================
# QuickBill Pro
# Production Build Configuration
# Version: 3.0.0
# Publisher: Kartik Bansode
# ============================================================

APP_NAME = "QuickBill"
ENTRY_POINT = "app.py"
ICON_FILE = "assets/images/logo.ico"
VERSION_FILE = "version/version_info.txt"


# ============================================================
# Dependencies
# ============================================================

# pyzbar requires the native ZBar libraries.
# Keep these paths relative to the Python environment instead
# of hardcoding the developer's absolute Windows path.

import os
import sys


PYTHON_SITE_PACKAGES = os.path.join(
    sys.prefix,
    "Lib",
    "site-packages"
)

PYZBAR_DIR = os.path.join(
    PYTHON_SITE_PACKAGES,
    "pyzbar"
)


PYZBAR_BINARIES = [
    (
        os.path.join(PYZBAR_DIR, "libiconv.dll"),
        "pyzbar"
    ),
    (
        os.path.join(PYZBAR_DIR, "libzbar-64.dll"),
        "pyzbar"
    ),
]


# ============================================================
# Data Files
# ============================================================

DATA_FILES = [
    (
        "assets",
        "assets"
    ),
] + collect_data_files("reportlab")


# ============================================================
# Hidden Imports
# ============================================================

HIDDEN_IMPORTS = (
    collect_submodules("reportlab")
    + collect_submodules("pyzbar")
)


# ============================================================
# Analysis
# ============================================================

a = Analysis(
    [ENTRY_POINT],

    pathex=[
        os.path.abspath(".")
    ],

    binaries=PYZBAR_BINARIES,

    datas=DATA_FILES,

    hiddenimports=HIDDEN_IMPORTS,

    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],

    excludes=[
        "pytest",
        "unittest",
        "IPython",
        "jupyter",
        "notebook",
    ],

    noarchive=False,

    optimize=2,
)


# ============================================================
# Python Bytecode Archive
# ============================================================

pyz = PYZ(
    a.pure
)


# ============================================================
# QuickBill Pro Executable
# ============================================================

exe = EXE(
    pyz,

    a.scripts,

    a.binaries,

    a.datas,

    [],

    name=APP_NAME,

    debug=False,

    bootloader_ignore_signals=False,

    strip=False,

    # UPX compression can reduce executable size.
    # If antivirus/security software reports false positives,
    # disable this by changing it to False.
    upx=True,

    upx_exclude=[],

    console=False,

    disable_windowed_traceback=False,

    icon=ICON_FILE,

    version=VERSION_FILE,

    # Production application settings
    uac_admin=False,

    argv_emulation=False,

    target_arch=None,

    codesign_identity=None,

    entitlements_file=None,
)