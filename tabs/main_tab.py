from __future__ import annotations
import tkinter as tk
from tkinter import ttk, END, messagebox
import locales as lang
from styles.button_style import ButtonStyle
from utils.utils import password_generator, validate_entries
from database.database import save_to_db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tabs.saved_tab import SavedTab


class MainTab:
    def __init__(self, tab_control: ttk.Notebook, saved_tab: SavedTab) -> None:
        self.tab_control = tab_control
        self.saved_tab = saved_tab
        self.frame = ttk.Frame(tab_control)
        tab_control.add(self.frame, text=lang.t("tab_main"))
        self._build(self.frame)
        lang.register_callback(self._retranslate)

    def _build(self, parent: ttk.Frame) -> None:
        self.lbl_website = tk.Label(parent, text=lang.t("label_website"), font=("Arial", 10, "bold"))
        self.lbl_website.grid(row=0, column=0)

        self.lbl_email = tk.Label(parent, text=lang.t("label_email"), font=("Arial", 10, "bold"))
        self.lbl_email.grid(row=1, column=0)

        self.lbl_password = tk.Label(parent, text=lang.t("label_password"), font=("Arial", 10, "bold"))
        self.lbl_password.grid(row=2, column=0)

        self.website_entry = tk.Entry(parent, width=30)
        self.website_entry.grid(row=0, column=1)
        self.website_entry.focus()

        self.email_entry = tk.Entry(parent, width=30)
        self.email_entry.grid(row=1, column=1)

        self.password_entry = tk.Entry(parent, width=30, show="*")
        self.password_entry.grid(row=2, column=1)

        tk.Label(parent, text="").grid(row=3, column=0)

        self.btn_clear = ButtonStyle(parent, text=lang.t("btn_clear"), command=self._clear_fields)
        self.btn_clear.grid(row=4, column=0)

        self.btn_save = ButtonStyle(parent, text=lang.t("btn_save"), command=self._add_entry)
        self.btn_save.grid(row=4, column=1)

        self.btn_generate = ButtonStyle(parent, text=lang.t("btn_auto_generate"), command=self._generate_password)
        self.btn_generate.grid(row=4, column=2)

    def _retranslate(self) -> None:
        self.tab_control.tab(self.frame, text=lang.t("tab_main"))
        self.lbl_website.config(text=lang.t("label_website"))
        self.lbl_email.config(text=lang.t("label_email"))
        self.lbl_password.config(text=lang.t("label_password"))
        self.btn_clear.config(text=lang.t("btn_clear"))
        self.btn_save.config(text=lang.t("btn_save"))
        self.btn_generate.config(text=lang.t("btn_auto_generate"))

    def _add_entry(self) -> None:
        website = self.website_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not validate_entries(website, email, password):
            messagebox.showwarning(lang.t("warning_fill_all_title"), lang.t("warning_fill_all_msg"))
            return

        save_to_db(website, email, password)
        self.saved_tab.update_table()
        self._clear_fields()

    def _generate_password(self) -> None:
        self.password_entry.delete(0, END)
        self.password_entry.insert(0, password_generator())

    def _clear_fields(self) -> None:
        self.website_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
