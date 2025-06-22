import yfinance as yf

def get_stock_history(code: str):
    # 国内株式か米国株か判定
    if code.isdigit():
        code += ".T"

    stock = yf.Ticker(code)
    hist = stock.history(period="1mo")
    return code, hist

from models.database import SessionLocal, SearchHistory

def save_search_history(code: str):
    db = SessionLocal()
    record = SearchHistory(code=code)
    db.add(record)
    db.commit()
    db.close()