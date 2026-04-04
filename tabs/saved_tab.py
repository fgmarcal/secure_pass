import tkinter as tk
from tkinter import ttk, messagebox
import locales as lang
from styles.theme import BG, SURFACE
from styles.button_style import ButtonStyle
from utils.utils import copy_to_clipboard
from database.database import fetch_all, delete_from_db


class SavedTab:
    def __init__(self, tab_control: ttk.Notebook) -> None:
        self.tab_control = tab_control
        self._row_id_map: dict[str, int] = {}
        self._password_map: dict[str, str | None] = {}
        self.frame = ttk.Frame(tab_control)
        tab_control.add(self.frame, text=lang.t("tab_saved"))
        self._build(self.frame)
        self.update_table()
        lang.register_callback(self._retranslate)

    def _build(self, parent: ttk.Frame) -> None:
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=0, pady=(0, 0))

        columns = ("Website", "Email", "Password")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("Website",  text=lang.t("col_website"))
        self.tree.heading("Email",    text=lang.t("col_email"))
        self.tree.heading("Password", text=lang.t("col_password"))

        self.tree.column("Website",  width=160, anchor="w")
        self.tree.column("Email",    width=200, anchor="w")
        self.tree.column("Password", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tree.bind("<Double-1>", self._on_item_click)

        bottom = tk.Frame(parent, bg=BG)
        bottom.pack(fill="x", pady=10)

        self.btn_delete = ButtonStyle(bottom, text=lang.t("btn_delete_selected"), command=self._delete_selected)
        self.btn_delete.pack()

    def _retranslate(self) -> None:
        self.tab_control.tab(self.frame, text=lang.t("tab_saved"))
        self.tree.heading("Website",  text=lang.t("col_website"))
        self.tree.heading("Email",    text=lang.t("col_email"))
        self.tree.heading("Password", text=lang.t("col_password"))
        self.btn_delete.config(text=lang.t("btn_delete_selected"))

    def update_table(self) -> None:
        """Updates the table with data from the database."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        self._row_id_map.clear()
        self._password_map.clear()

        for row_id, website, email, password in fetch_all():
            displayed_password = "•••••••" if password is not None else lang.t("pwd_unavailable_marker")
            item_id = self.tree.insert("", "end", values=(website, email, displayed_password))
            self._row_id_map[item_id] = row_id
            self._password_map[item_id] = password

    def _delete_selected(self) -> None:
        """Deletes the selected row."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning(lang.t("warning_select_item_title"), lang.t("warning_select_item_msg"))
            return

        item_id = selected_item[0]
        row_id = self._row_id_map.get(item_id)
        if row_id is None:
            messagebox.showerror(lang.t("error_delete_title"), lang.t("error_delete_msg"))
            return

        values = self.tree.item(item_id, "values")
        website = values[0]

        if not messagebox.askyesno(
            lang.t("confirm_delete_title"),
            lang.t("confirm_delete_msg", website=website),
        ):
            return

        try:
            delete_from_db(row_id)
            self._row_id_map.pop(item_id, None)
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
            messagebox.showerror(lang.t("error_pwd_unreadable_title"), lang.t("error_pwd_unreadable_msg"))
            return

        try:
            copy_to_clipboard(self.tree, password)
            messagebox.showinfo(lang.t("success_copy_title"), lang.t("success_copy_msg"))
        except Exception:
            messagebox.showerror(lang.t("error_copy_title"), lang.t("error_copy_msg"))
