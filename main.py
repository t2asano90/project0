from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import yfinance as yf

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_form():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>株価検索フォーム</title>
    </head>
    <body>
        <h1>銘柄コードを入力してください</h1>
        <form action="/get_price" method="post">
            <input type="text" name="code" placeholder="例: 7203 または AAPL" required>
            <button type="submit">検索</button>
        </form>
    </body>
    </html>
    """

@app.post("/get_price", response_class=HTMLResponse)
async def get_price(code: str = Form(...)):
    try:
        stock = yf.Ticker(code)
        price = stock.history(period="1d")["Close"][0]
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>株価表示</title>
        </head>
        <body>
            <h1>{code} の株価: {price:.2f} 円</h1>
            <a href="/">戻る</a>
        </body>
        </html>
        """
    except Exception as e:
        return f"""
        <html>
        <body>
            <h1>エラー: {str(e)}</h1>
            <a href="/">戻る</a>
        </body>
        </html>
        """