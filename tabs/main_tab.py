import tkinter as tk
from tkinter import ttk, END, messagebox
from styles.button_style import ButtonStyle
from utils.utils import password_generator, validate_entries
from database.database import save_to_db


class MainTab:
    def __init__(self, tab_control: ttk.Notebook, saved_tab) -> None:
        self.saved_tab = saved_tab
        self.frame = ttk.Frame(tab_control)
        tab_control.add(self.frame, text="Main")
        self._build(self.frame)

    def _build(self, parent: ttk.Frame) -> None:
        tk.Label(parent, text="Website:", font=("Arial", 10, "bold")).grid(row=0, column=0)
        tk.Label(parent, text="Email/Username:", font=("Arial", 10, "bold")).grid(row=1, column=0)
        tk.Label(parent, text="Password:", font=("Arial", 10, "bold")).grid(row=2, column=0)

        self.website_entry = tk.Entry(parent, width=30)
        self.website_entry.grid(row=0, column=1)
        self.website_entry.focus()

        self.email_entry = tk.Entry(parent, width=30)
        self.email_entry.grid(row=1, column=1)

        self.password_entry = tk.Entry(parent, width=30, show="*")
        self.password_entry.grid(row=2, column=1)

        tk.Label(parent, text="").grid(row=3, column=0)

        ButtonStyle(parent, text="Limpar", command=self._clear_fields).grid(row=4, column=0)
        ButtonStyle(parent, text="Salvar", command=self._add_entry).grid(row=4, column=1)
        ButtonStyle(parent, text="Auto gerar!", command=self._generate_password).grid(row=4, column=2)

    def _add_entry(self) -> None:
        website = self.website_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not validate_entries(website=website, email=email, password=password):
            messagebox.showwarning("Vazio?", "Preencha todos os campos.")
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
