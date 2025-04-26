from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/stock/{symbol}")
def get_stock_price(symbol: str):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")

    if data.empty:
        return {"error": "Symbol not found or no data available"}

    latest_price = data["Close"].iloc[-1]
    return {
        "symbol": symbol.upper(),
        "latest_price": latest_price
    }