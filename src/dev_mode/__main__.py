import sys
import os

# Necessário para o PyInstaller encontrar o pacote corretamente
if getattr(sys, 'frozen', False):
    # Rodando como executável PyInstaller
    sys.path.insert(0, os.path.dirname(sys.executable))
else:
    # Rodando normalmente como script
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dev_mode.app import DevModeApp


def main():
    app = DevModeApp()
    app.run()


if __name__ == "__main__":
    main()