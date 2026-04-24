"""Detecção de IDEs instaladas no sistema."""

import os
import subprocess

# Lista de comandos e nomes de IDEs populares
IDE_COMMANDS = [
    ("code", "VS Code"),
    ("code-insiders", "VS Code Insiders"),
    ("cursor", "Cursor"),
    ("windsurf", "Windsurf"),
    ("zed", "Zed"),
    ("fleet", "JetBrains Fleet"),
    ("codium", "VSCodium"),
    ("pycharm", "PyCharm"),
    ("pycharm-community", "PyCharm Community"),
    ("idea", "IntelliJ IDEA"),
    ("idea-community", "IntelliJ IDEA Community"),
    ("phpstorm", "PhpStorm"),
    ("webstorm", "WebStorm"),
    ("clion", "CLion"),
    ("rider", "Rider"),
    ("goland", "GoLand"),
    ("rubymine", "RubyMine"),
    ("datagrip", "DataGrip"),
    ("android-studio", "Android Studio"),
    ("subl", "Sublime Text"),
    ("sublime_text", "Sublime Text"),
    ("atom", "Atom"),
    ("gedit", "Gedit"),
    ("kate", "Kate"),
    ("geany", "Geany"),
    ("emacs", "Emacs"),
    ("vim", "Vim"),
    ("nvim", "Neovim"),
    ("nano", "Nano"),
    ("micro", "Micro"),
    ("lapce", "Lapce"),
    ("helix", "Helix"),
    ("oni", "Oni"),
    ("oni2", "Oni 2"),
]

# Caminhos alternativos onde IDEs podem estar instaladas (snap, flatpak, appimages, etc.)
EXTRA_PATHS = [
    "/usr/bin",
    "/usr/local/bin",
    "/opt",
    "/snap/bin",
    os.path.expanduser("~/.local/bin"),
    os.path.expanduser("~/AppImage"),
    os.path.expanduser("~/.cursor"),
    os.path.expanduser("~/.windsurf"),
    "/var/lib/flatpak/exports/bin",
    os.path.expanduser("~/.local/share/flatpak/exports/bin"),
]


def _is_command_available(cmd):
    """Verifica se um comando existe no PATH."""
    try:
        result = subprocess.run(
            ["which", cmd],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except Exception:
        return False


def _find_in_extra_paths(cmd):
    """Procura o executável em caminhos alternativos comuns."""
    for base in EXTRA_PATHS:
        if not os.path.exists(base):
            continue
        # Procura arquivo executável com o nome exato
        full_path = os.path.join(base, cmd)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return True
        # Se for diretório, procura recursivamente (1 nível)
        if os.path.isdir(base):
            for entry in os.listdir(base):
                if entry.lower() == cmd.lower():
                    candidate = os.path.join(base, entry)
                    if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                        return True
                # Verifica subdiretórios conhecidos (ex: /opt/cursor/)
                subdir = os.path.join(base, entry)
                if os.path.isdir(subdir):
                    candidate = os.path.join(subdir, cmd)
                    if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                        return True
    return False


def detect_ides():
    """Detecta IDEs instaladas e retorna uma lista com os nomes."""
    ides = []
    seen = set()
    for cmd, name in IDE_COMMANDS:
        if name in seen:
            continue
        if _is_command_available(cmd) or _find_in_extra_paths(cmd):
            ides.append(name)
            seen.add(name)
    return ides if ides else ["None found"]
