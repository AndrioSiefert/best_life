import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "best_life.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                age INTEGER,
                gender TEXT,
                state TEXT,
                phone TEXT,
                total_value REAL,
                total_items INTEGER
            );
            CREATE TABLE IF NOT EXISTS decisions (
                customer_id INTEGER PRIMARY KEY,
                tracks TEXT NOT NULL,
                confirmed_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS settings (
                name TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                customer_name TEXT NOT NULL,
                track TEXT NOT NULL,
                message_index INTEGER NOT NULL,
                scheduled_date TEXT NOT NULL,
                message TEXT NOT NULL,
                request TEXT NOT NULL,
                UNIQUE(customer_id, track, message_index, scheduled_date)
            );
        """)
