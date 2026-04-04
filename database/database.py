import sqlite3

DB_NAME = "database/data.db"

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
    """Salva os dados no banco de dados SQLite."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO data (website, email, password) VALUES (?, ?, ?)", (website, email, password))
        conn.commit()

def fetch_all():
    """Retorna todos os registros do banco de dados."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT website, email, password FROM data")
        return cursor.fetchall()

def delete_from_db(website, email):
    """Exclui um registro do banco de dados."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM data WHERE website = ? AND email = ?", (website, email))
        conn.commit()
