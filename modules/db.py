import sqlite3

DB_PATH = "database/potholes.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS potholes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT,
        image_path TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_data(location, image_path):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO potholes(location, image_path) VALUES (?, ?)",
        (location, image_path)
    )
    conn.commit()
    conn.close()

def fetch_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM potholes")
    rows = cur.fetchall()
    conn.close()
    return rows
