from httpx import AsyncClient

from app.core.config import settings


class AfishaClient:
    BASE_URL = 'https://api.afisha.ru/v3'

    def __init__(self):
        self.headers = {
            'X-ApiAuth-PartnerKey': settings.afisha_api_key,
        }
        self.params = {
            'WidgetKey': settings.afisha_widget_key,
        }

        self.client = AsyncClient(
            base_url=self.BASE_URL,
            headers=self.headers,
            params=self.params,
        )

    async def close(self):
        """Закрытие клиента для освобождения ресурсов"""
        await self.client.aclose()

    # -------------------- Функции эндпоинтов для городов --------------------

    async def get_cities(self, date_from=None, date_to=None):
        """Запрос возвращает все города с открытыми продажами для вашего партнерского аккаунта. По умолчанию возвращаются для всех продаж, начиная с текущей даты, при указании периода - только за указанный период"""
        params = {
            **self.params,
            'DateFrom': date_from,
            'DateTo': date_to,
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.client.get('/cities', params=params)
        response.raise_for_status()
        return response.json()

    async def get_city(self, city_id: int):
        """Получение города по идентификатору. Не зависит от наличия открытых продаж"""
        url = f'/cities/{city_id}'

        response = await self.client.get(url, params=self.params)
        response.raise_for_status()
        return response.json()

    # -------------------- Функции эндпоинтов для произведений (событий, мероприятий, фильмов и т.д.) --------------------

    async def get_creations(
        self, city_id, date_from=None, date_to=None, creation_type=None, limit=None, cursor=None
    ):
        """По умолчанию возвращаются произведения для всех сеансов, начиная с текущей даты, а при указании периода - только за указанный период"""
        params = {
            **self.params,
            'CityId': city_id,
            'DateFrom': date_from,
            'DateTo': date_to,
            'CreationType': creation_type,
            'Limit': limit,
            'Cursor': cursor,
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.client.get('/creations/page', headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    async def get_creation(self, id):
        """Получение произведения по Id, не учитывает доступность продаж"""
        url = f'/creations/{id}'

        response = await self.client.get(url, headers=self.headers, params=self.params)
        response.raise_for_status()
        return response.json()

    async def get_creation_kinoplan(self, id):
        """Получение произведения по идентификатору Kinoplan, не учитывает доступность продаж"""
        url = f'/creations/kinoplan/{id}'

        response = await self.client.get(url, headers=self.headers, params=self.params)
        response.raise_for_status()
        return response.json()

    async def get_creation_schedule(
        self,
        id,
        city_id=None,
        date_from=None,
        date_to=None,
        cinema_format_date_from=None,
        cinema_format_date_to=None,
    ):
        """Получение расписания произведения по идентификатору с необязательной фильтрацией по дате сеанса"""
        url = f'/creations/{id}/schedule'

        params = {
            **self.params,
            'CityId': city_id,
            'DateFrom': date_from,
            'DateTo': date_to,
            'CinemaFormatDateFrom': cinema_format_date_from,
            'CinemaFormatDateTo': cinema_format_date_to,
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.client.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    # -------------------- Функции эндпоинтов для площадок (мест событий) --------------------

    async def get_places(self, city_id, date_from=None, date_to=None, creation_type=None):
        """По умолчанию возвращаются площадки для всех сеансов, начиная с текущей даты, а при указании периода - только за указанный период"""
        params = {
            **self.params,
            'CityId': city_id,
            'DateFrom': date_from,
            'DateTo': date_to,
            'CreationType': creation_type,
        }

        response = await self.client.get('/places', headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    async def get_place(self, id):
        """Получение площадки по идентификатору, не учитывает доступность продаж"""
        url = f'/places/{id}'

        response = await self.client.get(url, headers=self.headers, params=self.params)
        response.raise_for_status()
        return response.json()

    async def get_place_schedule(
        self,
        id,
        date_from=None,
        date_to=None,
        cinema_format_date_from=None,
        cinema_format_date_to=None,
    ):
        """Получение расписания площадки по идентификатору с необязательной фильтрацией по дате сеанса"""
        url = f'/places/{id}/schedule'

        params = {
            **self.params,
            'DateFrom': date_from,
            'DateTo': date_to,
            'CinemaFormatDateFrom': cinema_format_date_from,
            'CinemaFormatDateTo': cinema_format_date_to,
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.client.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    # -------------------- Функции эндпоинтов для промоакций --------------------

    async def get_promotions(self, availability=None):
        """Получение списка действующих промоакций"""
        params = {**self.params, 'PromotionAvailability': availability}
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.client.get('/promotions', headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    async def get_promotion_sessions(self, id, city_id):
        """Получение списка сеансов, на которые действует указанная промоакция. Возвращается не более 150000 сеансов"""
        url = f'/promotions/{id}/sessions'

        params = {**self.params, 'CityId': city_id}

        response = await self.client.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
