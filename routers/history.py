# routers/history.py
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from services.stock_service import get_search_history

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/history", response_class=HTMLResponse)
async def view_history(request: Request):
    history = get_search_history()
    return templates.TemplateResponse("history.html", {
        "request": request,
        "history": history
    })