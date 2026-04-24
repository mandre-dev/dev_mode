"""Aplicação principal Dev_Mode com gerenciamento de telas."""

import tkinter as tk
from tkinter import ttk

from config import colors, WINDOW_WIDTH, WINDOW_HEIGHT
from presets_manager import (
    load_presets,
    save_presets,
    get_preset_names,
    delete_preset_by_name,
    add_preset,
)
from ide_detector import detect_ides
from music_detector import detect_music_apps
from ui_components import ToolTip, create_icon_button, create_shadow_button


class DevModeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Dev_Mode")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=colors["bg"])

        self.center_frame = tk.Frame(self.root, bg=colors["bg"])
        self.center_frame.pack(expand=True)

        self.title_frame = self._build_title()
        self.title_frame.pack(pady=(20, 10))

        self.combo = None
        self._build_main_screen()

    def _build_title(self):
        """Constrói o título com cores separadas."""
        frame = tk.Frame(self.center_frame, bg=colors["bg"])
        for text, color in [
            ("Dev", colors["title_dev"]),
            ("_", colors["title_underscore"]),
            ("Mode", colors["title_mode"]),
        ]:
            tk.Label(
                frame,
                text=text,
                font=("Arial", 18, "bold"),
                fg=color,
                bg=colors["bg"],
            ).pack(side="left")
        return frame

    def _clear_screen(self):
        """Remove todos os widgets exceto o título."""
        for widget in self.center_frame.winfo_children():
            if widget == self.title_frame:
                continue
            widget.destroy()

    def _build_main_screen(self):
        """Constrói a tela principal com combobox e botões."""
        self._clear_screen()
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        row = tk.Frame(self.center_frame, bg=colors["bg"])
        row.pack(pady=20)

        tk.Label(
            row,
            text="Preset:",
            font=("Arial", 12),
            fg=colors["accent"],
            bg=colors["bg"],
        ).pack(side="left", padx=(0, 10))

        self.combo = ttk.Combobox(
            row,
            values=get_preset_names(),
            state="readonly",
            font=("Arial", 12),
            width=18,
        )
        self.combo.set("")
        self.combo.pack(side="left")

        # Botão Editar
        btn_edit = create_icon_button(row, "editar.png", "Editar")
        btn_edit.pack(side="left", padx=(10, 0))
        ToolTip(btn_edit, "Editar")

        # Botão Adicionar
        btn_add = create_icon_button(
            row, "adicionar.png", "Adicionar", command=self._build_add_screen
        )
        btn_add.pack(side="left", padx=(10, 0))
        ToolTip(btn_add, "Adicionar")

        # Botão Excluir
        btn_delete = create_icon_button(
            row, "excluir.png", "Excluir", command=self._on_delete
        )
        btn_delete.pack(side="left", padx=(10, 0))
        ToolTip(btn_delete, "Excluir")

        # Botão Apply
        apply_btn = create_shadow_button(
            self.center_frame, 100, 36, "Apply", click_command=self._on_apply
        )
        apply_btn.pack(pady=(10, 0))

    def _on_delete(self):
        """Exclui o preset selecionado."""
        selected = self.combo.get()
        if not selected:
            return
        delete_preset_by_name(selected)
        self.combo.config(values=get_preset_names())
        self.combo.set("")

    def _on_apply(self):
        """Ação do botão Apply (a implementar)."""
        pass

    def _build_add_screen(self):
        """Constrói a tela de adicionar preset."""
        self._clear_screen()
        # Aumenta a altura da janela para caber os novos campos
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT + 100}")

        # Banner
        tk.Label(
            self.center_frame,
            text="Adding Preset",
            font=("Arial", 13, "bold"),
            fg=colors["yellow"],
            bg=colors["bg"],
            pady=8,
            bd=2,
            relief="solid",
            highlightbackground=colors["text_light"],
            highlightcolor=colors["text_light"],
            highlightthickness=2,
        ).pack(pady=(10, 14), fill="x", padx=40)

        # Campo nome
        frame = tk.Frame(self.center_frame, bg=colors["bg"])
        frame.pack(pady=(0, 10))

        tk.Label(
            frame,
            text="Preset name:",
            font=("Arial", 12),
            fg=colors["accent"],
            bg=colors["bg"],
        ).pack(side="left", padx=(0, 10))

        entry = tk.Entry(frame, font=("Arial", 12), width=18, bg=colors["text_light"])
        entry.pack(side="left")

        warning_label = tk.Label(
            self.center_frame,
            text="",
            font=("Arial", 10, "bold"),
            fg=colors["warning"],
            bg=colors["bg"],
        )
        warning_label.pack()

        # IDE
        ide_frame = tk.Frame(self.center_frame, bg=colors["bg"])
        ide_frame.pack(pady=(0, 10))

        tk.Label(
            ide_frame,
            text="Default IDE:",
            font=("Arial", 12),
            fg=colors["accent"],
            bg=colors["bg"],
        ).pack(side="left", padx=(0, 10))

        ides_list = detect_ides()
        ide_var = tk.StringVar(value=ides_list[0])
        ide_combo = ttk.Combobox(
            ide_frame,
            values=ides_list,
            state="readonly",
            font=("Arial", 12),
            width=18,
            textvariable=ide_var,
        )
        ide_combo.pack(side="left")

        # Playlist
        music_frame = tk.Frame(self.center_frame, bg=colors["bg"])
        music_frame.pack(pady=(0, 10))

        tk.Label(
            music_frame,
            text="Playlist:",
            font=("Arial", 12),
            fg=colors["accent"],
            bg=colors["bg"],
        ).pack(side="left", padx=(0, 10))

        music_apps = detect_music_apps()
        playlist_options = music_apps + ["Custom URL"]
        playlist_var = tk.StringVar(
            value=playlist_options[0] if playlist_options else "Custom URL"
        )
        playlist_combo = ttk.Combobox(
            music_frame,
            values=playlist_options,
            state="readonly",
            font=("Arial", 12),
            width=18,
            textvariable=playlist_var,
        )
        playlist_combo.pack(side="left")

        # Campo URL (aparece quando Custom URL é selecionado)
        url_frame = tk.Frame(self.center_frame, bg=colors["bg"])
        url_label = tk.Label(
            url_frame,
            text="Playlist URL:",
            font=("Arial", 12),
            fg=colors["accent"],
            bg=colors["bg"],
        )
        url_label.pack(side="left", padx=(0, 10))
        url_entry = tk.Entry(
            url_frame, font=("Arial", 12), width=22, bg=colors["text_light"]
        )
        url_entry.pack(side="left")

        def toggle_url_field(event=None):
            if playlist_var.get() == "Custom URL":
                url_frame.pack(pady=(0, 10))
            else:
                url_frame.pack_forget()

        playlist_combo.bind("<<ComboboxSelected>>", toggle_url_field)
        toggle_url_field()

        # Botões
        btns_frame = tk.Frame(self.center_frame, bg=colors["bg"])
        btns_frame.pack(pady=(10, 0))

        def do_save():
            name = entry.get().strip()
            if not name:
                entry.config(bg=colors["error_bg"])
                warning_label.config(
                    text="Please fill in the Preset name before saving."
                )
                return
            warning_label.config(text="")

            playlist = playlist_var.get()
            if playlist == "Custom URL":
                playlist = url_entry.get().strip()

            add_preset(name, ide_var.get(), playlist)
            entry.delete(0, tk.END)
            entry.config(bg=colors["success_bg"])
            self._build_main_screen()

        save_btn = create_shadow_button(
            btns_frame, 120, 36, "Save Preset", click_command=do_save
        )
        save_btn.pack(side="left", padx=(0, 8))

        def do_clean():
            entry.delete(0, tk.END)
            entry.config(bg=colors["text_light"])
            ide_combo.set(ides_list[0])
            playlist_combo.set(
                playlist_options[0] if playlist_options else "Custom URL"
            )
            url_entry.delete(0, tk.END)
            toggle_url_field()

        clean_btn = tk.Button(
            btns_frame,
            text="Clean",
            font=("Arial", 12, "bold"),
            fg=colors["yellow"],
            bg=colors["btn_clean"],
            activebackground=colors["btn_clean_active"],
            bd=0,
            cursor="hand2",
            command=do_clean,
            width=8,
        )
        clean_btn.pack(side="left", padx=(0, 8))

        cancel_btn = tk.Button(
            btns_frame,
            text="Cancel",
            font=("Arial", 12, "bold"),
            fg=colors["yellow"],
            bg=colors["btn_cancel"],
            activebackground=colors["btn_cancel_active"],
            bd=0,
            cursor="hand2",
            command=self._build_main_screen,
            width=8,
        )
        cancel_btn.pack(side="left")

    def run(self):
        self.root.mainloop()
