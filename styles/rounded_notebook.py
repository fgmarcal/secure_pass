import tkinter as tk
from tkinter.font import Font as TkFont
from styles.theme import BG, SURFACE, SURFACE2, TEXT, TEXT_MUTED, FONT

_ACTIVE   = dict(font_size=11, bold=True,  padx=20, pady=10, bg=SURFACE2, fg=TEXT)
_INACTIVE = dict(font_size=10, bold=False, padx=16, pady=7,  bg=SURFACE,  fg=TEXT_MUTED)

TAB_BAR_HEIGHT = 52


class _TabPill(tk.Canvas):
    """A single rounded tab pill."""

    def __init__(self, parent, text: str, active: bool, command, **kwargs):
        self._text_str = text
        self._command  = command
        self._active   = active
        self._radius   = 12
        self._hovering = False
        super().__init__(parent, bg=BG, highlightthickness=0, cursor="hand2", **kwargs)
        self._render()
        self.bind("<ButtonPress-1>", lambda e: self._command())
        self.bind("<Enter>",         self._on_enter)
        self.bind("<Leave>",         self._on_leave)

    def _style(self) -> dict:
        return _ACTIVE if self._active else _INACTIVE

    def _render(self, hover: bool = False) -> None:
        s  = self._style()
        bg = s["bg"]
        fg = s["fg"]
        if hover and not self._active:
            bg = SURFACE2
            fg = TEXT
        font   = TkFont(family=FONT, size=s["font_size"], weight="bold" if s["bold"] else "normal")
        padx   = s["padx"]
        pady   = s["pady"]
        tw     = font.measure(self._text_str)
        th     = font.metrics("linespace")
        w, h   = tw + padx * 2, th + pady * 2
        self.configure(width=w, height=h)
        self.delete("all")
        r   = self._radius
        pts = [r,0, w-r,0, w,0, w,r, w,h-r, w,h, w-r,h, r,h, 0,h, 0,h-r, 0,r, 0,0]
        self.create_polygon(pts, smooth=True, fill=bg, outline="")
        self.create_text(w // 2, h // 2, text=self._text_str, fill=fg, font=font)

    def set_active(self, active: bool) -> None:
        self._active = active
        self._render()

    def set_text(self, text: str) -> None:
        self._text_str = text
        self._render()

    def _on_enter(self, _e):
        self._hovering = True
        self._render(hover=True)

    def _on_leave(self, _e):
        self._hovering = False
        self._render(hover=False)


class RoundedNotebook(tk.Frame):
    """
    Drop-in replacement for ttk.Notebook with rounded pill tabs.
    The active tab is visually larger than the inactive ones.
    Supports the same .add() and .tab() interface used by the app's tab classes.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=BG, **kwargs)
        self._tabs: list[dict] = []

        self._tab_bar = tk.Frame(self, bg=BG, height=TAB_BAR_HEIGHT)
        self._tab_bar.pack(fill="x", side="top", padx=8)
        self._tab_bar.pack_propagate(False)

    def add(self, frame: tk.Widget, text: str = "") -> None:
        btn = _TabPill(
            self._tab_bar,
            text=text,
            active=False,
            command=lambda f=frame: self._select(f),
        )
        btn.pack(side="left", padx=(0, 6), pady=8, anchor="s")
        self._tabs.append({"frame": frame, "text": text, "btn": btn})
        if len(self._tabs) == 1:
            self._select(frame)
        else:
            frame.place_forget()

    def tab(self, frame: tk.Widget, text: str = "", **_) -> None:
        for t in self._tabs:
            if t["frame"] is frame:
                t["text"] = text
                t["btn"].set_text(text)
                return

    def _select(self, active_frame: tk.Widget) -> None:
        for t in self._tabs:
            is_active = t["frame"] is active_frame
            t["btn"].set_active(is_active)
            if is_active:
                t["frame"].place(
                    in_=self,
                    x=0, y=TAB_BAR_HEIGHT,
                    relwidth=1, relheight=1,
                    height=-TAB_BAR_HEIGHT,
                )
            else:
                t["frame"].place_forget()
