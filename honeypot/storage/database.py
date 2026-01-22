import sqlite3
from pathlib import Path

DB_PATH = Path("data/honeypot.db")

def get_connection():
    return sqlite3.connect(DB_PATH)
import sqlite3
from pathlib import Path

DB_PATH = Path("data/honeypot.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        ip TEXT,
        port INTEGER,
        start_time TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        event_type TEXT,
        payload TEXT,
        timestamp TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS features (
        session_id TEXT,
        feature_name TEXT,
        feature_value REAL
    )
    """)

    conn.commit()
    conn.close()

