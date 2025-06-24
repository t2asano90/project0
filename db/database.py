import aiosqlite
import logging
from datetime import datetime

# ログ設定
logger = logging.getLogger(__name__)
DB_PATH = "search_history.db"

# DB初期化
async def init_db():
    try:
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
            logger.info("Database initialized successfully.")
    except Exception as e:
        logger.exception(f"Failed to initialize database: {e}")

# 非同期で保存
async def save_search(code: str, price: float):
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT INTO search_history (code, price, timestamp) VALUES (?, ?, ?)",
                (code, price, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            await db.commit()
            logger.info(f"Saved search: code={code}, price={price}")
    except Exception as e:
        logger.exception(f"Failed to save search for code={code}: {e}")

# 最新の履歴を取得
async def get_latest_searches(limit: int = 10):
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute(
                "SELECT code, price, timestamp FROM search_history ORDER BY id DESC LIMIT ?",
                (limit,)
            )
            rows = await cursor.fetchall()
            await cursor.close()
            logger.info("Fetched latest search history.")
            return [
                {"code": row[0], "price": row[1], "timestamp": row[2]}
                for row in rows
            ]
    except Exception as e:
        logger.exception(f"Failed to fetch search history: {e}")
        return []