import tkinter as tk
from tkinter import ttk, messagebox
import locales as lang
from styles.theme import BG, TEXT_MUTED, FONT
from styles.button_style import ButtonStyle
from utils.utils import copy_to_clipboard, validate_entries
from database.database import fetch_all, delete_from_db, update_in_db


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

        actions = tk.Frame(bottom, bg=BG)
        actions.pack()

        self.btn_edit = ButtonStyle(actions, text=lang.t("btn_edit_selected"), command=self._edit_selected)
        self.btn_edit.pack(side="left", padx=6)

        self.btn_delete = ButtonStyle(actions, text=lang.t("btn_delete_selected"), command=self._delete_selected)
        self.btn_delete.pack(side="left", padx=6)

    def _retranslate(self) -> None:
        self.tab_control.tab(self.frame, text=lang.t("tab_saved"))
        self.tree.heading("Website",  text=lang.t("col_website"))
        self.tree.heading("Email",    text=lang.t("col_email"))
        self.tree.heading("Password", text=lang.t("col_password"))
        self.btn_edit.config(text=lang.t("btn_edit_selected"))
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

    def _edit_selected(self) -> None:
        """Opens a dialog to edit the selected row."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning(lang.t("warning_select_item_title"), lang.t("warning_select_item_msg"))
            return

        item_id = selected_item[0]
        row_id = self._row_id_map.get(item_id)
        password = self._password_map.get(item_id)
        if row_id is None:
            messagebox.showerror(lang.t("error_update_title"), lang.t("error_update_msg"))
            return
        if password is None:
            messagebox.showerror(lang.t("error_pwd_unreadable_title"), lang.t("error_pwd_unreadable_msg"))
            return

        website, email, _displayed_password = self.tree.item(item_id, "values")
        self._open_edit_dialog(row_id, str(website), str(email), password)

    def _open_edit_dialog(self, row_id: int, website: str, email: str, password: str) -> None:
        dialog = tk.Toplevel(self.frame)
        dialog.title(lang.t("edit_dialog_title"))
        dialog.configure(bg=BG)
        dialog.resizable(False, False)
        dialog.transient(self.frame.winfo_toplevel())
        dialog.grab_set()

        content = ttk.Frame(dialog)
        content.pack(padx=20, pady=18)

        label_cfg = dict(font=(FONT, 10), bg=BG, fg=TEXT_MUTED)
        entry_cfg = dict(width=30, font=(FONT, 10))

        tk.Label(content, text=lang.t("label_website"), **label_cfg).grid(row=0, column=0, sticky="e", padx=(0, 10), pady=8)
        website_entry = tk.Entry(content, **entry_cfg)
        website_entry.grid(row=0, column=1, sticky="w", pady=8, ipady=5)

        tk.Label(content, text=lang.t("label_email"), **label_cfg).grid(row=1, column=0, sticky="e", padx=(0, 10), pady=8)
        email_entry = tk.Entry(content, **entry_cfg)
        email_entry.grid(row=1, column=1, sticky="w", pady=8, ipady=5)

        tk.Label(content, text=lang.t("label_password"), **label_cfg).grid(row=2, column=0, sticky="e", padx=(0, 10), pady=8)
        password_entry = tk.Entry(content, show="*", **entry_cfg)
        password_entry.grid(row=2, column=1, sticky="w", pady=8, ipady=5)

        website_entry.insert(0, website)
        email_entry.insert(0, email)
        password_entry.insert(0, password)
        website_entry.focus()

        button_frame = ttk.Frame(content)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(14, 0))

        def save_changes() -> None:
            updated_website = website_entry.get()
            updated_email = email_entry.get()
            updated_password = password_entry.get()

            if not validate_entries(updated_website, updated_email, updated_password):
                messagebox.showwarning(lang.t("warning_fill_all_title"), lang.t("warning_fill_all_msg"))
                return

            try:
                update_in_db(row_id, updated_website, updated_email, updated_password)
                self.update_table()
            except Exception as e:
                print(f"An error occurred: {e}")
                messagebox.showerror(lang.t("error_update_title"), lang.t("error_update_msg"))
                return

            dialog.destroy()
            messagebox.showinfo(lang.t("success_update_title"), lang.t("success_update_msg"))

        btn_cancel = ButtonStyle(button_frame, text=lang.t("btn_cancel"), command=dialog.destroy)
        btn_cancel.pack(side="left", padx=6)

        btn_save = ButtonStyle(button_frame, text=lang.t("btn_save_changes"), command=save_changes)
        btn_save.pack(side="left", padx=6)

        dialog.bind("<Return>", lambda _event: save_changes())
        dialog.bind("<Escape>", lambda _event: dialog.destroy())

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
