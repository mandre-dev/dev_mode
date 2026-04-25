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
    get_preset_by_name,
    update_preset,
)
from ide_detector import detect_ides
from music_detector import detect_music_apps
from brightness_controller import set_brightness
from preset_applier import apply_preset
from ui_components import ToolTip, create_icon_button, create_shadow_button
from font_renderer import render_text_image, get_font_path


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
        """Constrói o título com cores separadas e fonte Press Start 2P via PIL."""
        frame = tk.Frame(self.center_frame, bg=colors["bg"])
        font_path = get_font_path("PressStart2P-Regular.ttf")

        self._title_images = []  # Manter referências para evitar garbage collection

        for text, color in [
            ("Dev", colors["title_dev"]),
            ("_", colors["title_underscore"]),
            ("Mode", colors["title_mode"]),
        ]:
            img = render_text_image(text, font_path, 14, color, colors["bg"])
            self._title_images.append(img)
            lbl = tk.Label(frame, image=img, bg=colors["bg"])
            lbl.pack(side="left")
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
        def _on_edit():
            selected = self.combo.get()
            if not selected:
                return
            preset = get_preset_by_name(selected)
            if preset:
                self._build_add_screen(preset_data=preset)

        btn_edit = create_icon_button(row, "editar.png", "Editar", command=_on_edit)
        btn_edit.pack(side="left", padx=(10, 0))
        ToolTip(btn_edit, "Edit")

        # Botão Adicionar
        btn_add = create_icon_button(
            row, "adicionar.png", "Adicionar", command=self._build_add_screen
        )
        btn_add.pack(side="left", padx=(10, 0))
        ToolTip(btn_add, "Add")

        # Botão Excluir
        btn_delete = create_icon_button(
            row, "excluir.png", "Excluir", command=self._on_delete
        )
        btn_delete.pack(side="left", padx=(10, 0))
        ToolTip(btn_delete, "Delete")

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
        """Aplica o preset selecionado: IDE, playlist e brilho."""
        selected = self.combo.get()
        if not selected:
            self._set_status("Select a preset first!", colors["warning"])
            return

        preset = get_preset_by_name(selected)
        if not preset:
            self._set_status("Preset not found!", colors["warning"])
            return

        results = apply_preset(preset)

        # Monta mensagem de feedback
        parts = []
        if results["ide"]:
            parts.append(f"IDE: {preset.get('ide', '')}")
        if results["playlist"]:
            parts.append("Playlist opened")
        if results["brightness"]:
            parts.append(f"Brightness: {preset.get('brightness', 100)}%")

        if parts:
            self._set_status("Applied: " + " | ".join(parts), colors["success_bg"])
        else:
            self._set_status("Could not apply preset.", colors["warning"])

    def _set_status(self, message, color):
        """Exibe uma mensagem de status temporária na tela principal."""
        if hasattr(self, "_status_label"):
            self._status_label.destroy()

        self._status_label = tk.Label(
            self.center_frame,
            text=message,
            font=("Arial", 10, "bold"),
            fg=colors["text_light"] if color != colors["success_bg"] else "#006400",
            bg=color,
            padx=10,
            pady=4,
            bd=1,
            relief="solid",
        )
        self._status_label.pack(pady=(8, 0))

        # Limpa a mensagem após 4 segundos
        self.root.after(
            4000,
            lambda: (
                self._status_label.destroy() if hasattr(self, "_status_label") else None
            ),
        )

    def _build_add_screen(self, preset_data=None):
        """Constrói a tela de adicionar/editar preset."""
        self._clear_screen()
        # Aumenta a altura da janela para caber os novos campos
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT + 160}")

        is_edit = preset_data is not None
        banner_text = "Editing Preset" if is_edit else "Adding Preset"
        btn_text = "Update" if is_edit else "Save Preset"

        # Banner
        tk.Label(
            self.center_frame,
            text=banner_text,
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

        entry = tk.Entry(
            frame,
            font=("Arial", 12),
            width=18,
            bg=colors["text_light"],
        )
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

        ides_list = ["-- Select IDE --"] + detect_ides()
        ide_var = tk.StringVar(value="-- Select IDE --")
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

        # Campo URL (aparece logo embaixo quando Custom URL é selecionado)
        url_container = tk.Frame(self.center_frame, bg=colors["bg"])
        url_label = tk.Label(
            url_container,
            text="Playlist URL:",
            font=("Arial", 12),
            fg=colors["accent"],
            bg=colors["bg"],
        )
        url_label.pack(side="left", padx=(0, 10))
        url_entry = tk.Entry(
            url_container, font=("Arial", 12), width=22, bg=colors["text_light"]
        )
        url_entry.pack(side="left")

        def toggle_url_field(event=None):
            if playlist_var.get() == "Custom URL":
                url_container.pack(pady=(0, 10), after=music_frame)
            else:
                url_container.pack_forget()

        playlist_combo.bind("<<ComboboxSelected>>", toggle_url_field)
        toggle_url_field()

        # Brilho do monitor
        brightness_frame = tk.Frame(self.center_frame, bg=colors["bg"])
        brightness_frame.pack(pady=(0, 10))

        tk.Label(
            brightness_frame,
            text="Brightness:",
            font=("Arial", 12),
            fg=colors["accent"],
            bg=colors["bg"],
        ).pack(side="left", padx=(0, 10))

        brightness_var = tk.IntVar(value=100)
        brightness_scale = tk.Scale(
            brightness_frame,
            from_=10,
            to=100,
            orient="horizontal",
            length=150,
            variable=brightness_var,
            bg=colors["bg"],
            fg=colors["accent"],
            highlightthickness=0,
            troughcolor=colors["text_dark"],
            activebackground=colors["accent"],
            showvalue=True,
        )
        brightness_scale.pack(side="left")

        # Preenche campos se estiver em modo de edição
        original_name = ""
        if is_edit:
            original_name = preset_data.get("name", "")
            entry.insert(0, original_name)

            ide_val = preset_data.get("ide", "-- Select IDE --")
            if ide_val in ides_list:
                ide_var.set(ide_val)
            else:
                ide_var.set("-- Select IDE --")

            playlist_val = preset_data.get("playlist", "")
            if playlist_val in playlist_options:
                playlist_var.set(playlist_val)
            else:
                # Assume que é uma URL customizada
                playlist_var.set("Custom URL")
                url_entry.delete(0, tk.END)
                url_entry.insert(0, playlist_val)
            toggle_url_field()

            brightness_val = preset_data.get("brightness", 100)
            brightness_var.set(brightness_val)

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

            selected_ide = ide_var.get()
            if selected_ide == "-- Select IDE --":
                warning_label.config(text="Please select a Default IDE.")
                return
            warning_label.config(text="")

            playlist = playlist_var.get()
            if playlist == "Custom URL":
                playlist = url_entry.get().strip()

            if is_edit:
                success = update_preset(
                    original_name, name, ide_var.get(), playlist, brightness_var.get()
                )
                if not success:
                    warning_label.config(text="A preset with this name already exists.")
                    return
            else:
                add_preset(name, ide_var.get(), playlist, brightness_var.get())
            entry.delete(0, tk.END)
            entry.config(bg=colors["success_bg"])
            self._build_main_screen()

        save_btn = create_shadow_button(
            btns_frame, 120, 36, btn_text, click_command=do_save
        )
        save_btn.pack(side="left", padx=(0, 8))

        def do_clean():
            if not is_edit:
                entry.delete(0, tk.END)
            entry.config(bg=colors["text_light"])
            ide_var.set("-- Select IDE --")
            playlist_combo.set(
                playlist_options[0] if playlist_options else "Custom URL"
            )
            url_entry.delete(0, tk.END)
            toggle_url_field()
            brightness_var.set(100)

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
