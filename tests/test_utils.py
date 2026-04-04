from __future__ import annotations

import string

from utils.utils import copy_to_clipboard, password_generator, validate_entries


class ClipboardStub:
    def __init__(self) -> None:
        self.value = None
        self.clear_called = 0
        self.update_called = 0

    def clipboard_clear(self) -> None:
        self.clear_called += 1
        self.value = None

    def clipboard_append(self, value: str) -> None:
        self.value = value

    def update(self) -> None:
        self.update_called += 1


def test_copy_to_clipboard_uses_widget_api() -> None:
    widget = ClipboardStub()
    copy_to_clipboard(widget, "secret")

    assert widget.clear_called == 1
    assert widget.value == "secret"
    assert widget.update_called == 1


def test_password_generator_builds_expected_shape() -> None:
    password = password_generator()

    assert 12 <= len(password) <= 18
    assert any(ch.isalpha() for ch in password)
    assert any(ch.isdigit() for ch in password)
    assert any(ch in string.punctuation for ch in password)


def test_validate_entries_requires_non_empty_values() -> None:
    assert validate_entries("example.com", "user@example.com", "secret") is True
    assert validate_entries("", "user@example.com", "secret") is False
    assert validate_entries("example.com", "", "secret") is False
    assert validate_entries("example.com", "user@example.com", "") is False
