import tkinter as tk


class ButtonStyle(tk.Button):
    """Styled button subclass."""
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            font=("Arial", 10, "bold"),
            bd=3,
            bg="#3E5879",
            fg="#F5EFE7",
            relief="raised",
            activebackground="#F5EFE7",
            activeforeground="#3E5879",
            **kwargs,
        )

