from __future__ import annotations

import pytest

import database.crypto as crypto


def test_encrypt_requires_init(isolated_storage) -> None:
    with pytest.raises(RuntimeError):
        crypto.encrypt_password("secret")


def test_decrypt_requires_init(isolated_storage) -> None:
    with pytest.raises(RuntimeError):
        crypto.decrypt_password("not-a-token")


def test_init_creates_salt_file(isolated_storage) -> None:
    salt_path = isolated_storage["salt_path"]
    assert not salt_path.exists()

    crypto.init_crypto("master-pass")

    assert salt_path.exists()
    assert len(salt_path.read_bytes()) == 16


def test_encrypt_decrypt_round_trip(isolated_storage) -> None:
    crypto.init_crypto("master-pass")
    encrypted = crypto.encrypt_password("my-secret-password")

    assert encrypted != "my-secret-password"
    assert crypto.decrypt_password(encrypted) == "my-secret-password"


def test_decrypt_with_wrong_password_raises_value_error(isolated_storage) -> None:
    crypto.init_crypto("correct-password")
    encrypted = crypto.encrypt_password("my-secret-password")

    crypto.init_crypto("wrong-password")
    with pytest.raises(ValueError):
        crypto.decrypt_password(encrypted)


def test_master_verifier_validates_only_matching_password(isolated_storage) -> None:
    crypto.init_crypto("correct-password")
    verifier = crypto.create_master_verifier()
    assert crypto.verify_master_password(verifier) is True

    crypto.init_crypto("wrong-password")
    assert crypto.verify_master_password(verifier) is False
