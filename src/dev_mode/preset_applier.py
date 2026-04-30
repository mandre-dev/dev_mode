"""Aplica um preset: abre IDE, playlist e ajusta brilho."""

import subprocess

from .ide_detector import get_ide_command
from .music_detector import open_playlist
from .brightness_controller import set_brightness


def apply_preset(preset_data):
    """Aplica um preset completo: IDE, playlist e brilho.

    Args:
        preset_data: dict com chaves 'ide', 'playlist', 'brightness'.

    Returns:
        dict com status de cada ação aplicada.
    """
    results = {"ide": False, "playlist": False, "brightness": False}

    ide_name = preset_data.get("ide", "")
    playlist = preset_data.get("playlist", "")
    brightness = preset_data.get("brightness", 100)

    # Abre a IDE
    if ide_name and ide_name != "-- Select IDE --":
        cmd = get_ide_command(ide_name)
        print(f"[DEBUG] Tentando abrir IDE: {cmd}")
        if cmd:
            try:
                subprocess.Popen(
                    [cmd],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                results["ide"] = True
            except Exception as e:
                print(f"[Aviso] Não foi possível abrir a IDE '{ide_name}': {e}")
        else:
            print(
                f"[Aviso] Caminho da IDE '{ide_name}' não encontrado. Verifique se está instalada e no PATH."
            )

    # Abre a playlist / app de música
    if playlist:
        try:
            open_playlist(playlist)
            results["playlist"] = True
        except Exception:
            pass

    # Ajusta o brilho
    try:
        set_brightness(brightness)
        results["brightness"] = True
    except Exception:
        pass

    return results
