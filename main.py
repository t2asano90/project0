# main.py
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import yfinance as yf
import matplotlib.pyplot as plt
import io
import base64

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def form():
    return """
    <html>
        <head><title>株価検索フォーム</title></head>
        <body>
            <h1>銘柄コードを入力してください</h1>
            <form action="/get_price" method="post">
                <input type="text" name="code" placeholder="例: AAPL" required>
                <button type="submit">検索</button>
            </form>
        </body>
    </html>
    """

@app.post("/get_price", response_class=HTMLResponse)
async def get_price(code: str = Form(...)):
    ticker = yf.Ticker(code)
    hist = ticker.history(period="1mo")

    if hist.empty:
        return f"<h2>{code} のデータが見つかりませんでした。</h2>"

    # グラフ作成
    plt.figure(figsize=(10, 4))
    plt.plot(hist.index, hist["Close"], label="Close")
    plt.title(f"{code} の過去1ヶ月の終値")
    plt.xlabel("日付")
    plt.ylabel("株価")
    plt.grid(True)
    plt.legend()

    # 画像をbase64にエンコード
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    return f"""
    <html>
        <head><title>結果</title></head>
        <body>
            <h2>{code} の株価チャート</h2>
            <img src="data:image/png;base64,{image_base64}" />
            <br><a href="/">戻る</a>
        </body>
    </html>
    """