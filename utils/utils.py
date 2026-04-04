import secrets
import string
import tkinter as tk

def copy_password(password):
    """Copia a senha para o clipboard."""
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()

def password_generator():
    letters = string.ascii_letters
    numbers = string.digits
    symbols = string.punctuation

    password_list = (
        [secrets.choice(letters) for _ in range(secrets.randbelow(3) + 8)] +
        [secrets.choice(symbols) for _ in range(secrets.randbelow(3) + 2)] +
        [secrets.choice(numbers) for _ in range(secrets.randbelow(3) + 2)]
    )

    secrets.SystemRandom().shuffle(password_list)
    return "".join(password_list)

def validate_entries(**kw):
    website_value = kw.get("website")
    email_value = kw.get("email")
    password_value = kw.get("password")
    if len(website_value) == 0 or len(email_value) == 0 or len(password_value) == 0:
        return False
    return True