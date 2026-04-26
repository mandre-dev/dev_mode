"""Configurações e constantes do Dev_Mode."""

import os

# Cores
colors = {
    "bg": "#101820",
    "accent": "#00AEEF",
    "title_dev": "#00AEEF",
    "title_underscore": "#FFFFFF",
    "title_mode": "#FFD700",
    "text_light": "#FFFFFF",
    "text_dark": "#333333",
    "btn_bg": "#101820",
    "btn_cancel": "#D32F2F",
    "btn_cancel_active": "#B71C1C",
    "btn_clean": "#333333",
    "btn_clean_active": "#555555",
    "shadow": "#B8860B",
    "shadow_hover": "#8B6914",
    "yellow": "#FFD700",
    "yellow_hover": "#FFE135",
    "apply_bg": "#00AEEF",
    "apply_bg_hover": "#008BC7",
    "warning": "#FFD700",
    "error_bg": "#FFD2D2",
    "success_bg": "#D2FFD2",
}

# Fontes
FONTS = {
    "title": ("Press Start 2P", 18),
    "default": ("JetBrains Mono", 12),
    "default_bold": ("JetBrains Mono", 12, "bold"),
    "banner": ("JetBrains Mono", 13, "bold"),
    "status": ("JetBrains Mono", 10, "bold"),
    "warning": ("JetBrains Mono", 10, "bold"),
}

# Fonte fallback se JetBrains Mono não estiver disponível
FALLBACK_FONT = ("Noto Sans Mono", 12)

# Caminho do arquivo de presets
PRESETS_FILE = os.path.join(os.path.expanduser("~"), ".dev_mode_presets.json")

# Dimensões da janela
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 250

# Tamanho alvo para ícones
ICON_TARGET_SIZE = 20
