"""Renderizador de labels com fonte customizada via PIL."""

import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
from .font_renderer import get_font_path, _pil_to_photoimage


# Cache de imagens de label para evitar recriação
def _get_jetbrains_font(size=12, bold=False):
    """Carrega a fonte JetBrains Mono ExtraBold para todos os textos."""
    font_path = get_font_path("JetBrainsMono-ExtraBold.ttf")
    try:
        return ImageFont.truetype(font_path, size)
    except Exception:
        # Fallback se não encontrar a fonte
        return ImageFont.load_default()


def create_rendered_label(
    parent,
    text,
    font_size=12,
    fg_color="#FFFFFF",
    bg_color="#101820",
    bold=False,
    **kwargs,
):
    """
    Cria um tk.Label com texto renderizado via PIL usando JetBrains Mono.
    Retorna o widget Label e armazena a referência da imagem nele.
    """
    font = _get_jetbrains_font(font_size, bold)

    # Calcula bounds do texto
    bbox = font.getbbox(text)
    width = bbox[2] - bbox[0] + 8  # Padding horizontal
    height = bbox[3] - bbox[1] + 6  # Padding vertical

    # Cria imagem com fundo
    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Desenha o texto com padding
    x = 4 - bbox[0]
    y = 3 - bbox[1]

    # Se bold, desenha com outline
    if bold:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0, 128))

    draw.text((x, y), text, font=font, fill=fg_color)

    # Converte para PhotoImage
    photo = _pil_to_photoimage(img)

    # Cria o label com a imagem
    label = tk.Label(parent, image=photo, bg=bg_color, **kwargs)
    label._rendered_image = photo  # Manter referência

    return label


def update_rendered_label(
    label, text, font_size=12, fg_color="#FFFFFF", bg_color="#101820", bold=False
):
    """Atualiza o texto de um label renderizado."""
    font = _get_jetbrains_font(font_size, bold)

    bbox = font.getbbox(text)
    width = bbox[2] - bbox[0] + 8
    height = bbox[3] - bbox[1] + 6

    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    x = 4 - bbox[0]
    y = 3 - bbox[1]

    if bold:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0, 128))

    draw.text((x, y), text, font=font, fill=fg_color)

    photo = _pil_to_photoimage(img)
    label.config(image=photo)
    label._rendered_image = photo
    return label
