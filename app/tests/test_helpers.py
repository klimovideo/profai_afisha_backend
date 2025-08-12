import json
from app.utils.helpers import transform_params

with open('app/tests/data/cities.json', encoding='utf-8') as f:
    cities_data = json.load(f)


def test_transform_params_city_name():  # Тест на поиск ID города по имени
    params = {'city_name': 'Москва'}
    expected = {'CityId': 2}  # ID города Москва
    result = transform_params(params, cities_data)
    assert result == expected


def test_transform_params_city_id():  # Тест на использование ID города напрямую
    params = {'city_id': 456}
    expected = {'CityId': 456}  # ID города
    result = transform_params(params, cities_data)
    assert result == expected


def test_transform_params_city_not_found():  # Тест на случай, когда город не найден
    params = {'city_name': 'Неизвестный город'}
    expected = {'CityId': None}
    result = transform_params(params, cities_data)
    assert result == expected


def test_transform_params_city_and_id():  # Тест на случай, когда переданы и имя города, и ID
    params = {'city_name': 'Санкт-Петербург', 'city_id': 99999}
    expected = {'CityId': 3}  # ID города Санкт-Петербург
    result = transform_params(params, cities_data)
    assert result == expected


def test_transform_params_dates():  # Тест на преобразование дат c разными значениями
    params = {'date_from': '2025-08-01', 'date_to': '2025-08-12'}
    expected = {'DateFrom': '2025-08-01T00:00:00', 'DateTo': '2025-08-12T00:00:00'}
    result = transform_params(params)
    assert result == expected


def test_transform_params_dates_equal():  # Тест на преобразование дат с одинаковыми значениями
    params = {'date_from': '2025-08-01', 'date_to': '2025-08-01'}
    expected = {'DateFrom': '2025-08-01T00:00:00', 'DateTo': '2025-08-02T00:00:00'}
    result = transform_params(params)
    assert result == expected


def test_transform_params_dates_none():  # Тест на преобразование дат с None значениями
    params = {'date_from': None, 'date_to': '2025-08-12'}
    expected = {'DateTo': '2025-08-12T00:00:00'}
    result = transform_params(params)
    assert result == expected


def test_transform_params_passthrough():  # Тест на пропуск параметров, которые не требуют преобразования
    params = {'creation_type': 'movie', 'limit': 10, 'cursor': 'abc'}
    expected = {'CreationType': 'movie', 'Limit': 10, 'Cursor': 'abc'}
    result = transform_params(params)
    assert result == expected


def test_transform_params_city_and_dates():  # Тест на преобразование параметров с городом и датами
    params = {
        'city_name': 'Санкт-Петербург',
        'date_from': '2025-08-01',
        'date_to': '2025-08-15',
    }
    expected = {
        'CityId': 3,  # ID города Санкт-Петербург
        'DateFrom': '2025-08-01T00:00:00',
        'DateTo': '2025-08-15T00:00:00',
    }
    result = transform_params(params, cities_data)
    assert result == expected
