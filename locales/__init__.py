LANGUAGES: dict[str, str] = {
    "en": "English",
    "pt_br": "Português (Brasil)",
    "es": "Español",
}

_strings: dict[str, str] = {}
_current_lang: str = "en"
_callbacks: list = []


def _load_strings(lang_code: str) -> dict[str, str]:
    if lang_code == "pt_br":
        from locales.pt_br import STRINGS
    elif lang_code == "es":
        from locales.es import STRINGS
    else:
        from locales.en import STRINGS
    return STRINGS


def _load_saved_lang() -> str:
    try:
        from database.database import get_setting
        return get_setting("language", "en")
    except Exception:
        return "en"


def _save_lang(lang_code: str) -> None:
    try:
        from database.database import set_setting
        set_setting("language", lang_code)
    except Exception:
        pass


def init(lang_code: str | None = None) -> None:
    """Load language strings. Call once at startup before building the UI."""
    global _current_lang, _strings
    if lang_code is None:
        lang_code = _load_saved_lang()
    _current_lang = lang_code
    _strings = _load_strings(lang_code)


def set_language(lang_code: str) -> None:
    """Switch the active language and notify all registered callbacks."""
    global _current_lang, _strings
    _current_lang = lang_code
    _strings = _load_strings(lang_code)
    _save_lang(lang_code)
    for cb in _callbacks:
        cb()


def t(key: str, **kwargs: str) -> str:
    """Return the translated string for *key*, optionally formatting with kwargs."""
    text = _strings.get(key, f"[{key}]")
    if kwargs:
        return text.format(**kwargs)
    return text


def register_callback(cb) -> None:
    """Register a callable that is invoked whenever the language changes."""
    _callbacks.append(cb)


def current_lang() -> str:
    return _current_lang
