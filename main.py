import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv  # ← .env を読み込む

from routers import stock, history
from db.database import init_db, get_latest_searches
from utils.logger import setup_logger  # ← ロガーのインポート

# .env 読み込み
load_dotenv()

# 環境変数からログレベル取得（なければ info）
log_level = os.getenv("LOG_LEVEL", "info")

# ログ設定の初期化
logger = setup_logger("main", log_level=log_level)
logger.info("アプリケーションを起動します")

app = FastAPI()

# ルーティング追加
app.include_router(stock.router)
app.include_router(history.router)

# 静的ファイルとテンプレートの設定
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# アプリ起動時にDB初期化
@app.on_event("startup")
async def startup_event():
    logger.info("DB初期化開始")
    await init_db()
    logger.info("DB初期化完了")

# ルートエンドポイント（/）を追加
@app.get("/")
async def read_root(request: Request):
    logger.info("トップページにアクセスがありました")
    history = await get_latest_searches()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "history": history
    })