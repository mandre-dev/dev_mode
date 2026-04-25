"""Detecção de apps de música instalados no sistema."""

import subprocess
import webbrowser

MUSIC_COMMANDS = [
    ("spotify", "Spotify"),
    ("rhythmbox", "Rhythmbox"),
    ("audacious", "Audacious"),
    ("clementine", "Clementine"),
    ("amarok", "Amarok"),
    ("deadbeef", "DeaDBeeF"),
    ("lollypop", "Lollypop"),
]

# Mapeamento nome -> comando
MUSIC_NAME_TO_CMD = {name: cmd for cmd, name in MUSIC_COMMANDS}


def detect_music_apps():
    """Detecta apps de música instalados."""
    apps = []
    for cmd, name in MUSIC_COMMANDS:
        if (
            subprocess.call(
                ["which", cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            == 0
        ):
            apps.append(name)
    return apps if apps else []


def get_music_command(app_name):
    """Retorna o comando executável para um app de música pelo nome."""
    return MUSIC_NAME_TO_CMD.get(app_name)


def open_playlist(playlist_value):
    """Abre uma playlist — app de música ou URL no navegador."""
    if not playlist_value:
        return

    # Se for URL (começa com http), abre no navegador
    if playlist_value.startswith(("http://", "https://")):
        webbrowser.open(playlist_value)
        return

    # Se for um app de música conhecido, tenta abrir
    cmd = get_music_command(playlist_value)
    if cmd:
        try:
            subprocess.Popen(
                [cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except Exception:
            pass
