# utils/stock_data.py
import yfinance as yf

def get_stock_history(code: str):
    if code.isnumeric():
        code += ".T"  # 国内株式の処理
    ticker = yf.Ticker(code)
    hist = ticker.history(period="1mo")
    return code, hist