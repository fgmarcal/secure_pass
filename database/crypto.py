import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet, InvalidToken
from utils.paths import get_app_data_dir

SALT_FILE = get_app_data_dir() / "salt.key"
MASTER_VERIFIER_PAYLOAD = "secure-pass-verifier-v1"

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
    except InvalidToken as exc:
        raise ValueError("Password decryption failed.") from exc


def create_master_verifier() -> str:
    """Returns an encrypted verifier token for the current derived key."""
    if _fernet is None:
        raise RuntimeError("Crypto not initialised. Call init_crypto() first.")
    return _fernet.encrypt(MASTER_VERIFIER_PAYLOAD.encode()).decode()


def verify_master_password(verifier_token: str) -> bool:
    """Checks if the current derived key can decrypt the stored verifier token."""
    if _fernet is None:
        raise RuntimeError("Crypto not initialised. Call init_crypto() first.")
    try:
        payload = _fernet.decrypt(verifier_token.encode()).decode()
    except (InvalidToken, UnicodeDecodeError):
        return False
    return payload == MASTER_VERIFIER_PAYLOAD


def is_initialised() -> bool:
    return _fernet is not None
