import tkinter as tk
from tkinter import ttk, messagebox
from styles.button_style import ButtonStyle
from utils.utils import copy_to_clipboard
from database.database import fetch_all, delete_from_db


class SavedTab:
    def __init__(self, tab_control: ttk.Notebook) -> None:
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
        """Atualiza a tabela com os dados do banco de dados."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for website, email, password in fetch_all():
            self.tree.insert("", "end", values=(website, email, "***", password))

    def _delete_selected(self) -> None:
        """Deleta a linha selecionada."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um item para excluir.")
            return

        values = self.tree.item(selected_item, "values")
        website, email = values[0], values[1]

        if not messagebox.askyesno("Delete", f"Tem certeza que deseja excluir a senha de {website}?"):
            return

        try:
            delete_from_db(website, email)
            self.update_table()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro ao excluir a senha.")
        else:
            messagebox.showinfo("Success", "Senha excluída com sucesso.")

    def _on_item_click(self, event) -> None:
        """Copia a senha ao dar duplo clique na linha da tabela."""
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item, "values")
            try:
                copy_to_clipboard(self.tree, values[3])
                messagebox.showinfo("Success", "Password copiado para a área de transferência.")
            except Exception:
                messagebox.showerror("Erro", "Não foi possível copiar a senha.")
