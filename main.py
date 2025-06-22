from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import stock

app = FastAPI()

# ルーティング追加（router定義ファイル）
app.include_router(stock.router)

# 静的ファイル・テンプレートの設定
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

from models.database import init_db

init_db()