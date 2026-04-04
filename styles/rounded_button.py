import tkinter as tk
from tkinter.font import Font as TkFont
from styles.theme import ACCENT, ACCENT_HOV, TEXT, BG, FONT


class RoundedButton(tk.Canvas):
    """A flat, fully-rounded-corner button drawn on a Canvas."""

    def __init__(
        self,
        parent,
        text: str = "",
        command=None,
        radius: int = 10,
        bg_color: str = ACCENT,
        bg_hover: str = ACCENT_HOV,
        fg_color: str = TEXT,
        padx: int = 16,
        pady: int = 8,
        font_size: int = 10,
        bold: bool = True,
        **kwargs,
    ):
        self._text_str = text
        self._command = command
        self._radius = radius
        self._bg_color = bg_color
        self._bg_hover = bg_hover
        self._fg_color = fg_color
        self._padx = padx
        self._pady = pady
        self._font = TkFont(family=FONT, size=font_size, weight="bold" if bold else "normal")
        self._hovering = False

        w, h = self._measure(text)
        super().__init__(
            parent,
            width=w,
            height=h,
            bg=kwargs.pop("bg", BG),
            highlightthickness=0,
            cursor="hand2",
            **kwargs,
        )
        self._render(self._bg_color)

        self.bind("<ButtonPress-1>",   self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>",           self._on_enter)
        self.bind("<Leave>",           self._on_leave)

    def _measure(self, text: str) -> tuple[int, int]:
        tw = self._font.measure(text)
        th = self._font.metrics("linespace")
        return tw + self._padx * 2, th + self._pady * 2

    def _render(self, fill: str) -> None:
        self.delete("all")
        w = int(self["width"])
        h = int(self["height"])
        r = self._radius
        pts = [r,0, w-r,0, w,0, w,r, w,h-r, w,h, w-r,h, r,h, 0,h, 0,h-r, 0,r, 0,0]
        self.create_polygon(pts, smooth=True, fill=fill, outline="")
        self.create_text(w // 2, h // 2, text=self._text_str, fill=self._fg_color, font=self._font)

    def _on_press(self, _e):
        self._render(self._bg_hover)

    def _on_release(self, _e):
        self._render(self._bg_hover if self._hovering else self._bg_color)
        if self._command:
            self._command()

    def _on_enter(self, _e):
        self._hovering = True
        self._render(self._bg_hover)

    def _on_leave(self, _e):
        self._hovering = False
        self._render(self._bg_color)

    def config(self, **kwargs):
        if "text" in kwargs:
            self._text_str = kwargs.pop("text")
            w, h = self._measure(self._text_str)
            tk.Canvas.config(self, width=w, height=h)
            self._render(self._bg_hover if self._hovering else self._bg_color)
        if kwargs:
            tk.Canvas.config(self, **kwargs)

    configure = config
