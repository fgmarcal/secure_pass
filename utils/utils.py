import random
import tkinter as tk

def copy_password(password):
    """Copia a senha para o clipboard."""
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()

def password_generator():
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"
    symbols = "!#$%&()*+"

    password_list = (
        random.choices(letters, k=random.randint(8, 10)) +
        random.choices(symbols, k=random.randint(2, 4)) +
        random.choices(numbers, k=random.randint(2, 4))
    )

    random.shuffle(password_list)
    return "".join(password_list)

def validate_entries(**kw):
    website_value = kw.get("website")
    email_value = kw.get("email")
    password_value = kw.get("password")
    if len(website_value) == 0 or len(email_value) == 0 or len(password_value) == 0:
        return False
    return True