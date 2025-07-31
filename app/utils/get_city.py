from fastapi import Depends

from app.dependencies.afisha import get_afisha_client
from app.services.afisha import AfishaClient

from .json_cities import read_cities_from_json


def get_city_id(
    city_name,
    from_api: bool = None,
    afisha_client: AfishaClient = Depends(get_afisha_client),
):
    if from_api is False or from_api is None:
        cities = read_cities_from_json()

        if cities:
            for city in cities:
                if city['Name'] == city_name:
                    print(f"ID города '{city_name}': {city['Id']}")
                    return city['Id']
            print(f"Город '{city_name}' не найден.")
        return None
    else:
        cities = afisha_client.get_cities()

        if cities:
            for city in cities:
                if city['Name'] == city_name:
                    print(f"ID города '{city_name}': {city['Id']}")
                    return city['Id']
            print(f"Город '{city_name}' не найден.")
        return None


if __name__ == '__main__':
    get_city_id('Москва', True)
