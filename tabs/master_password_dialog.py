import tkinter as tk
from tkinter import messagebox
from database.crypto import init_crypto, SALT_FILE


def prompt_master_password(root: tk.Tk) -> bool:
    """
    Shows a modal dialog asking for the master password.
    Returns True if the password was accepted, False if the user cancelled.
    On first launch (no salt file yet), the entered password becomes the master password.
    """
    is_first_launch = not SALT_FILE.exists()

    dialog = tk.Toplevel(root)
    dialog.title("Master Password")
    dialog.resizable(False, False)
    dialog.grab_set()

    label_text = (
        "Create a master password:" if is_first_launch
        else "Enter your master password:"
    )
    tk.Label(dialog, text=label_text, font=("Arial", 10, "bold"), pady=10).pack(padx=20)

    password_var = tk.StringVar()
    entry = tk.Entry(dialog, textvariable=password_var, show="*", width=30)
    entry.pack(padx=20, pady=(0, 5))
    entry.focus()

    confirm_var = tk.StringVar()
    confirm_label = tk.Label(dialog, text="Confirm master password:", font=("Arial", 10, "bold"))
    confirm_entry = tk.Entry(dialog, textvariable=confirm_var, show="*", width=30)
    if is_first_launch:
        confirm_label.pack(padx=20, pady=(5, 0))
        confirm_entry.pack(padx=20, pady=(0, 5))

    result = {"ok": False}

    def on_submit():
        pwd = password_var.get()
        if not pwd:
            messagebox.showwarning("Aviso", "A senha não pode ser vazia.", parent=dialog)
            return
        if is_first_launch and pwd != confirm_var.get():
            messagebox.showerror("Erro", "As senhas não coincidem.", parent=dialog)
            return
        init_crypto(pwd)
        result["ok"] = True
        dialog.destroy()

    def on_cancel():
        dialog.destroy()

    btn_frame = tk.Frame(dialog)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="OK", width=10, command=on_submit).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Cancelar", width=10, command=on_cancel).pack(side="left", padx=5)

    dialog.bind("<Return>", lambda e: on_submit())
    dialog.bind("<Escape>", lambda e: on_cancel())

    root.wait_window(dialog)
    return result["ok"]
