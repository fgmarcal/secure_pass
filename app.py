import tkinter as tk
from tkinter import ttk, Canvas, PhotoImage, messagebox
from tabs.main_tab import MainTab
from tabs.saved_tab import SavedTab
from tabs.master_password_dialog import prompt_master_password
from database.database import init_db


def main():
    init_db()

    window = tk.Tk()
    window.title("Password Manager")
    window.geometry("500x500")
    window.withdraw()

    if not prompt_master_password(window):
        messagebox.showwarning("Aviso", "Senha mestre necessária. O programa será encerrado.")
        window.destroy()
        return

    window.deiconify()

    canvas = Canvas(window, width=100, height=100)
    logo_image = PhotoImage(file="assets/logo.png")
    logo_image_resized = logo_image.subsample(2, 2)
    canvas.create_image(50, 50, image=logo_image_resized)
    canvas.pack()

    tab_control = ttk.Notebook(window)

    saved_tab = SavedTab(tab_control)
    MainTab(tab_control, saved_tab)

    tab_control.pack(expand=1, fill="both")

    window.mainloop()

if __name__ == "__main__":
    main()
