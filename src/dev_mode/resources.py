import os
import sys


def resource_path(*parts: str) -> str:
    """Resolve paths para assets/fonts, compatível com PyInstaller e execução normal."""
    if getattr(sys, 'frozen', False):
        # Rodando como executável PyInstaller — arquivos estão em sys._MEIPASS
        base_dir = sys._MEIPASS
    else:
        # Rodando normalmente como script Python
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, *parts)