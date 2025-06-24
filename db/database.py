import aiosqlite
from datetime import datetime

DB_PATH = "search_history.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL,
                price REAL NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        await db.commit()

def save_search(code: str, price: float):
    import asyncio
    asyncio.create_task(_save_search(code, price))

async def _save_search(code: str, price: float):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO search_history (code, price, timestamp) VALUES (?, ?, ?)",
            (code, price, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        await db.commit()

def get_latest_searches(limit: int = 10):
    import asyncio
    return asyncio.run(_get_latest_searches(limit))

async def _get_latest_searches(limit: int = 10):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT code, price, timestamp FROM search_history ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = await cursor.fetchall()
        await cursor.close()
        return [
            {"code": row[0], "price": row[1], "timestamp": row[2]}
            for row in rows
        ]