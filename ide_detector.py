"""Detecção de IDEs instaladas no sistema."""

import subprocess

# Lista de comandos e nomes de IDEs populares
IDE_COMMANDS = [
    ("code", "VS Code"),
    ("codium", "VSCodium"),
    ("pycharm", "PyCharm"),
    ("idea", "IntelliJ IDEA"),
    ("subl", "Sublime Text"),
    ("atom", "Atom"),
    ("gedit", "Gedit"),
    ("kate", "Kate"),
    ("geany", "Geany"),
    ("emacs", "Emacs"),
    ("vim", "Vim"),
    ("nano", "Nano"),
]


def detect_ides():
    """Detecta IDEs instaladas e retorna uma lista com os nomes."""
    ides = []
    for cmd, name in IDE_COMMANDS:
        if (
            subprocess.call(
                ["which", cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            == 0
        ):
            ides.append(name)
    return ides if ides else ["None found"]
