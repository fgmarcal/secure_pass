import tkinter as tk
from tkinter import ttk, messagebox
from styles.button_style import ButtonStyle
from utils.utils import copy_to_clipboard
from database.database import fetch_all, delete_from_db


class SavedTab:
    def __init__(self, tab_control: ttk.Notebook) -> None:
        self._password_map: dict[str, str] = {}
        self.frame = ttk.Frame(tab_control)
        tab_control.add(self.frame, text="Saved")
        self._build(self.frame)
        self.update_table()

    def _build(self, parent: ttk.Frame) -> None:
        columns = ("Website", "Email", "Password")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("Website", text="Website")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Password", text="Password")

        self.tree.column("Website", width=150)
        self.tree.column("Email", width=200)
        self.tree.column("Password", width=100)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self._on_item_click)

        ButtonStyle(parent, text="Delete Selected", command=self._delete_selected).pack(pady=5)

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
            messagebox.showwarning("Warning", "Please select an item to delete.")
            return

        item_id = selected_item[0]
        values = self.tree.item(item_id, "values")
        website, email = values[0], values[1]

        if not messagebox.askyesno("Delete", f"Are you sure you want to delete the password for {website}?"):
            return

        try:
            delete_from_db(website, email)
            self._password_map.pop(item_id, None)
            self.update_table()
        except Exception as e:
            print(f"An error occurred: {e}")
            messagebox.showerror("Error", "An error occurred while deleting the password.")
        else:
            messagebox.showinfo("Success", "Password deleted successfully.")

    def _on_item_click(self, event) -> None:
        """Copies the password on double-click of a table row."""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_id = selected_item[0]
        password = self._password_map.get(item_id)
        if password is None:
            messagebox.showerror("Error", "Password not found.")
            return

        try:
            copy_to_clipboard(self.tree, password)
            messagebox.showinfo("Success", "Password copied to clipboard.")
        except Exception:
            messagebox.showerror("Error", "Could not copy the password.")

