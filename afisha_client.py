import os
import requests
from dotenv import load_dotenv

class AfishaClient:
    BASE_URL = "https://api.afisha.ru/v3"
    
    def __init__(self):
        load_dotenv()
        self.partner_key = os.getenv("PARTNER_KEY")
        self.widget_key = os.getenv("WIDGET_KEY")
        if not self.partner_key or not self.widget_key:
            raise ValueError("PARTNER_KEY and WIDGET_KEY must be set in .env file")
        
        self.headers = {
            "X-ApiAuth-PartnerKey": self.partner_key,
        }
        self.params = {
            "WidgetKey": self.widget_key,
        }
    
    def get_cities(self):
        """Получение списка городов"""
        url = f"{self.BASE_URL}/cities"
        response = requests.get(url, headers=self.headers, params=self.params)
        response.raise_for_status()
        return response.json()
    
    def get_city(self, city_id):
        """Получение города по его ID"""
        url = f"{self.BASE_URL}/cities/{city_id}"
        response = requests.get(url, headers=self.headers, params=self.params)
        response.raise_for_status()
        return response.json()
    
    def get_creations(self, city_id, date_from=None, date_to=None, creation_type=None, limit=None, cursor=None):
        """Получение всех произведений с разбивкой по страницам"""
        url = f"{self.BASE_URL}/creations/page"
        params = {
            **self.params,
            "CityId": city_id,
            "DateFrom": date_from,
            "DateTo": date_to,
            "CreationType": creation_type,
            "Limit": limit,
            "Cursor": cursor
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_places(self, city_id, date_from=None, date_to=None, creation_type=None):
        """Получение всех площадок"""
        url = f"{self.BASE_URL}/places"
        params = {
            **self.params,
            "CityId": city_id,
            "DateFrom": date_from,
            "DateTo": date_to,
            "CreationType": creation_type,
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()