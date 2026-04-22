import subprocess
import webbrowser
import os
import sys
import platform


# Caminho para o VS Code
def get_vscode_cmd():
    if os.name == "nt":
        # Windows: tente localizar o executável do VS Code
        return r"C:\\Program Files\\Microsoft VS Code\\Code.exe"
    else:
        return "code"


# URL da playlist (exemplo YouTube Music)
PLAYLIST_URL = (
    "https://music.youtube.com/playlist?list=PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI"
)


# Função para abrir o VS Code
def abrir_vscode():
    try:
        vscode_cmd = get_vscode_cmd()
        if os.name == "nt":
            subprocess.Popen([vscode_cmd])
        else:
            subprocess.Popen([vscode_cmd])
    except Exception as e:
        print(f"Erro ao abrir VS Code: {e}")


# Função para abrir a playlist no navegador
def abrir_playlist():
    try:
        webbrowser.open(PLAYLIST_URL)
    except Exception as e:
        print(f"Erro ao abrir playlist: {e}")


# Função para diminuir o brilho do monitor em 10%
def diminuir_brilho():
    try:
        if os.name == "nt":
            # Windows: usar screen-brightness-control
            try:
                import screen_brightness_control as sbc
            except ImportError:
                print(
                    "Instale a biblioteca 'screen-brightness-control' com: pip install screen-brightness-control"
                )
                return
            brilho_atual = sbc.get_brightness(display=0)[0]
            novo_brilho = max(10, int(brilho_atual - 10))
            sbc.set_brightness(novo_brilho, display=0)
        else:
            # Linux: usar xrandr
            output = subprocess.check_output(["xrandr", "--current"]).decode()
            for line in output.splitlines():
                if " connected" in line:
                    display = line.split()[0]
                    break
            else:
                print("Nenhum monitor detectado.")
                return
            brilho_atual = float(
                subprocess.check_output(["xrandr", "--verbose"])
                .decode()
                .split("Brightness:")[1]
                .split()[0]
            )
            novo_brilho = max(0.1, brilho_atual - 0.1)
            subprocess.call(
                ["xrandr", "--output", display, "--brightness", str(novo_brilho)]
            )
    except Exception as e:
        print(f"Erro ao ajustar brilho: {e}")


if __name__ == "__main__":
    abrir_vscode()
    abrir_playlist()
    diminuir_brilho()
