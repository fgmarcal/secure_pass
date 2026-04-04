import sqlite3
from pathlib import Path
from database.crypto import encrypt_password, decrypt_password

DB_NAME = Path(__file__).parent / "data.db"

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

def save_to_db(website: str, email: str, password: str) -> None:
    """Saves data to the SQLite database with the password encrypted."""
    encrypted = encrypt_password(password)
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO data (website, email, password) VALUES (?, ?, ?)", (website, email, encrypted))
        conn.commit()

def fetch_all() -> list[tuple[int, str, str, str]]:
    """Returns all records from the database with passwords decrypted."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, website, email, password FROM data")
        rows = cursor.fetchall()
    return [(row_id, website, email, decrypt_password(pwd)) for row_id, website, email, pwd in rows]

def delete_from_db(row_id: int) -> None:
    """Deletes a record from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM data WHERE id = ?", (row_id,))
        conn.commit()
