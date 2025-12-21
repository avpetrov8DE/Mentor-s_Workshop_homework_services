import os
import sqlite3
from contextlib import contextmanager

DATA_DIR = os.getenv("DATA_DIR", "/data")
DB_PATH = os.getenv("DB_PATH", os.path.join(DATA_DIR, "todo.db"))

def init_db() -> None:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'Несрочная',
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            CHECK (status IN ('Неотложная', 'Несрочная'))
        )
        """)
        conn.commit()

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
