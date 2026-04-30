# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['../src/dev_mode/__main__.py'],
    pathex=['../src'],
    binaries=[],
    datas=[
        ('../src/dev_mode/assets', 'assets'),
        ('../src/dev_mode/fonts', 'fonts'),
    ],
    hiddenimports=['PIL', 'PIL.Image', 'PIL.ImageDraw', 'PIL.ImageFont', 'dev_mode', 'dev_mode.app'],
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
    a.binaries,
    a.datas,
    [],
    name='dev_mode',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)