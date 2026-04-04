import tkinter as tk
from tkinter import Canvas, PhotoImage, messagebox
from pathlib import Path
import locales as lang
from styles.theme import apply_theme, BG
from styles.rounded_notebook import RoundedNotebook
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
    window.geometry("520x600")
    window.withdraw()
    apply_theme(window)

    if not prompt_master_password(window):
        messagebox.showwarning(
            lang.t("app_warning_master_required_title"),
            lang.t("app_warning_master_required_msg"),
        )
        window.destroy()
        return

    window.deiconify()

    canvas = Canvas(window, width=80, height=80, bg=BG, highlightthickness=0)
    logo_image = PhotoImage(file=str(ASSETS_DIR / "logo.png"))
    logo_image_resized = logo_image.subsample(2, 2)
    canvas.create_image(40, 40, image=logo_image_resized)
    canvas.pack(pady=(12, 0))

    tab_control = RoundedNotebook(window)

    saved_tab = SavedTab(tab_control)
    MainTab(tab_control, saved_tab)
    SettingsTab(tab_control)

    tab_control.pack(expand=1, fill="both", padx=0, pady=(8, 0))

    window.mainloop()

if __name__ == "__main__":
    main()
