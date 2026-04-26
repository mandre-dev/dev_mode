"""Renderiza texto com fontes TTF customizadas para uso no tkinter."""

import os
import io
import base64
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
from .resources import resource_path


def _pil_to_photoimage(pil_img):
    """Converte uma imagem PIL para tkinter.PhotoImage sem ImageTk."""
    # Salva em formato PNG na memória
    buffer = io.BytesIO()
    pil_img.save(buffer, format="PNG")
    buffer.seek(0)
    # Codifica em base64 para PhotoImage
    b64 = base64.b64encode(buffer.read()).decode("utf-8")
    return tk.PhotoImage(data=b64)


def render_text_image(text, font_path, font_size, color, bg_color=None):
    """Renderiza texto em uma imagem PIL e retorna PhotoImage do tkinter.

    Args:
        text: Texto a renderizar.
        font_path: Caminho para o arquivo .ttf.
        font_size: Tamanho da fonte em pixels.
        color: Cor do texto (hex ou tupla RGB).
        bg_color: Cor de fundo (None = transparente).

    Returns:
        tkinter.PhotoImage pronta para usar em Labels.
    """
    # Carrega a fonte
    font = ImageFont.truetype(font_path, font_size)

    # Calcula o tamanho do texto
    bbox = font.getbbox(text)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]

    # Adiciona padding
    padding_x = 4
    padding_y = 2
    img_width = width + padding_x * 2
    img_height = height + padding_y * 2

    # Cria a imagem
    if bg_color:
        img = Image.new("RGBA", (img_width, img_height), bg_color)
    else:
        img = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))

    draw = ImageDraw.Draw(img)
    draw.text((padding_x, padding_y), text, font=font, fill=color)

    return _pil_to_photoimage(img)


def get_font_path(filename):
    """Retorna o caminho completo para um arquivo de fonte no diretório fonts/."""
    return resource_path("fonts", filename)
