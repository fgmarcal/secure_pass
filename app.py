import tkinter as tk
from tkinter import ttk, Canvas, PhotoImage, messagebox
from pathlib import Path
import locales as lang
from tabs.main_tab import MainTab
from tabs.saved_tab import SavedTab
from tabs.settings_tab import SettingsTab
from tabs.master_password_dialog import prompt_master_password
from database.database import init_db

ASSETS_DIR = Path(__file__).parent / "assets"


def main():
    init_db()
    lang.init()

    window = tk.Tk()
    window.title(lang.t("app_title"))
    window.geometry("600x600")
    window.withdraw()

    if not prompt_master_password(window):
        messagebox.showwarning(
            lang.t("app_warning_master_required_title"),
            lang.t("app_warning_master_required_msg"),
        )
        window.destroy()
        return

    window.deiconify()

    canvas = Canvas(window, width=100, height=100)
    logo_image = PhotoImage(file=str(ASSETS_DIR / "logo.png"))
    logo_image_resized = logo_image.subsample(2, 2)
    canvas.create_image(50, 50, image=logo_image_resized)
    canvas.pack()

    tab_control = ttk.Notebook(window)

    saved_tab = SavedTab(tab_control)
    MainTab(tab_control, saved_tab)
    SettingsTab(tab_control)

    tab_control.pack(expand=1, fill="both")

    window.mainloop()

if __name__ == "__main__":
    main()
