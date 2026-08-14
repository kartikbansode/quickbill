# -*- mode: python ; coding: utf-8 -*-

"""
QuickBill
Production Build Configuration
Version 3.1.0
Copyright © 2026 Kartik Bansode. All Rights Reserved.
"""

import os
import sys

from PyInstaller.utils.hooks import (
    collect_data_files,
    collect_submodules,
)


# ============================================================
# Application
# ============================================================

APP_NAME = "QuickBill"
ENTRY_POINT = "app.py"
ICON_FILE = "assets/images/logo.ico"
VERSION_FILE = "version/version_info.txt"


# ============================================================
# Project Root
# ============================================================

PROJECT_ROOT = os.path.abspath(".")


# ============================================================
# Python Site-Packages
# ============================================================

PYTHON_SITE_PACKAGES = os.path.join(
    sys.prefix,
    "Lib",
    "site-packages",
)


# ============================================================
# PyZBar Native Dependencies
# ============================================================

PYZBAR_DIR = os.path.join(
    PYTHON_SITE_PACKAGES,
    "pyzbar",
)


PYZBAR_BINARIES = []

for dll_name in (
    "libiconv.dll",
    "libzbar-64.dll",
):
    dll_path = os.path.join(
        PYZBAR_DIR,
        dll_name,
    )

    if os.path.exists(dll_path):
        PYZBAR_BINARIES.append(
            (
                dll_path,
                "pyzbar",
            )
        )


# ============================================================
# Application Data
# ============================================================

DATA_FILES = [
    (
        os.path.join(
            PROJECT_ROOT,
            "assets",
        ),
        "assets",
    ),
]

DATA_FILES += collect_data_files(
    "reportlab"
)


# ============================================================
# Hidden Imports
# ============================================================

HIDDEN_IMPORTS = []

HIDDEN_IMPORTS += collect_submodules(
    "reportlab"
)

HIDDEN_IMPORTS += collect_submodules(
    "pyzbar"
)

HIDDEN_IMPORTS += collect_submodules(
    "websockets"
)


# ============================================================
# Analysis
# ============================================================

a = Analysis(
    [os.path.join(PROJECT_ROOT, ENTRY_POINT)],

    pathex=[
        PROJECT_ROOT,
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
# QuickBill Executable
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

    upx=True,

    upx_exclude=[],

    console=False,

    disable_windowed_traceback=False,

    icon=os.path.join(
        PROJECT_ROOT,
        ICON_FILE,
    ),

    version=os.path.join(
        PROJECT_ROOT,
        VERSION_FILE,
    ),

    uac_admin=False,

    argv_emulation=False,

    target_arch=None,

    codesign_identity=None,

    entitlements_file=None,
)