#!/usr/bin/env bash
# setup.sh — Configura o Dev Mode na máquina do usuário
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "⚙️  Configurando Dev Mode..."

# Permissões
chmod +x "$SCRIPT_DIR/dev_mode"
chmod +x "$SCRIPT_DIR/launch_dev_mode.sh"

# Cria o .desktop com caminhos absolutos
cat > "$SCRIPT_DIR/dev_mode.desktop" <<EOF
[Desktop Entry]
Name=Dev Mode
Comment=Apply development presets: IDE, music and brightness
Exec=$SCRIPT_DIR/launch_dev_mode.sh
Icon=$SCRIPT_DIR/dev-mode.png
Type=Application
Categories=Development;Utility;
Terminal=false
StartupNotify=true
EOF

chmod +x "$SCRIPT_DIR/dev_mode.desktop"

echo "✅ Pronto! Agora dê duplo clique em dev_mode.desktop para abrir o Dev Mode."