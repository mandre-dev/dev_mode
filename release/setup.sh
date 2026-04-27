#!/usr/bin/env bash
# setup.sh — Configura o Dev Mode na máquina do usuário
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DESKTOP_FILE="$SCRIPT_DIR/Dev Mode.desktop"

echo "⚙️  Configurando Dev Mode..."

# Permissões
chmod +x "$SCRIPT_DIR/dev_mode"
chmod +x "$SCRIPT_DIR/launch_dev_mode.sh"

# Cria o .desktop com caminhos absolutos
cat > "$DESKTOP_FILE" <<DESKTOP
[Desktop Entry]
Name=Dev Mode
Comment=Apply development presets: IDE, music and brightness
Exec=$SCRIPT_DIR/launch_dev_mode.sh
Icon=$SCRIPT_DIR/dev-mode.png
Type=Application
Categories=Development;Utility;
Terminal=false
StartupNotify=true
DESKTOP

chmod +x "$DESKTOP_FILE"

# Marca como confiável para o GNOME (evita o aviso de segurança)
gio set "$DESKTOP_FILE" metadata::trusted true 2>/dev/null && \
    echo "✅ Marcado como confiável no GNOME." || \
    echo "⚠️  Não foi possível marcar como confiável automaticamente."

echo "✅ Pronto! Agora dê duplo clique em 'Dev Mode.desktop' para abrir o Dev Mode."