import tkinter as tk
from tkinter import messagebox
import locales as lang
from styles.theme import BG, TEXT, TEXT_MUTED, ACCENT, ACCENT_HOV, ENTRY_BG, BORDER, FONT
from database.crypto import init_crypto, SALT_FILE


def _styled_entry(parent: tk.Widget, **kwargs) -> tk.Entry:
    return tk.Entry(
        parent,
        font=(FONT, 11),
        bg=ENTRY_BG,
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat",
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=ACCENT,
        **kwargs,
    )


def _styled_button(parent: tk.Widget, **kwargs) -> tk.Button:
    return tk.Button(
        parent,
        font=(FONT, 10, "bold"),
        bg=ACCENT,
        fg=TEXT,
        activebackground=ACCENT_HOV,
        activeforeground=TEXT,
        relief="flat",
        bd=0,
        padx=20,
        pady=8,
        cursor="hand2",
        **kwargs,
    )


def prompt_master_password(root: tk.Tk) -> bool:
    """
    Shows a modal dialog asking for the master password.
    Returns True if the password was accepted, False if the user cancelled.
    On first launch (no salt file yet), the entered password becomes the master password.
    """
    is_first_launch = not SALT_FILE.exists()

    dialog = tk.Toplevel(root)
    dialog.title(lang.t("master_pwd_dialog_title"))
    dialog.configure(bg=BG)
    dialog.resizable(False, False)
    dialog.grab_set()

    padding = dict(padx=32)

    tk.Label(
        dialog,
        text=lang.t("master_pwd_create_label") if is_first_launch else lang.t("master_pwd_enter_label"),
        font=(FONT, 11),
        bg=BG,
        fg=TEXT_MUTED,
    ).pack(pady=(28, 8), **padding)

    password_var = tk.StringVar()
    entry = _styled_entry(dialog, textvariable=password_var, show="*", width=30)
    entry.pack(ipady=6, **padding)
    entry.focus()

    confirm_var = tk.StringVar()
    confirm_label = tk.Label(
        dialog,
        text=lang.t("master_pwd_confirm_label"),
        font=(FONT, 11),
        bg=BG,
        fg=TEXT_MUTED,
    )
    confirm_entry = _styled_entry(dialog, textvariable=confirm_var, show="*", width=30)
    if is_first_launch:
        confirm_label.pack(pady=(14, 8), **padding)
        confirm_entry.pack(ipady=6, **padding)

    result = {"ok": False}

    def on_submit():
        pwd = password_var.get()
        if not pwd:
            messagebox.showwarning(
                lang.t("master_pwd_warning_empty_title"),
                lang.t("master_pwd_warning_empty_msg"),
                parent=dialog,
            )
            return
        if is_first_launch and pwd != confirm_var.get():
            messagebox.showerror(
                lang.t("master_pwd_error_mismatch_title"),
                lang.t("master_pwd_error_mismatch_msg"),
                parent=dialog,
            )
            return
        init_crypto(pwd)
        result["ok"] = True
        dialog.destroy()

    def on_cancel():
        dialog.destroy()

    btn_frame = tk.Frame(dialog, bg=BG)
    btn_frame.pack(pady=(20, 28))

    _styled_button(btn_frame, text=lang.t("btn_ok"),     command=on_submit).pack(side="left", padx=6)
    _styled_button(btn_frame, text=lang.t("btn_cancel"), command=on_cancel).pack(side="left", padx=6)

    dialog.bind("<Return>", lambda e: on_submit())
    dialog.bind("<Escape>", lambda e: on_cancel())

    root.wait_window(dialog)
    return result["ok"]
