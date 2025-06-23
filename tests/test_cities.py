from fastapi.testclient import TestClient
from app import app

print(TestClient.__module__)

client = TestClient(app)

def test_get_cities():
    response = client.get("/cities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Проверяем, что хотя бы один город содержит нужные ключи
    if data:
        assert "Id" in data[0]
        assert "Name" in data[0]

def test_get_city():
    # Получаем список городов, чтобы взять существующий id
    cities_resp = client.get("/cities")
    assert cities_resp.status_code == 200
    cities = cities_resp.json()
    if not cities:
        return  # Нет городов — пропускаем тест
    city_id = cities[0]["Id"]
    resp = client.get(f"/city/{city_id}")
    assert resp.status_code == 200
    city = resp.json()
    assert city["Id"] == city_id
    assert "Name" in city