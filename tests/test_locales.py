from __future__ import annotations

import locales as lang
from locales import en, es, pt_br


def test_init_uses_explicit_language() -> None:
    lang.init("es")

    assert lang.current_lang() == "es"
    assert lang.t("tab_saved") == "Guardados"


def test_init_uses_saved_language_when_none(monkeypatch) -> None:
    monkeypatch.setattr(lang, "_load_saved_lang", lambda: "pt_br")

    lang.init()
    assert lang.current_lang() == "pt_br"
    assert lang.t("tab_saved") == "Salvos"


def test_missing_translation_key_has_bracket_fallback() -> None:
    lang.init("en")
    assert lang.t("missing_key_example") == "[missing_key_example]"


def test_set_language_persists_and_notifies_callbacks(monkeypatch) -> None:
    captured = {"saved": None, "calls": 0}

    def _fake_save(code: str) -> None:
        captured["saved"] = code

    monkeypatch.setattr(lang, "_save_lang", _fake_save)
    lang.init("en")
    lang.register_callback(lambda: captured.__setitem__("calls", captured["calls"] + 1))

    lang.set_language("es")

    assert lang.current_lang() == "es"
    assert captured["saved"] == "es"
    assert captured["calls"] == 1


def test_all_locale_files_have_same_translation_keys() -> None:
    assert set(en.STRINGS) == set(pt_br.STRINGS) == set(es.STRINGS)
