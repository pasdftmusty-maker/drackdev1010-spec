import sqlite3

def get_db():
    conn = sqlite3.connect("bot.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        moedas INTEGER DEFAULT 0,
        rep INTEGER DEFAULT 0,
        ultimo_daily TEXT
    )
    """)
    conn.commit()
    conn.close()

def get_or_create_user(user_id):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    if not user:
        conn.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        user = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return user
