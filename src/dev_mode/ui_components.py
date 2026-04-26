"""Componentes de UI reutilizáveis."""

import tkinter as tk
from tkinter import PhotoImage
from .config import ICON_TARGET_SIZE, colors, FONTS
from .resources import resource_path


def _hex_to_rgb(value: str):
    value = value.lstrip("#")
    if len(value) != 6:
        raise ValueError("Expected #RRGGBB")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb):
    r, g, b = (max(0, min(255, int(v))) for v in rgb)
    return f"#{r:02x}{g:02x}{b:02x}"


def _lerp(a, b, t: float):
    return a + (b - a) * t


def _lerp_color(c1: str, c2: str, t: float):
    r1, g1, b1 = _hex_to_rgb(c1)
    r2, g2, b2 = _hex_to_rgb(c2)
    return _rgb_to_hex((_lerp(r1, r2, t), _lerp(g1, g2, t), _lerp(b1, b2, t)))


def _animate(widget, steps, update_fn, duration_ms=150):
    """Pequena engine de animação baseada em `after`."""
    if hasattr(widget, "_hover_anim_after_id"):
        try:
            widget.after_cancel(widget._hover_anim_after_id)
        except Exception:
            pass
        widget._hover_anim_after_id = None

    if steps <= 0:
        update_fn(1.0)
        return

    interval = max(10, duration_ms // steps)

    def tick(i=0):
        t = i / steps
        update_fn(t)
        if i >= steps:
            widget._hover_anim_after_id = None
            return
        widget._hover_anim_after_id = widget.after(interval, lambda: tick(i + 1))

    tick(0)


def attach_hover_animation_button(
    btn,
    normal_bg,
    hover_bg,
    normal_fg=None,
    hover_fg=None,
    normal_border=None,
    hover_border=None,
    duration_ms=150,
    steps=8,
):
    """Anima hover/leave em tk.Button (transição suave de cor)."""
    def set_state(t, bg_from, bg_to, fg_from, fg_to, br_from, br_to):
        bg = _lerp_color(bg_from, bg_to, t)
        try:
            btn.configure(bg=bg, activebackground=bg)
        except Exception:
            pass
        if fg_from is not None and fg_to is not None:
            fg = _lerp_color(fg_from, fg_to, t)
            try:
                btn.configure(fg=fg, activeforeground=fg)
            except Exception:
                pass
        if br_from is not None and br_to is not None:
            br = _lerp_color(br_from, br_to, t)
            try:
                btn.configure(highlightthickness=1, highlightbackground=br)
            except Exception:
                pass

    def on_enter(_=None):
        _animate(
            btn,
            steps,
            lambda t: set_state(
                t,
                normal_bg,
                hover_bg,
                normal_fg,
                hover_fg,
                normal_border,
                hover_border,
            ),
            duration_ms=duration_ms,
        )

    def on_leave(_=None):
        _animate(
            btn,
            steps,
            lambda t: set_state(
                t,
                hover_bg,
                normal_bg,
                hover_fg,
                normal_fg,
                hover_border,
                normal_border,
            ),
            duration_ms=duration_ms,
        )

    btn.bind("<Enter>", on_enter, add=True)
    btn.bind("<Leave>", on_leave, add=True)
    return btn


def attach_hover_animation_canvas(
    canvas,
    text_id,
    normal_bg,
    hover_bg,
    normal_text,
    hover_text,
    duration_ms=150,
    steps=8,
):
    """Anima hover/leave em Canvas (bg + cor do texto)."""
    def set_state(t, bg_from, bg_to, tx_from, tx_to):
        bg = _lerp_color(bg_from, bg_to, t)
        tx = _lerp_color(tx_from, tx_to, t)
        try:
            canvas.configure(bg=bg)
        except Exception:
            pass
        try:
            canvas.itemconfig(text_id, fill=tx)
        except Exception:
            pass

    def on_enter(_=None):
        _animate(
            canvas,
            steps,
            lambda t: set_state(t, normal_bg, hover_bg, normal_text, hover_text),
            duration_ms=duration_ms,
        )

    def on_leave(_=None):
        _animate(
            canvas,
            steps,
            lambda t: set_state(t, hover_bg, normal_bg, hover_text, normal_text),
            duration_ms=duration_ms,
        )

    canvas.bind("<Enter>", on_enter, add=True)
    canvas.bind("<Leave>", on_leave, add=True)
    return canvas


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
        # Permite passar apenas o nome do arquivo (ex.: "editar.png").
        # Resolve automaticamente para `assets/` dentro do pacote.
        icon_path = path if isinstance(path, str) else str(path)
        # Se o caller passar só "editar.png", resolve em assets/.
        # Se passar um path com separador, assume que já é um caminho.
        if "/" not in icon_path and "\\" not in icon_path:
            icon_path = resource_path("assets", icon_path)
        icon = PhotoImage(file=icon_path)
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
    # Hover suave para botões de ícone/texto.
    normal_fg = btn.cget("fg") if not icon else None
    attach_hover_animation_button(
        btn,
        normal_bg=colors["btn_bg"],
        hover_bg=colors["apply_bg_hover"],
        normal_fg=normal_fg,
        hover_fg=colors["text_light"] if not icon else None,
        # Para botões com ícone, a borda ajuda a deixar o hover visível.
        normal_border=colors["btn_bg"],
        hover_border=colors["accent"],
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
        pass

    def on_leave(event):
        pass

    def on_click(event):
        if click_command:
            click_command()

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.bind("<Button-1>", on_click)
    # Hover suave (bg + texto); sombra fica constante.
    attach_hover_animation_canvas(
        canvas,
        text_id=text_id,
        normal_bg=colors["apply_bg"],
        hover_bg=colors["apply_bg_hover"],
        normal_text=colors["yellow"],
        hover_text=colors["yellow_hover"],
    )
    return canvas
