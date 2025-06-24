import io
import base64
import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from utils.stock_data import get_stock_history
from db.database import save_search
from utils.logger import setup_logger

router = APIRouter()
templates = Jinja2Templates(directory="templates")
logger = setup_logger("routers.stock")

# 日本語フォントの設定（IPAexGothic など）
font_path = "/usr/share/fonts/truetype/ipaexg/ipaexg.ttf"  # 環境によって変更が必要
if os.path.exists(font_path):
    plt.rcParams['font.family'] = fm.FontProperties(fname=font_path).get_name()
else:
    logger.warning(f"日本語フォントが見つかりません: {font_path}")

@router.post("/get_price", response_class=HTMLResponse)
async def get_price(request: Request, code: str = Form(...), period: str = Form("1mo")):
    try:
        logger.info(f"株価データ取得開始: code={code}, period={period}")
        code, hist = get_stock_history(code, period)
        if hist.empty:
            logger.warning(f"株価データが取得できませんでした: {code}")
            return templates.TemplateResponse("index.html", {
                "request": request,
                "history": [],
                "error": f"{code} の株価データが取得できませんでした"
            })

        latest_price = hist["Close"].iloc[-1]
        await save_search(code, float(latest_price))

        plt.figure(figsize=(10, 5))
        plt.plot(hist.index, hist["Close"], marker="o")
        plt.title(f"{code} の株価推移")
        plt.xlabel("日付")
        plt.ylabel("終値")
        plt.grid(True)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        graph = base64.b64encode(buf.getvalue()).decode("utf-8")

        logger.info(f"株価データ取得完了: {code}")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "history": [],
            "graph": graph,
            "code": code
        })
    except Exception as e:
        logger.exception(f"エラー発生: {e}")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "history": [],
            "error": f"データ取得中にエラーが発生しました: {str(e)}"
        })