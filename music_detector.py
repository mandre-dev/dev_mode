"""Detecção de apps de música instalados no sistema."""

import subprocess

MUSIC_COMMANDS = [
    ("spotify", "Spotify"),
    ("rhythmbox", "Rhythmbox"),
    ("audacious", "Audacious"),
    ("clementine", "Clementine"),
    ("amarok", "Amarok"),
    ("deadbeef", "DeaDBeeF"),
    ("lollypop", "Lollypop"),
]


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
