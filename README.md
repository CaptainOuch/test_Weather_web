# 🌦️ Weather Forecast App (FastAPI)

Веб-приложение на FastAPI для получения прогноза погоды по названию города, с сохранением истории запросов и визуализацией статистики.

---

## 🚀 Возможности

- Поиск текущей погоды по названию города (русский и английский язык)
- Поддержка автосохранения последнего города в cookie
- Сохранение истории запросов в SQLite
- API `/api/stats` для получения статистики по городам
- Отображение топ-5 городов в виде графика (Chart.js)
- Упаковано в Docker

---

## 🧰 Используемые технологии

- FastAPI
- Jinja2 Templates
- SQLite + SQLAlchemy
- Chart.js
- Docker + Docker Compose

---

## 📦 Как запустить

```bash
git clone https://github.com/yourusername/weather-fastapi.git
cd weather-fastapi
docker-compose up --build

После запуска приложение будет доступно на http://localhost:8000