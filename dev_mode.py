import tkinter as tk


class ToolTip:
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
            font=("Arial", 9),
            fg="#FFFFFF",
            bg="#333333",
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


root = tk.Tk()
root.title("Dev_Mode")
root.geometry("400x250")
root.configure(bg="#101820")

# Frame centralizador
center_frame = tk.Frame(root, bg="#101820")
center_frame.pack(expand=True)

# Título centralizado
label_title = tk.Label(
    center_frame,
    text="Dev_Mode",
    font=("Arial", 18, "bold"),
    fg="#00AEEF",
    bg="#101820",
)
label_title.pack(pady=(20, 10))


# Label 'Preset:' à esquerda da lista
from tkinter import ttk

row_frame = tk.Frame(center_frame, bg="#101820")
row_frame.pack(pady=20)

label_preset = tk.Label(
    row_frame, text="Preset:", font=("Arial", 12), fg="#00AEEF", bg="#101820"
)
label_preset.pack(side="left", padx=(0, 10))

# Lista suspensa (Combobox) vazia
combo = ttk.Combobox(
    row_frame, values=[], state="readonly", font=("Arial", 12), width=18
)
combo.set("")
combo.pack(side="left")

# Botão de editar com ícone de lápis
from tkinter import PhotoImage

try:
    pencil_icon = PhotoImage(file="editar.png")
    # Reduz a imagem proporcionalmente para ~20x20 px (tamanho próximo ao texto "Editar")
    factor = max(1, pencil_icon.width() // 20)
    if factor > 1:
        pencil_icon = pencil_icon.subsample(factor, factor)
    btn_edit = tk.Button(
        row_frame,
        image=pencil_icon,
        bg="#101820",
        bd=0,
        activebackground="#101820",
    )
    btn_edit.image = pencil_icon  # manter referência
except Exception:
    btn_edit = tk.Button(
        row_frame,
        text="Editar",
        bg="#101820",
        fg="#00AEEF",
        bd=0,
        activebackground="#101820",
    )
btn_edit.pack(side="left", padx=(10, 0))
ToolTip(btn_edit, "Editar")

# Botão de adicionar
try:
    add_icon = PhotoImage(file="adicionar.png")
    # Reduz a imagem proporcionalmente para ~20x20 px
    factor_add = max(1, add_icon.width() // 20)
    if factor_add > 1:
        add_icon = add_icon.subsample(factor_add, factor_add)
    btn_add = tk.Button(
        row_frame,
        image=add_icon,
        bg="#101820",
        bd=0,
        activebackground="#101820",
    )
    btn_add.image = add_icon  # manter referência
except Exception:
    btn_add = tk.Button(
        row_frame,
        text="Adicionar",
        bg="#101820",
        fg="#00AEEF",
        bd=0,
        activebackground="#101820",
    )
btn_add.pack(side="left", padx=(10, 0))
ToolTip(btn_add, "Adicionar")

# Botão de excluir
try:
    delete_icon = PhotoImage(file="excluir.png")
    # Reduz a imagem proporcionalmente para ~20x20 px
    factor_del = max(1, delete_icon.width() // 20)
    if factor_del > 1:
        delete_icon = delete_icon.subsample(factor_del, factor_del)
    btn_delete = tk.Button(
        row_frame,
        image=delete_icon,
        bg="#101820",
        bd=0,
        activebackground="#101820",
    )
    btn_delete.image = delete_icon  # manter referência
except Exception:
    btn_delete = tk.Button(
        row_frame,
        text="Excluir",
        bg="#101820",
        fg="#00AEEF",
        bd=0,
        activebackground="#101820",
    )
btn_delete.pack(side="left", padx=(10, 0))
ToolTip(btn_delete, "Excluir")

# Botão Apply abaixo da lista suspensa
btn_apply = tk.Button(
    center_frame,
    text="Apply",
    font=("Arial", 12, "bold"),
    fg="#101820",
    bg="#00AEEF",
    bd=0,
    activebackground="#008BC7",
    activeforeground="#101820",
    padx=20,
    pady=5,
)
btn_apply.pack(pady=(10, 0))

root.mainloop()
