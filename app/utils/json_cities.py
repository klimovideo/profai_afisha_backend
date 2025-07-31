import json
import os

from fastapi import Depends

from app.dependencies.afisha import get_afisha_client
from app.services.afisha import AfishaClient

path_file = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'cities.json'
)


def save_cities_to_json(afisha_client: AfishaClient = Depends(get_afisha_client)):
    client = afisha_client

    try:
        # Получаем список городов
        cities = client.get_cities()

        # Сохраняем в JSON файл
        with open(path_file, 'w', encoding='utf-8') as f:
            json.dump(cities, f, ensure_ascii=False, indent=2)

        print(f'Список городов успешно сохранен в файл: {path_file}')
        print(f'Всего сохранено городов: {len(cities)}')

    except Exception as e:
        print(f'Произошла ошибка при сохранении городов: {str(e)}')


def read_cities_from_json():
    """Читает список городов из файла data/cities.json"""
    try:
        with open(path_file, 'r', encoding='utf-8') as f:
            cities = json.load(f)
        return cities
    except FileNotFoundError:
        print(f'Файл не найден: {path_file}')
        return None
    except Exception as e:
        print(f'Произошла ошибка при чтении файла: {str(e)}')
        return None


if __name__ == '__main__':
    save_cities_to_json()
