import tkinter as tk
from tkinter import ttk
import locales as lang
from styles.button_style import ButtonStyle


class SettingsTab:
    def __init__(self, tab_control: ttk.Notebook) -> None:
        self.tab_control = tab_control
        self.frame = ttk.Frame(tab_control)
        tab_control.add(self.frame, text=lang.t("tab_settings"))
        self._build(self.frame)
        lang.register_callback(self._retranslate)

    def _build(self, parent: ttk.Frame) -> None:
        wrapper = ttk.Frame(parent)
        wrapper.pack(expand=True)

        self.lbl_language = tk.Label(wrapper, text=lang.t("label_language"), font=("Arial", 10, "bold"))
        self.lbl_language.grid(row=0, column=0, padx=10, pady=20, sticky="e")

        self._lang_var = tk.StringVar(value=lang.LANGUAGES[lang.current_lang()])
        self.lang_combo = ttk.Combobox(
            wrapper,
            textvariable=self._lang_var,
            values=list(lang.LANGUAGES.values()),
            state="readonly",
            width=22,
        )
        self.lang_combo.grid(row=0, column=1, padx=10, pady=20, sticky="w")
        self.lang_combo.bind("<<ComboboxSelected>>", self._on_language_change)

    def _on_language_change(self, _event=None) -> None:
        selected_label = self._lang_var.get()
        code = next(k for k, v in lang.LANGUAGES.items() if v == selected_label)
        lang.set_language(code)

    def _retranslate(self) -> None:
        self.tab_control.tab(self.frame, text=lang.t("tab_settings"))
        self.lbl_language.config(text=lang.t("label_language"))
        self._lang_var.set(lang.LANGUAGES[lang.current_lang()])
