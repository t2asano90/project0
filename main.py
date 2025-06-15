from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import yfinance as yf

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_form():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>株価検索フォーム</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>銘柄コードを入力してください</h1>
        <form action="/get_price" method="post">
            <input type="text" name="code" placeholder="例: 7203 または AAPL" required>
            <br>
            <button type="submit">検索</button>
        </form>
    </body>
    </html>
    """

@app.post("/get_price", response_class=HTMLResponse)
async def get_price(code: str = Form(...)):
    try:
        ticker = yf.Ticker(code)
        price = ticker.info.get("regularMarketPrice", "価格情報が見つかりません")
    except Exception as e:
        price = f"エラーが発生しました: {e}"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>株価結果</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>{code} の株価</h1>
        <p>現在の価格: {price}</p>
        <a href="/">戻る</a>
    </body>
    </html>
    """