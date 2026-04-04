from __future__ import annotations

import pytest

import database.crypto as crypto
import database.database as db
import locales as lang


@pytest.fixture(autouse=True)
def reset_locale_state() -> None:
    """Avoid state leakage between tests due module-level globals."""
    lang._callbacks.clear()
    lang._strings = {}
    lang._current_lang = "en"
    yield
    lang._callbacks.clear()
    lang._strings = {}
    lang._current_lang = "en"


@pytest.fixture
def isolated_storage(tmp_path, monkeypatch):
    """
    Redirect database and salt files to a temporary location per test.
    This keeps tests isolated from real project data.
    """
    db_path = tmp_path / "data.db"
    salt_path = tmp_path / "salt.key"

    monkeypatch.setattr(db, "DB_NAME", db_path)
    monkeypatch.setattr(crypto, "SALT_FILE", salt_path)

    crypto._fernet = None
    db.init_db()

    yield {"db_path": db_path, "salt_path": salt_path}

    crypto._fernet = None
