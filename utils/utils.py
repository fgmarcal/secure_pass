import secrets
import string
import tkinter as tk


def copy_to_clipboard(widget: tk.Misc, password: str) -> None:
    """Copies the password to the clipboard using the existing Tk widget."""
    widget.clipboard_clear()
    widget.clipboard_append(password)
    widget.update()


def password_generator() -> str:
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


def validate_entries(website: str, email: str, password: str) -> bool:
    return bool(website and email and password)
