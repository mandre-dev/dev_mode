"""Detecção de IDEs instaladas no sistema."""

import os
import platform
import shutil

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

# Mapeamento nome -> comando para fácil lookup
IDE_NAME_TO_CMD = {name: cmd for cmd, name in IDE_COMMANDS}

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
        return shutil.which(cmd) is not None
    except Exception:
        return False


def _find_in_extra_paths(cmd):
    """Procura o executável em caminhos alternativos comuns."""
    # Windows: além do PATH, tenta locais comuns de instalação
    if platform.system() == "Windows":
        candidates = []
        program_files = os.environ.get("ProgramFiles")
        program_files_x86 = os.environ.get("ProgramFiles(x86)")
        local_appdata = os.environ.get("LOCALAPPDATA")
        user_profile = os.environ.get("USERPROFILE")

        # Busca em possíveis subpastas de IDEs
        ide_dirs = [program_files, program_files_x86, local_appdata, user_profile]
        subfolders = [
            "Microsoft VS Code",
            "JetBrains\\PyCharm Community Edition 2023.1\\bin",
            "JetBrains\\IntelliJ IDEA Community Edition 2023.1\\bin",
            "JetBrains\\CLion 2023.1\\bin",
            "JetBrains\\Rider 2023.1\\bin",
            "Sublime Text",
            "AppData\\Local\\Programs\\Microsoft VS Code",
        ]
        for base in ide_dirs:
            if base:
                for sub in subfolders:
                    path = os.path.join(base, *sub.split("\\"))
                    exe = os.path.join(path, f"{cmd}.exe")
                    if os.path.isfile(exe):
                        return exe
        # Se o "cmd" já for um .exe conhecido, tenta localizar diretamente.
        if cmd.lower().endswith(".exe"):
            if os.path.isfile(cmd):
                return cmd

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
    if platform.system() == "Windows" and not ides:
        print("[Aviso] Nenhuma IDE detectada automaticamente no Windows. Adicione ao PATH ou instale em local padrão.")
    return ides if ides else ["None found"]


def get_ide_command(ide_name):
    """Retorna o caminho completo do executável para uma IDE, se encontrado, ou o comando se estiver no PATH."""
    cmd = IDE_NAME_TO_CMD.get(ide_name)
    if not cmd:
        return None
    # Se estiver no PATH, retorna só o comando
    if _is_command_available(cmd):
        return cmd
    # Se encontrar em caminhos alternativos, retorna o caminho completo
    found = _find_in_extra_paths(cmd)
    if isinstance(found, str):
        return found
    # Se não encontrou, retorna o comando (pode falhar)
    return cmd
