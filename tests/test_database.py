from __future__ import annotations

import database.crypto as crypto
import database.database as db


def test_settings_round_trip(isolated_storage) -> None:
    assert db.get_setting("language", "en") == "en"

    db.set_setting("language", "es")
    assert db.get_setting("language", "en") == "es"


def test_master_verifier_round_trip(isolated_storage) -> None:
    crypto.init_crypto("master-pass")
    verifier = crypto.create_master_verifier()

    db.set_master_verifier(verifier)
    assert db.get_master_verifier() == verifier


def test_save_and_fetch_returns_decrypted_password(isolated_storage) -> None:
    crypto.init_crypto("master-pass")
    db.save_to_db("example.com", "user@example.com", "p@ssw0rd")

    rows = db.fetch_all()
    assert len(rows) == 1
    row_id, website, email, password = rows[0]
    assert isinstance(row_id, int)
    assert website == "example.com"
    assert email == "user@example.com"
    assert password == "p@ssw0rd"


def test_delete_by_row_id_removes_only_selected_row(isolated_storage) -> None:
    crypto.init_crypto("master-pass")
    db.save_to_db("example.com", "user@example.com", "secret-1")
    db.save_to_db("example.com", "user@example.com", "secret-2")

    rows = db.fetch_all()
    assert len(rows) == 2
    first_id = rows[0][0]
    second_id = rows[1][0]

    db.delete_from_db(first_id)
    remaining_rows = db.fetch_all()

    assert len(remaining_rows) == 1
    assert remaining_rows[0][0] == second_id


def test_has_saved_passwords_tracks_empty_and_non_empty_db(isolated_storage) -> None:
    assert db.has_saved_passwords() is False

    crypto.init_crypto("master-pass")
    db.save_to_db("example.com", "user@example.com", "secret")
    assert db.has_saved_passwords() is True


def test_has_any_decryptable_password_when_key_matches(isolated_storage) -> None:
    crypto.init_crypto("master-pass")
    db.save_to_db("example.com", "user@example.com", "secret")

    assert db.has_any_decryptable_password() is True


def test_has_any_decryptable_password_when_key_does_not_match(isolated_storage) -> None:
    crypto.init_crypto("correct-pass")
    db.save_to_db("example.com", "user@example.com", "secret")

    crypto.init_crypto("wrong-pass")
    assert db.has_any_decryptable_password() is False


def test_fetch_all_marks_undecryptable_rows_as_none(isolated_storage) -> None:
    crypto.init_crypto("correct-pass")
    db.save_to_db("example.com", "user@example.com", "secret")

    crypto.init_crypto("wrong-pass")
    rows = db.fetch_all()

    assert len(rows) == 1
    assert rows[0][3] is None
