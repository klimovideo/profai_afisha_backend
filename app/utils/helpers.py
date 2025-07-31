from fastapi import Depends
from typing import Optional

from app.dependencies.afisha import get_afisha_client
from app.services.afisha import AfishaClient

from .json_cities import read_cities_from_json


# def _get_id_from_json(city_name: str):
#     """Получение ID города из локального JSON-файла."""
#     cities = read_cities_from_json()
#     if cities:
#         for city in cities:
#             if city['Name'] == city_name:
#                 print(f"ID города '{city_name}' (из JSON): {city['Id']}")
#                 return city['Id']
#         print(f"Город '{city_name}' не найден в JSON.")
#     return None


async def _get_id_from_afisha(city_name: str):
    """Получение ID города из API Афиши."""
    afisha_client: AfishaClient = Depends(get_afisha_client)
    cities_response = await afisha_client.cities.get_list()
    cities = (
        cities_response.get('Cities', []) if isinstance(cities_response, dict) else cities_response
    )

    for city in cities:
        if city['Name'] == city_name:
            return city['Id']
    return None


async def get_city_id(city_name: str, from_api: Optional[bool] = None):
    if from_api:
        return await _get_id_from_afisha(city_name)
    # return _get_id_from_json(city_name)

