#!/usr/bin/env python3
"""
Gera uma imagem preview da interface Dev Mode.

Uso:
    python3 preview.py          # Gera preview.png da tela principal
    python3 preview.py --add    # Gera preview_add.png da tela de adicionar

Requisitos:
    - Rodar em ambiente com display gráfico (não funciona em headless)
    - pip install pillow
"""

import argparse
import os
import sys
import time

# Garante que PIL está disponível
try:
    from PIL import Image
except ImportError:
    print("Instalando pillow...")
    os.system("pip install pillow --break-system-packages --quiet")
    from PIL import Image


def capture_tk_window(root, output_path):
    """Captura screenshot da janela tkinter usando PIL."""
    root.update_idletasks()
    root.update()
    time.sleep(0.3)  # Espera renderizar

    # Coordenadas da janela
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    width = root.winfo_width()
    height = root.winfo_height()

    # Usa PIL para capturar
    try:
        from PIL import ImageGrab

        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        screenshot.save(output_path)
        print(f"✅ Preview salvo em: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Erro ao capturar: {e}")
        print("💡 Dica: Este script precisa rodar em ambiente com display gráfico.")
        return False


def preview_main_screen():
    """Gera preview da tela principal."""
    from app import DevModeApp

    app = DevModeApp()
    success = capture_tk_window(app.root, "preview_main.png")
    app.root.destroy()
    return success


def preview_add_screen():
    """Gera preview da tela de adicionar preset."""
    from app import DevModeApp

    app = DevModeApp()
    # Navega para tela de adicionar
    app._build_add_screen()
    app.root.update_idletasks()
    app.root.update()

    success = capture_tk_window(app.root, "preview_add.png")
    app.root.destroy()
    return success


def main():
    parser = argparse.ArgumentParser(description="Preview generator for Dev Mode")
    parser.add_argument(
        "--add", action="store_true", help="Gera preview da tela de adicionar preset"
    )
    args = parser.parse_args()

    if args.add:
        success = preview_add_screen()
    else:
        success = preview_main_screen()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
