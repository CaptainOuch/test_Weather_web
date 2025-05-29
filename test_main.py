import pytest
from fastapi.testclient import TestClient
from main import app, SessionLocal
from models import SearchHistory, Base
from db import engine
import os

client = TestClient(app)

# Переинициализация базы перед каждым тестом
@pytest.fixture(autouse=True)
def setup_and_teardown():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_main_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Погода в городе" in response.text


def test_search_city_and_history():
    response = client.post("/weather", data={"city": "Москва"})
    assert response.status_code == 200
    assert "Москва" in response.text

    # Проверим, что запись появилась в истории
    db = SessionLocal()
    result = db.query(SearchHistory).filter_by(city="Москва").first()
    db.close()
    assert result is not None


def test_stats_top_5():
    # Сымитируем несколько запросов
    cities = ["Москва", "Берлин", "Москва", "Берлин", "Берлин", "Лондон", "Париж", "Рим", "Рим", "Рим"]
    for city in cities:
        client.post("/weather", data={"city": city})

    res = client.get("/api/stats")
    assert res.status_code == 200
    stats = res.json()

    # Убедимся, что Москва и Берлин в списке
    assert "Москва" in stats
    assert "Берлин" in stats
    assert stats["Берлин"] >= stats["Москва"]
    assert len(stats) <= 5
