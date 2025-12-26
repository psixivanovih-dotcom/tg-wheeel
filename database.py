import aiosqlite

DB_PATH = "bot.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            tokens INTEGER
        );""")
        await db.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            result TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""")
        await db.commit()

async def get_user(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT id, name, tokens FROM users WHERE id = ?", (user_id,))
        return await cursor.fetchone()

async def add_user(user_id, name):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO users (id, name, tokens) VALUES (?, ?, ?)", (user_id, name, 4))
        await db.commit()

async def update_tokens(user_id, new_tokens):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET tokens = ? WHERE id = ?", (new_tokens, user_id))
        await db.commit()

async def save_stat(user_id, name, result):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO stats (user_id, name, result) VALUES (?, ?, ?)", (user_id, name, result))
        await db.commit()

async def get_stats():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT name, result FROM stats")
        return await cursor.fetchall()
