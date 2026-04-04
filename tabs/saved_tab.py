import tkinter as tk
from tkinter import ttk, messagebox
from styles.button_style import ButtonStyle
from database.database import fetch_all, delete_from_db

def copy_to_clipboard(password):
    """Copia a senha para a área de transferência."""
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(password)
    messagebox.showinfo("Success", "Password copiado para a área de transferência.")
    root.update()
    root.destroy()

def update_table():
    """Atualiza a tabela com os dados do banco de dados."""
    for row in tree.get_children():
        tree.delete(row)  # Limpa os dados antigos

    for website, email, password in fetch_all():
        tree.insert("", "end", values=(website, email, "***", password))

def delete_selected():
    """Deleta a linha selecionada."""
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item, "values")
        website, email = values[0], values[1]

        confirm = messagebox.askyesno("Delete", f"Tem certeza que deseja excluir a senha de {website}?")
        try:
            if confirm:
                delete_from_db(website, email)
                update_table()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro ao excluir a senha.")
        else:
            messagebox.showinfo("Success", "Senha excluída com sucesso.")
    else:
        messagebox.showwarning("Atenção", "Selecione um item para excluir.")

def on_item_click(event):
    """Copia a senha ao clicar na linha da tabela."""
    password = 3
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item, "values")
        copy_to_clipboard(values[password])  # Copia a senha real (index 3)

def create_saved_tab(tab_control):
    """Cria a aba Saved."""
    global tree
    saved_frame = ttk.Frame(tab_control)
    tab_control.add(saved_frame, text="Saved")

    columns = ("Website", "Email", "Password")
    tree = ttk.Treeview(saved_frame, columns=columns, show="headings", selectmode="browse")

    tree.heading("Website", text="Website")
    tree.heading("Email", text="Email")
    tree.heading("Password", text="Password")

    tree.column("Website", width=150)
    tree.column("Email", width=200)
    tree.column("Password", width=100)

    tree.pack(fill="both", expand=True)
    tree.bind("<Double-1>", on_item_click)  # Clique duplo copia senha

    delete_button = tk.Button(saved_frame, text="Delete Selected",
                                command=delete_selected)
    styled_delete_button = ButtonStyle(delete_button)
    styled_delete_button.pack(pady=5)

    update_table()
    return saved_frame
