# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

project_root = Path.cwd()

datas = [
    (str(project_root / "config"), "config"),
    (str(project_root / "assets"), "assets"),
    (str(project_root / ".env.example"), "."),
]

a = Analysis(
    ["main.py"],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="TaskAutomationApp",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="TaskAutomationApp",
)
