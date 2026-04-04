import sqlite3
from pathlib import Path
from database.crypto import encrypt_password, decrypt_password

DB_NAME = Path(__file__).parent / "data.db"

def init_db():
    """Cria o banco de dados e a tabela caso não existam."""
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

def save_to_db(website, email, password):
    """Salva os dados no banco de dados SQLite com a senha encriptada."""
    encrypted = encrypt_password(password)
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO data (website, email, password) VALUES (?, ?, ?)", (website, email, encrypted))
        conn.commit()

def fetch_all():
    """Retorna todos os registros do banco de dados com as senhas desencriptadas."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT website, email, password FROM data")
        rows = cursor.fetchall()
    return [(website, email, decrypt_password(pwd)) for website, email, pwd in rows]

def delete_from_db(website, email):
    """Exclui um registro do banco de dados."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM data WHERE website = ? AND email = ?", (website, email))
        conn.commit()
