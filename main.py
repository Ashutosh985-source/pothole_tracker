from modules import gui, db
import os

# Create database folder if not exists
if not os.path.exists("database"):
    os.makedirs("database")

db.init_db()
gui.run_app()
