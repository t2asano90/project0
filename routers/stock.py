from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.stock_service import get_latest_history
from utils.stock_data import get_stock_history
import matplotlib.pyplot as plt

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    history = get_latest_history()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "history": history
    })

@router.post("/get_price", response_class=HTMLResponse)
async def get_price(request: Request, code: str = Form(...)):
    code, hist = get_stock_history(code)

    if hist is None or hist.empty:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"「{code}」の株価データが見つかりませんでした。"
        })

    # グラフ描画
    image_path = f"static/{code}.png"
    plt.figure(figsize=(10, 5))
    hist["Close"].plot(title=f"{code} 株価")
    plt.savefig(image_path)
    plt.close()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "image_url": f"/static/{code}.png"
    })