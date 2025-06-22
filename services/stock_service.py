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

    # services/stock_service.py
from models.database import SessionLocal, SearchHistory

# 既存関数：save_search_history(code)

def get_search_history():
    db = SessionLocal()
    records = db.query(SearchHistory).order_by(SearchHistory.timestamp.desc()).all()
    db.close()
    return records