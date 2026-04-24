"""Controle de brilho do monitor via xrandr."""

import subprocess
import re


def get_displays():
    """Retorna a lista de displays conectados."""
    try:
        output = subprocess.check_output(["xrandr"], text=True)
        displays = []
        for line in output.splitlines():
            if " connected " in line:
                match = re.match(r"(\S+)\s+connected", line)
                if match:
                    displays.append(match.group(1))
        return displays if displays else ["default"]
    except Exception:
        return ["default"]


def set_brightness(percent):
    """Define o brilho do monitor (0-100%)."""
    value = max(10, min(100, percent)) / 100.0
    displays = get_displays()
    for display in displays:
        try:
            subprocess.run(
                ["xrandr", "--output", display, "--brightness", str(value)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        except Exception:
            pass
