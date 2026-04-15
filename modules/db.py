import sqlite3
import os


class Database:
    def __init__(self, db_path="database/potholes.db"):
        self.db_path = db_path

        # create folder if not exists
        os.makedirs("database", exist_ok=True)

        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_path)
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

    def insert(self, location, image_path):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO potholes(location, image_path) VALUES (?, ?)",
            (location, image_path)
        )

        conn.commit()
        conn.close()

    def fetch_all(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute("SELECT * FROM potholes")
        data = cur.fetchall()

        conn.close()
        return data
