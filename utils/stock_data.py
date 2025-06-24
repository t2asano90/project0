import yfinance as yf
import pandas as pd

def get_stock_history(code: str, period: str = "1mo"):
    """
    指定された期間の株価データを取得（国内外両対応）。
    period: "1mo", "3mo", "1y" など yfinance のサポート形式に準拠。
    国内株式は、".T" を末尾に追加する。
    """
    original_code = code
    if code.isdigit():
        code += ".T"  # 国内株式

    try:
        ticker = yf.Ticker(code)
        hist = ticker.history(period=period)
        return original_code, hist
    except Exception as e:
        raise RuntimeError(f"Failed to fetch data for {original_code} ({code}): {e}")