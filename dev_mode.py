import tkinter as tk

root = tk.Tk()
root.title("Dev_Mode")
root.geometry("400x250")
root.configure(bg="#101820")

# Título
label_title = tk.Label(root, text="Dev_Mode", font=("Arial", 18, "bold"), fg="#00AEEF", bg="#101820")
label_title.pack(pady=(20, 10))

# Botão de exemplo
btn_exemplo = tk.Button(
    root,
    text="Clique aqui",
    font=("Arial", 12),
    bg="#00AEEF",
    fg="white",
    activebackground="#0077A3",
    activeforeground="white"
)
btn_exemplo.pack(pady=20)

root.mainloop()
