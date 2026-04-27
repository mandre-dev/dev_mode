#!/usr/bin/env bash
# setup.sh — Configura o Dev Mode na máquina do usuário
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DESKTOP_FILE="$SCRIPT_DIR/Dev_Mode.desktop"

echo "⚙️  Configurando Dev Mode..."

# Permissões
chmod +x "$SCRIPT_DIR/dev_mode"
chmod +x "$SCRIPT_DIR/launch_dev_mode.sh"

# Cria o .desktop com caminhos absolutos (usando aspas para evitar erro com espaços)
cat > "$DESKTOP_FILE" <<DESKTOP
[Desktop Entry]
Name=Dev Mode
Comment=Apply development presets: IDE, music and brightness
Exec="$SCRIPT_DIR/launch_dev_mode.sh"
Icon="$SCRIPT_DIR/dev-mode.png"
Type=Application
Categories=Development;Utility;
Terminal=false
StartupNotify=true
DESKTOP

chmod +x "$DESKTOP_FILE"

# Marca como confiável para o GNOME/Cinnamon
gio set "$DESKTOP_FILE" metadata::trusted true 2>/dev/null && \
    echo "✅ Marcado como confiável no sistema." || \
    echo "⚠️  Não foi possível marcar como confiável automaticamente (você pode precisar fazer isso manualmente)."

echo "✅ Pronto! Agora dê duplo clique em 'Dev_Mode.desktop' para abrir o Dev Mode."