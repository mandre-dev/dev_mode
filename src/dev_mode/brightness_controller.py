"""Controle de brilho do monitor.

- Linux: tenta via `xrandr --brightness` (X11).
- Windows: tenta via PowerShell/WMI (monitores internos/compatíveis).

Observação: em alguns ambientes (Wayland, monitores externos, drivers específicos),
ajuste de brilho pode não estar disponível; nesses casos, a função falha em silêncio.
"""

import platform
import re
import subprocess


def _linux_get_displays():
    """Retorna a lista de displays conectados (Linux/X11 via xrandr)."""
    try:
        output = subprocess.check_output(["xrandr"], text=True)
        displays = []
        for line in output.splitlines():
            if " connected " in line:
                match = re.match(r"(\S+)\s+connected", line)
                if match:
                    displays.append(match.group(1))
        return displays
    except Exception:
        return []


def _linux_set_brightness(percent):
    """Define brilho (0-100%) via xrandr (Linux/X11)."""
    value = max(10, min(100, int(percent))) / 100.0
    displays = _linux_get_displays()
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


def _windows_set_brightness(percent):
    """Define brilho (0-100%) via PowerShell/WMI (Windows)."""
    value = max(0, min(100, int(percent)))
    ps = (
        "$b=%d;"
        "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods)"
        " | ForEach-Object { try { $_.WmiSetBrightness(1,$b) | Out-Null } catch {} }"
    ) % value
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            text=True,
        )
        if result.returncode != 0:
            print("[Aviso] Não foi possível ajustar o brilho no Windows. Pode ser necessário executar como administrador ou o monitor não é compatível.")
    except Exception as e:
        print(f"[Erro] Falha ao tentar ajustar brilho no Windows: {e}")


def set_brightness(percent):
    """Define o brilho do monitor (0-100%), quando suportado pelo SO."""
    system = platform.system()
    if system == "Windows":
        _windows_set_brightness(percent)
        return
    if system == "Linux":
        _linux_set_brightness(percent)
        return
    print("[Aviso] Ajuste de brilho não suportado neste sistema.")
    return
