import os
import base64
from pathlib import Path
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet, InvalidToken

SALT_FILE = Path(__file__).parent / "salt.key"

_fernet: Fernet | None = None


def _load_or_create_salt() -> bytes:
    if SALT_FILE.exists():
        return SALT_FILE.read_bytes()
    salt = os.urandom(16)
    SALT_FILE.write_bytes(salt)
    return salt


def init_crypto(master_password: str) -> None:
    """Derives a Fernet key from the master password and initialises the module."""
    global _fernet
    salt = _load_or_create_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480_000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    _fernet = Fernet(key)


def encrypt_password(plaintext: str) -> str:
    if _fernet is None:
        raise RuntimeError("Crypto not initialised. Call init_crypto() first.")
    return _fernet.encrypt(plaintext.encode()).decode()


def decrypt_password(token: str) -> str:
    if _fernet is None:
        raise RuntimeError("Crypto not initialised. Call init_crypto() first.")
    try:
        return _fernet.decrypt(token.encode()).decode()
    except InvalidToken:
        return "[decryption failed]"


def is_initialised() -> bool:
    return _fernet is not None
