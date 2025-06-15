from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import yfinance as yf
import matplotlib.pyplot as plt
import os

app = FastAPI()

# テンプレートと静的ファイルの設定
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get_price", response_class=HTMLResponse)
async def get_price(request: Request, code: str = Form(...)):
    stock = yf.Ticker(code)
    hist = stock.history(period="1mo")

    # グラフ生成
    plt.figure(figsize=(10, 5))
    hist["Close"].plot(title=f"{code} 株価")
    image_path = f"static/{code}.png"
    plt.savefig(image_path)
    plt.close()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "image_url": f"/static/{code}.png"
    })