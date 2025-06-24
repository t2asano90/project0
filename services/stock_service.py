import yfinance as yf
from utils.logger import setup_logger
from models.database import SessionLocal, SearchHistory

logger = setup_logger(__name__)

def get_stock_history(code: str, period: str = "1mo"):
    """株価履歴の取得（yfinance使用）。国内株式なら .T を追加"""
    original_code = code
    if code.isdigit():
        code += ".T"

    try:
        stock = yf.Ticker(code)
        hist = stock.history(period=period)

        if hist.empty:
            logger.warning(f"株価データが見つかりません: {code}")
            return original_code, None

        logger.info(f"株価データ取得成功: {code}")
        return original_code, hist

    except Exception as e:
        logger.error(f"株価データ取得失敗: {code} | エラー: {e}")
        return original_code, None

def save_search_history(code: str):
    """検索履歴をDBに保存"""
    db = SessionLocal()
    try:
        record = SearchHistory(code=code)
        db.add(record)
        db.commit()
        logger.info(f"検索履歴を保存しました: {code}")
    except Exception as e:
        logger.error(f"検索履歴の保存に失敗: {code} | エラー: {e}")
    finally:
        db.close()

def get_search_history():
    """全ての検索履歴を取得"""
    db = SessionLocal()
    try:
        records = db.query(SearchHistory).order_by(SearchHistory.timestamp.desc()).all()
        return records
    except Exception as e:
        logger.error(f"検索履歴の取得に失敗: {e}")
        return []
    finally:
        db.close()

def get_latest_history(limit: int = 10):
    """最新n件の履歴を取得"""
    db = SessionLocal()
    try:
        records = db.query(SearchHistory).order_by(SearchHistory.timestamp.desc()).limit(limit).all()
        return records
    except Exception as e:
        logger.error(f"最新履歴の取得に失敗: {e}")
        return []
    finally:
        db.close()