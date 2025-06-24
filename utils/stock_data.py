import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_stock_history(code: str):
    """
    株価データを取得（国内外両対応）。
    国内株式の場合、".T"を末尾に追加する。
    """
    original_code = code
    if code.isdigit():
        code += ".T"  # 国内株式
    try:
        ticker = yf.Ticker(code)
        end = datetime.today()
        start = end - timedelta(days=30)
        hist = ticker.history(start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'))
        return original_code, hist
    except Exception as e:
        print(f"Error fetching data for {code}: {e}")
        return original_code, pd.DataFrame()