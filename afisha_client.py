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
        
    #-------------------- Функции эндпоинтов для городов --------------------
    
    def get_cities(self, date_from, date_to):
        """Запрос возвращает все города с открытыми продажами для вашего партнерского аккаунта. По умолчанию возвращаются для всех продаж, начиная с текущей даты, при указании периода - только за указанный период"""
        url = f"{self.BASE_URL}/cities"
        params = {
            **self.params,
            "DateFrom": date_from,
            "DateTo": date_to,
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_city(self, city_id):
        """Получение города по идентификатору. Не зависит от наличия открытых продаж"""
        url = f"{self.BASE_URL}/cities/{city_id}"
        response = requests.get(url, headers=self.headers, params=self.params)
        response.raise_for_status()
        return response.json()
    
    #-------------------- Функции эндпоинтов для произведений (событий, мероприятий, фильмов и т.д.) --------------------
    
    def get_creations(self, city_id, date_from=None, date_to=None, creation_type=None, limit=None, cursor=None):
        """По умолчанию возвращаются произведения для всех сеансов, начиная с текущей даты, а при указании периода - только за указанный период"""
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
    
    def get_creation(self, id):
        """Получение произведения по Id, не учитывает доступность продаж"""
        url = f"{self.BASE_URL}/creations/{id}"
        response = requests.get(url, headers=self.headers, params=self.params)
        response.raise_for_status()
        return response.json()
    
    def get_creation_kinoplan(self, id):
        """Получение произведения по идентификатору Kinoplan, не учитывает доступность продаж"""
        url = f"{self.BASE_URL}/creations/kinoplan/{id}"
        response = requests.get(url, headers=self.headers, params=self.params)
        response.raise_for_status()
        return response.json()
    
    def get_creation_schedule(self, id, city_id=None, date_from=None, date_to=None, cinema_format_date_from=None, cinema_format_date_to=None):
        """Получение расписания произведения по идентификатору с необязательной фильтрацией по дате сеанса"""
        params = {
            **self.params,
            "CityId": city_id,
            "DateFrom": date_from,
            "DateTo": date_to,
            "CinemaFormatDateFrom": cinema_format_date_from,
            "CinemaFormatDateTo": cinema_format_date_to,
        }
        url = f"{self.BASE_URL}/creations/{id}/schedule"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    #-------------------- Функции эндпоинтов для площадок (мест событий) --------------------
    
    def get_places(self, city_id, date_from=None, date_to=None, creation_type=None):
        """По умолчанию возвращаются площадки для всех сеансов, начиная с текущей даты, а при указании периода - только за указанный период"""
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
    
    def get_place(self, id):
        """Получение площадки по идентификатору, не учитывает доступность продаж"""
        url = f"{self.BASE_URL}/places/{id}"
        response = requests.get(url, headers=self.headers, params=self.params)
        response.raise_for_status()
        return response.json()
    
    def get_place_schedule(self, id, date_from=None, date_to=None, cinema_format_date_from=None, cinema_format_date_to=None):
        """Получение расписания площадки по идентификатору с необязательной фильтрацией по дате сеанса"""
        url = f"{self.BASE_URL}/places/{id}/schedule"
        params = {
            **self.params,
            "DateFrom": date_from,
            "DateTo": date_to,
            "CinemaFormatDateFrom": cinema_format_date_from,
            "CinemaFormatDateTo": cinema_format_date_to,
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    #-------------------- Функции эндпоинтов для промоакций --------------------
    
    def get_promotions(self, availability=None):
        """Получение списка действующих промоакций"""
        url = f"{self.BASE_URL}/promotions"
        params = {
            **self.params,
            "PromotionAvailability": availability
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_promotion_sessions(self, id, city_id):
        """Получение списка сеансов, на которые действует указанная промоакция. Возвращается не более 150000 сеансов"""
        url = f"{self.BASE_URL}/promotions/{id}/sessions"
        params = {
            **self.params,
            "CityId": city_id
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()