"""Componentes de UI reutilizáveis."""

import tkinter as tk
from tkinter import PhotoImage
from config import ICON_TARGET_SIZE, colors, FONTS


class ToolTip:
    """Tooltip que aparece ao passar o mouse sobre um widget."""

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tooltip_window:
            return
        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() - 22
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw,
            text=self.text,
            font=FONTS["default"],
            fg=colors["text_light"],
            bg=colors["text_dark"],
            bd=1,
            relief="solid",
            padx=4,
            pady=2,
        )
        label.pack()

    def hide(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


def load_icon(path):
    """Carrega uma imagem PNG e a redimensiona proporcionalmente."""
    try:
        icon = PhotoImage(file=path)
        factor = max(1, icon.width() // ICON_TARGET_SIZE)
        if factor > 1:
            icon = icon.subsample(factor, factor)
        return icon
    except Exception:
        return None


def create_icon_button(parent, image_path, text_fallback, command=None):
    """Cria um botão com ícone ou texto de fallback."""
    icon = load_icon(image_path)
    if icon:
        btn = tk.Button(
            parent,
            image=icon,
            bg=colors["btn_bg"],
            bd=0,
            activebackground=colors["btn_bg"],
            command=command,
        )
        btn.image = icon
    else:
        btn = tk.Button(
            parent,
            text=text_fallback,
            bg=colors["btn_bg"],
            fg=colors["accent"],
            bd=0,
            activebackground=colors["btn_bg"],
            command=command,
        )
    return btn


def create_shadow_button(parent, width, height, text, click_command=None):
    """Cria um botão customizado com sombra de texto em Canvas."""
    canvas = tk.Canvas(
        parent,
        width=width,
        height=height,
        bg=colors["apply_bg"],
        highlightthickness=1,
        highlightbackground=colors["text_light"],
        cursor="hand2",
    )
    # Sombra
    shadow_id = canvas.create_text(
        width // 2 + 1,
        height // 2 + 1,
        text=text,
        font=FONTS["default_bold"],
        fill="#000000",
    )
    # Texto principal
    text_id = canvas.create_text(
        width // 2,
        height // 2,
        text=text,
        font=FONTS["default_bold"],
        fill=colors["yellow"],
    )

    def on_enter(event):
        canvas.config(bg=colors["apply_bg_hover"])
        canvas.itemconfig(shadow_id, fill="#000000")
        canvas.itemconfig(text_id, fill=colors["yellow_hover"])

    def on_leave(event):
        canvas.config(bg=colors["apply_bg"])
        canvas.itemconfig(shadow_id, fill="#000000")
        canvas.itemconfig(text_id, fill=colors["yellow"])

    def on_click(event):
        if click_command:
            click_command()

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.bind("<Button-1>", on_click)
    return canvas
