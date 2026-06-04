import sqlite3
from pathlib import Path
from database.crypto import encrypt_password, decrypt_password

DB_NAME = Path(__file__).parent / "data.db"
MASTER_VERIFIER_KEY = "master_verifier"

def init_db() -> None:
    """Creates the database and tables if they do not exist."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        conn.commit()


def get_setting(key: str, default: str = "") -> str:
    """Returns the value for a settings key, or *default* if not found."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
    return row[0] if row else default


def set_setting(key: str, value: str) -> None:
    """Inserts or updates a settings key-value pair."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )
        conn.commit()


def get_master_verifier() -> str:
    """Returns the encrypted master-password verifier token, if present."""
    return get_setting(MASTER_VERIFIER_KEY, "")


def set_master_verifier(verifier_token: str) -> None:
    """Persists the encrypted master-password verifier token."""
    set_setting(MASTER_VERIFIER_KEY, verifier_token)


def has_saved_passwords() -> bool:
    """Returns True when there is at least one credential row."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM data LIMIT 1")
        return cursor.fetchone() is not None


def has_any_decryptable_password() -> bool:
    """
    Returns True when at least one encrypted password can be decrypted with the
    currently initialised key.
    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM data")
        rows = cursor.fetchall()
    for (encrypted_password,) in rows:
        try:
            decrypt_password(encrypted_password)
            return True
        except ValueError:
            continue
    return False


def save_to_db(website: str, email: str, password: str) -> None:
    """Saves data to the SQLite database with the password encrypted."""
    encrypted = encrypt_password(password)
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO data (website, email, password) VALUES (?, ?, ?)", (website, email, encrypted))
        conn.commit()


def update_in_db(row_id: int, website: str, email: str, password: str) -> None:
    """Updates an existing record with the password encrypted."""
    encrypted = encrypt_password(password)
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE data SET website = ?, email = ?, password = ? WHERE id = ?",
            (website, email, encrypted, row_id),
        )
        conn.commit()


def fetch_all() -> list[tuple[int, str, str, str | None]]:
    """Returns all records from the database with passwords decrypted."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, website, email, password FROM data")
        rows = cursor.fetchall()
    decrypted_rows: list[tuple[int, str, str, str | None]] = []
    for row_id, website, email, encrypted_password in rows:
        try:
            decrypted = decrypt_password(encrypted_password)
        except ValueError:
            decrypted = None
        decrypted_rows.append((row_id, website, email, decrypted))
    return decrypted_rows

def delete_from_db(row_id: int) -> None:
    """Deletes a record from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM data WHERE id = ?", (row_id,))
        conn.commit()
