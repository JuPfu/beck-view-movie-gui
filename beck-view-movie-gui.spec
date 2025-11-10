# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
from PyInstaller.building.datastruct import TOC
from PyInstaller.utils.hooks import collect_dynamic_libs

# Path to your project
project_dir = Path.cwd()
dist_dir = Path("./dist")

# Collect all .so files from the dist/ directory
cython_so_files = [
    (str(f), '.') for f in dist_dir.glob("*.so")
]
print(f"Found following *.so files {cython_so_files}")

# Optional: Include compiled shared libraries from some packages
# e.g. numpy, if needed
# numpy_binaries = collect_dynamic_libs("numpy")

a = Analysis(
    ['beck_view_movie_gui.py'],  # your stub that imports main
    pathex=[str(project_dir)],
    binaries=cython_so_files,
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='beck-view-movie-gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # change to False if you want a GUI app
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="C:\\Users\\Peter lokal\\PycharmProjects\\beck-view-movie-gui\\beck-view-movie-logo.png"
)


coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='beck-view-movie-gui-bundle'
)
