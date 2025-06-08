from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import yfinance as yf

app = FastAPI()

# テンプレート設定
templates = Jinja2Templates(directory="templates")

# ホームページ表示
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 株価取得処理
@app.post("/get_price", response_class=HTMLResponse)
async def get_price(request: Request, code: str = Form(...)):
    print(f"銘柄コード: {code}")  # 送信されたコードをコンソールに出力
    stock = yf.Ticker(code)
    stock_info = stock.history(period="1d")
    price = stock_info['Close'].iloc[0]
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "code": code,
        "price": price
    })