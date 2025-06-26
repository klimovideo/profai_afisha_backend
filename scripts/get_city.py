import os
import sys

from json_cities import read_cities_from_json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from afisha_client import AfishaClient

def get_city_id(city_name, from_api:bool=None):
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
        afisha_client = AfishaClient()    
        cities = afisha_client.get_cities()
        
        if cities:
            for city in cities:
                if city['Name'] == city_name:
                    print(f"ID города '{city_name}': {city['Id']}")
                    return city['Id']
            print(f"Город '{city_name}' не найден.")
        return None

if __name__ == "__main__":
    get_city_id('Москва', True)