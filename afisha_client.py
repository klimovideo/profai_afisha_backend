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
        """Get list of available cities"""
        url = f"{self.BASE_URL}/cities"
        response = requests.get(url, headers=self.headers, params=self.params)
        response.raise_for_status()
        return response.json()
    
    def get_city(self, city_id):
        """Get city for id"""
        url = f"{self.BASE_URL}/cities/{city_id}"
        response = requests.get(url, headers=self.headers, params=self.params)
        response.raise_for_status()
        return response.json()
    
    def get_productions(self, city_id, page=1, per_page=20):
        """Get productions for a specific city"""
        url = f"{self.BASE_URL}/productions"
        params = {
            **self.params,
            "cityId": city_id,
            "page": page,
            "perPage": per_page
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_production_details(self, production_id):
        """Get detailed information about a specific production"""
        url = f"{self.BASE_URL}/productions/{production_id}"
        response = requests.get(url, headers=self.headers, params=self.params)
        response.raise_for_status()
        return response.json() 