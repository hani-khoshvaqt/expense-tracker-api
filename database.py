import sqlite3

DB_NAME = "expense.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
                 CREATE TABLE IF NOT EXISTS expenses (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     title TEXT NOT NULL,
                     amount REAL NOT NULL,
                     category TEXT NOT NULL,
                     date TEXT NOT NULL
                 )
            """)
    conn.commit()
    conn.close()