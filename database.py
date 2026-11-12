import sqlite3

conn = sqlite3.connect("grab_character.db")
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS waifus (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        source TEXT,
        rarity TEXT,
        price INTEGER,
        image_url TEXT
    )
    """)
    defaults = {
        "tap_limit": "100",
        "tap_cooldown": "60",
        "daily_reward": "50",
        "bg_blur": "6",
        "blue_shade": "0.35",
        "ad_text": "Yangi anime kanallarga obuna bo'ling!",
        "ad_link": "https://t.me/",
        "ad_trigger": "all",
        "drop_basic": "60",
        "drop_rare": "25",
        "drop_divine": "10",
        "drop_season": "5"
    }
    for k, v in defaults.items():
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (k, v))
    conn.commit()

def set_setting(key, value):
    cursor.execute("REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
    conn.commit()

def get_setting(key):
    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = cursor.fetchone()
    return row[0] if row else None
