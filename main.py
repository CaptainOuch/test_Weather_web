import re
from urllib.parse import quote, unquote

import requests
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import func

from db import SessionLocal, init_db
from models import SearchHistory

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Инициализируем базу при запуске
init_db()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    last_city = unquote(request.cookies.get("last_city", ""))
    return templates.TemplateResponse("index.html", {"request": request, "last_city": last_city})

@app.post("/weather", response_class=HTMLResponse)
async def get_weather(request: Request, city: str = Form(...)):
    # Сохраняем в БД через SQLAlchemy
    db = SessionLocal()
    search = SearchHistory(city=city)
    db.add(search)
    db.commit()
    db.close()

    # Определяем язык
    lang = "ru" if re.search(r"[а-яА-Я]", city) else "en"

    # Получаем координаты города
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city,
        "count": 1,
        "language": lang,
        "format": "json"
    }
    geo = requests.get(geo_url, params=params).json()
    if not geo.get("results"):
        return templates.TemplateResponse("index.html", {"request": request, "error": "Город не найден."})

    lat = geo['results'][0]['latitude']
    lon = geo['results'][0]['longitude']

    # Получаем прогноз погоды
    weather = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    ).json()

    forecast = weather.get("current_weather", {})

    response = templates.TemplateResponse("index.html", {
        "request": request,
        "city": city,
        "forecast": forecast
    })
    response.set_cookie(key="last_city", value=quote(city))
    return response

@app.get("/api/stats")
def get_stats():
    db = SessionLocal()
    try:
        stats = (
            db.query(SearchHistory.city, func.count().label("count"))
            .group_by(SearchHistory.city)
            .order_by(func.count().desc())
            .limit(5)
            .all()
        )
        return {city: count for city, count in stats}
    finally:
        db.close()
