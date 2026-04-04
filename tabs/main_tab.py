from styles.button_style import ButtonStyle
from utils.utils import password_generator, validate_entries
import tkinter as tk
from tkinter import ttk, END, messagebox
from database.database import save_to_db
from tabs.saved_tab import update_table


def add_entry(tab_control):
    """Função chamada ao clicar no botão Add para salvar os dados no banco."""
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if not validate_entries(website=website, email=email, password=password):
        messagebox.showwarning("Vazio?", "Preencha todos os campos.")
        return

    if website and email and password:
        save_to_db(website, email, password)
        update_table()
        clear_fields(tab_control)

def generate_password(tab_control):
    password_entry.delete(0, END)
    PASSWORD=password_generator()
    password_entry.insert(0, PASSWORD)

def clear_fields(tab_control):
    website_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def create_main_tab(tab_control):
    """Cria a aba principal."""
    main_frame = ttk.Frame(tab_control)
    tab_control.add(main_frame, text="Main")

    global website_entry, email_entry, password_entry

    tk.Label(main_frame, text="Website:", font=("Arial", 10, "bold")).grid(row=0, column=0)
    tk.Label(main_frame, text="Email/Username:", font=("Arial", 10, "bold")).grid(row=1, column=0)
    tk.Label(main_frame, text="Password:", font=("Arial", 10, "bold")).grid(row=2, column=0)

    website_entry = tk.Entry(main_frame, width=30)
    website_entry.grid(row=0, column=1)
    website_entry.focus()

    email_entry = tk.Entry(main_frame, width=30)
    email_entry.grid(row=1, column=1)

    password_entry = tk.Entry(main_frame, width=30, show="*")
    password_entry.grid(row=2, column=1)

    free_space_label = tk.Label(main_frame, text="")
    free_space_label.grid(row=3, column=0)

    clear_fields_button = tk.Button(main_frame, text="Limpar")
    styled_clear_fields_button = ButtonStyle(clear_fields_button)
    styled_clear_fields_button.set_command(lambda: clear_fields(tab_control))
    styled_clear_fields_button.grid(row=4, column=0)


    add_button = tk.Button(main_frame, text="Salvar")
    styled_add_button = ButtonStyle(add_button)
    styled_add_button.set_command(lambda: add_entry(tab_control))
    styled_add_button.grid(row=4, column=1)

    generate_passord_button = tk.Button(main_frame, text="Auto gerar!")
    styled_generate_passord_button = ButtonStyle(generate_passord_button)
    styled_generate_passord_button.set_command(lambda: generate_password(tab_control))
    styled_generate_passord_button.grid(row=4, column=2)


    return main_frame
