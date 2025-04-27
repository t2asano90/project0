from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
import yfinance as yf
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# スタティックファイル（CSSとか）を使いたいときのために
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/get_price", response_class=HTMLResponse)
def get_price(request: Request, code: str = Form(...)):
    # コードを判定して日本株 or 米国株対応
    if code.isdigit():
        ticker_symbol = f"{code}.T"
    else:
        ticker_symbol = code

    stock = yf.Ticker(ticker_symbol)
    todays_data = stock.history(period='1d')
    
    if todays_data.empty:
        price = "株価データが取得できませんでした。"
    else:
        price = todays_data['Close'][0]

    return templates.TemplateResponse("result.html", {"request": request, "code": code, "price": price})