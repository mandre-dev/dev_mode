#!/usr/bin/env python3
"""Build script: gera executável standalone do Dev_Mode via PyInstaller."""

import os
import subprocess
import sys


def main():
    # Verifica se pyinstaller está instalado
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller não encontrado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Paths
    root = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(root, "src")
    main_script = os.path.join(src_dir, "dev_mode", "__main__.py")
    assets_dir = os.path.join(src_dir, "dev_mode", "assets")
