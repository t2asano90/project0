from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import matplotlib.pyplot as plt
import io
import base64

from utils.stock_data import get_stock_history
from db.database import save_search, get_latest_searches

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/get_price", response_class=HTMLResponse)
async def get_price(request: Request, code: str = Form(...), period: str = Form("1mo")):
    code, hist = get_stock_history(code, period=period)

    img_data = None
    if hist is not None and not hist.empty:
        plt.figure(figsize=(10, 5))
        plt.plot(hist.index, hist['Close'], label="終値", color='blue')
        plt.title(f"{code} の過去の株価推移 ({period})")
        plt.xlabel("日付")
        plt.ylabel("株価")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img_data = base64.b64encode(buf.read()).decode("utf-8")
        buf.close()
        plt.close()

        latest_price = hist["Close"].iloc[-1]
        save_search(code, latest_price)
    else:
        latest_price = "データなし"

    latest_searches = await get_latest_searches()

    return templates.TemplateResponse("result.html", {
        "request": request,
        "code": code,
        "price": latest_price,
        "graph": img_data,
        "searches": latest_searches
    })