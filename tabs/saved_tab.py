import tkinter as tk
from tkinter import ttk, messagebox
import locales as lang
from styles.button_style import ButtonStyle
from utils.utils import copy_to_clipboard
from database.database import fetch_all, delete_from_db


class SavedTab:
    def __init__(self, tab_control: ttk.Notebook) -> None:
        self.tab_control = tab_control
        self._password_map: dict[str, str] = {}
        self.frame = ttk.Frame(tab_control)
        tab_control.add(self.frame, text=lang.t("tab_saved"))
        self._build(self.frame)
        self.update_table()
        lang.register_callback(self._retranslate)

    def _build(self, parent: ttk.Frame) -> None:
        columns = ("Website", "Email", "Password")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("Website", text=lang.t("col_website"))
        self.tree.heading("Email", text=lang.t("col_email"))
        self.tree.heading("Password", text=lang.t("col_password"))

        self.tree.column("Website", width=150)
        self.tree.column("Email", width=200)
        self.tree.column("Password", width=100)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self._on_item_click)

        self.btn_delete = ButtonStyle(parent, text=lang.t("btn_delete_selected"), command=self._delete_selected)
        self.btn_delete.pack(pady=5)

    def _retranslate(self) -> None:
        self.tab_control.tab(self.frame, text=lang.t("tab_saved"))
        self.tree.heading("Website", text=lang.t("col_website"))
        self.tree.heading("Email", text=lang.t("col_email"))
        self.tree.heading("Password", text=lang.t("col_password"))
        self.btn_delete.config(text=lang.t("btn_delete_selected"))

    def update_table(self) -> None:
        """Updates the table with data from the database."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        self._password_map.clear()

        for website, email, password in fetch_all():
            item_id = self.tree.insert("", "end", values=(website, email, "***"))
            self._password_map[item_id] = password

    def _delete_selected(self) -> None:
        """Deletes the selected row."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning(lang.t("warning_select_item_title"), lang.t("warning_select_item_msg"))
            return

        item_id = selected_item[0]
        values = self.tree.item(item_id, "values")
        website, email = values[0], values[1]

        if not messagebox.askyesno(
            lang.t("confirm_delete_title"),
            lang.t("confirm_delete_msg", website=website),
        ):
            return

        try:
            delete_from_db(website, email)
            self._password_map.pop(item_id, None)
            self.update_table()
        except Exception as e:
            print(f"An error occurred: {e}")
            messagebox.showerror(lang.t("error_delete_title"), lang.t("error_delete_msg"))
        else:
            messagebox.showinfo(lang.t("success_delete_title"), lang.t("success_delete_msg"))

    def _on_item_click(self, event) -> None:
        """Copies the password on double-click of a table row."""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_id = selected_item[0]
        password = self._password_map.get(item_id)
        if password is None:
            messagebox.showerror(lang.t("error_pwd_not_found_title"), lang.t("error_pwd_not_found_msg"))
            return

        try:
            copy_to_clipboard(self.tree, password)
            messagebox.showinfo(lang.t("success_copy_title"), lang.t("success_copy_msg"))
        except Exception:
            messagebox.showerror(lang.t("error_copy_title"), lang.t("error_copy_msg"))
