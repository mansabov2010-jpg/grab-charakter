import sqlite3

conn = sqlite3.connect("grab_character.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    # Sozlamalar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)
    
    # Foydalanuvchilar jadvali (Balansi 0 dan boshlanadi)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        balance INTEGER DEFAULT 0,
        energy INTEGER DEFAULT 100,
        last_daily TEXT DEFAULT ''
    )
    """)
    
    # Waifular jadvali
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
    
    # Adminlar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        user_id INTEGER PRIMARY KEY
    )
    """)
    
    # O'zingizning ID raqamingizni boshlang'ich admin qilamiz (7986354170)
    cursor.execute("INSERT OR IGNORE INTO admins (user_id) VALUES (?)", (7986354170,))

    defaults = {
        "tap_limit": "100",
        "tap_cooldown": "60",
        "daily_reward": "50", # Admin o'zgartira oladigan kunlik sovg'a qiymati
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

def is_admin(user_id: int) -> bool:
    cursor.execute("SELECT user_id FROM admins WHERE user_id = ?", (user_id,))
    return cursor.fetchone() is not None

def add_admin(user_id: int):
    cursor.execute("INSERT OR IGNORE INTO admins (user_id) VALUES (?)", (user_id,))
    conn.commit()

def get_user(user_id: int, username: str, first_name: str):
    cursor.execute("SELECT balance, energy FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        cursor.execute("INSERT INTO users (user_id, username, first_name, balance, energy) VALUES (?, ?, ?, 0, 100)", 
                       (user_id, username, first_name))
        conn.commit()
        return 0, 100
    return row[0], row[1]
