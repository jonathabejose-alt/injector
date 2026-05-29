# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas    = []
binaries = []
hiddenimports = []

# Collect ALL pynput files (backend dlls, etc)
tmp = collect_all('pynput')
datas    += tmp[0]
binaries += tmp[1]
hiddenimports += tmp[2]

# Collect ALL keyboard files
tmp = collect_all('keyboard')
datas    += tmp[0]
binaries += tmp[1]
hiddenimports += tmp[2]

datas    += [('ui', 'ui'), ('core', 'core'), ('cr.ico', '.'), ('offsets', 'offsets')]

hiddenimports += [
    'pymem', 'pymem.process', 'pymem.pattern',
    'PyQt6', 'PyQt6.QtWidgets', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtSvg',
    'ui', 'ui.gui',
    'core', 'core.app_state', 'core.actions',
    'core.config_manager', 'core.injector', 'core.logger',
    'core.discord_rpc', 'core.lagswitch',
    'pypresence', 'pypresence.presence',
    'PIL', 'PIL.Image',
    'winreg', 'webbrowser',
    'ctypes', 'ctypes.wintypes',
]

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SacredWare',
    debug=False,
    strip=False,
    upx=False,
    console=False,
    icon='cr.ico',
    uac_admin=False,
)
