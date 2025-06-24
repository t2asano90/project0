from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routers import stock, history
from db.database import init_db

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
    await init_db()

# ルートエンドポイント（/）を追加
from db.database import get_latest_searches

@app.get("/")
async def read_root(request: Request):
    history = await get_latest_searches()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "history": history
    })