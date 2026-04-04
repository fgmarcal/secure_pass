import tkinter as tk
from tkinter import ttk

# Color palette
BG         = "#111827"   # main background   (gray-900)
SURFACE    = "#1f2937"   # panels / cards     (gray-800)
SURFACE2   = "#374151"   # subtle dividers    (gray-700)
ACCENT     = "#6366f1"   # indigo-500
ACCENT_HOV = "#4f46e5"   # indigo-600
TEXT       = "#f9fafb"   # primary text       (gray-50)
TEXT_MUTED = "#9ca3af"   # secondary text     (gray-400)
ENTRY_BG   = "#1f2937"
BORDER     = "#374151"
SUCCESS    = "#10b981"
ERROR      = "#f43f5e"
WARNING    = "#f59e0b"
FONT       = "Segoe UI"


def apply_theme(window: tk.Tk) -> None:
    """Apply the dark modern theme to the entire application."""
    window.configure(bg=BG)

    # --- Global tk widget defaults (apply before any widget is created) ---
    window.option_add("*Font",                    (FONT, 10))
    window.option_add("*Background",              BG)
    window.option_add("*Foreground",              TEXT)

    window.option_add("*Label.Background",        BG)
    window.option_add("*Label.Foreground",        TEXT)

    window.option_add("*Entry.Background",        ENTRY_BG)
    window.option_add("*Entry.Foreground",        TEXT)
    window.option_add("*Entry.InsertBackground",  TEXT)
    window.option_add("*Entry.SelectBackground",  ACCENT)
    window.option_add("*Entry.SelectForeground",  TEXT)
    window.option_add("*Entry.Relief",            "flat")
    window.option_add("*Entry.BorderWidth",       0)
    window.option_add("*Entry.HighlightThickness", 1)
    window.option_add("*Entry.HighlightBackground", BORDER)
    window.option_add("*Entry.HighlightColor",    ACCENT)

    window.option_add("*Button.Background",       ACCENT)
    window.option_add("*Button.Foreground",       TEXT)
    window.option_add("*Button.ActiveBackground", ACCENT_HOV)
    window.option_add("*Button.ActiveForeground", TEXT)
    window.option_add("*Button.Relief",           "flat")
    window.option_add("*Button.BorderWidth",      0)
    window.option_add("*Button.Cursor",           "hand2")

    window.option_add("*Toplevel.Background",     BG)
    window.option_add("*Frame.Background",        BG)

    # --- ttk style ---
    style = ttk.Style(window)
    style.theme_use("clam")

    style.configure("TFrame",      background=BG)
    style.configure("TLabel",      background=BG,       foreground=TEXT, font=(FONT, 10))

    style.configure(
        "TNotebook",
        background=BG,
        borderwidth=0,
        tabmargins=[0, 0, 0, 0],
    )
    style.configure(
        "TNotebook.Tab",
        background=SURFACE,
        foreground=TEXT_MUTED,
        padding=[16, 8],
        font=(FONT, 10),
        borderwidth=0,
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", SURFACE2), ("active", SURFACE2)],
        foreground=[("selected", TEXT),     ("active",  TEXT)],
        expand=[("selected", [0, 0, 0, 0])],
    )

    style.configure(
        "Treeview",
        background=SURFACE,
        foreground=TEXT,
        fieldbackground=SURFACE,
        rowheight=34,
        font=(FONT, 10),
        borderwidth=0,
        relief="flat",
    )
    style.configure(
        "Treeview.Heading",
        background=SURFACE2,
        foreground=TEXT_MUTED,
        font=(FONT, 9, "bold"),
        relief="flat",
        borderwidth=0,
    )
    style.map(
        "Treeview",
        background=[("selected", ACCENT)],
        foreground=[("selected", TEXT)],
    )

    style.configure(
        "Vertical.TScrollbar",
        background=SURFACE2,
        troughcolor=SURFACE,
        borderwidth=0,
        arrowcolor=TEXT_MUTED,
        relief="flat",
    )

    style.configure(
        "TCombobox",
        fieldbackground=ENTRY_BG,
        background=SURFACE2,
        foreground=TEXT,
        arrowcolor=TEXT_MUTED,
        insertcolor=TEXT,
        borderwidth=1,
        relief="flat",
        padding=[6, 4],
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", ENTRY_BG)],
        foreground=[("readonly",      TEXT)],
        selectbackground=[("readonly", ENTRY_BG)],
        selectforeground=[("readonly", TEXT)],
        bordercolor=[("focus", ACCENT), ("!focus", BORDER)],
    )
