#!/usr/bin/env bash
# setup.sh — Configura o Dev Mode na máquina do usuário
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DESKTOP_FILE="Dev_Mode.desktop"
LOCAL_APPS="$HOME/.local/share/applications"
LOCAL_ICONS="$HOME/.local/share/icons"

echo "⚙️  Configurando Dev Mode no sistema..."

# 1. Garante que as pastas do sistema do usuário existam
mkdir -p "$LOCAL_APPS"
mkdir -p "$LOCAL_ICONS"

# 2. Permissões nos binários
chmod +x "$SCRIPT_DIR/dev_mode"
chmod +x "$SCRIPT_DIR/launch_dev_mode.sh"

# 3. Copia o ícone para a pasta de ícones do sistema (isso ajuda o painel a achar a imagem)
cp "$SCRIPT_DIR/dev-mode.png" "$LOCAL_ICONS/dev-mode.png"

# 4. Cria o arquivo .desktop direto na pasta de aplicações do sistema
cat > "$LOCAL_APPS/$DESKTOP_FILE" <<EOF
[Desktop Entry]
Name=Dev Mode
Comment=Apply development presets
Exec="$SCRIPT_DIR/launch_dev_mode.sh"
Icon=dev-mode
Type=Application
Categories=Development;
Terminal=false
StartupNotify=true
StartupWMClass=Dev_Mode
EOF

# 5. Dá permissão e atualiza o banco de dados de atalhos
chmod +x "$LOCAL_APPS/$DESKTOP_FILE"
update-desktop-database "$LOCAL_APPS"

echo "✅ Instalação concluída!"
echo "👉 Procure por 'Dev Mode' no seu menu de aplicativos (Iniciar) e abra por lá."
Type=Application
Categories=Development;Utility;
Terminal=false
StartupNotify=true
StartupWMClass=Tk
DESKTOP

chmod +x "$DESKTOP_FILE"

# Marca como confiável para o GNOME/Cinnamon
gio set "$DESKTOP_FILE" metadata::trusted true 2>/dev/null && \
    echo "✅ Marcado como confiável no sistema." || \
    echo "⚠️  Não foi possível marcar como confiável automaticamente (você pode precisar fazer isso manualmente)."

echo "✅ Pronto! Agora dê duplo clique em 'Dev_Mode.desktop' para abrir o Dev Mode."