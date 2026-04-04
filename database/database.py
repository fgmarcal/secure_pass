import sqlite3
from pathlib import Path
from database.crypto import encrypt_password, decrypt_password

DB_NAME = Path(__file__).parent / "data.db"

def init_db() -> None:
    """Creates the database and table if they do not exist."""
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
        conn.commit()

def save_to_db(website: str, email: str, password: str) -> None:
    """Saves data to the SQLite database with the password encrypted."""
    encrypted = encrypt_password(password)
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO data (website, email, password) VALUES (?, ?, ?)", (website, email, encrypted))
        conn.commit()

def fetch_all() -> list[tuple[str, str, str]]:
    """Returns all records from the database with passwords decrypted."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT website, email, password FROM data")
        rows = cursor.fetchall()
    return [(website, email, decrypt_password(pwd)) for website, email, pwd in rows]

def delete_from_db(website: str, email: str) -> None:
    """Deletes a record from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM data WHERE website = ? AND email = ?", (website, email))
        conn.commit()
