from .base import AfishaBaseClient


class PlacesClient(AfishaBaseClient):
    async def get_list(self, city_id, date_from=None, date_to=None, creation_type=None):
        """
        Получение списка площадок в городе.
        По умолчанию — для всех сеансов с текущей даты.
        """
        return await self._get('/places', {
            'CityId': city_id,
            'DateFrom': date_from,
            'DateTo': date_to,
            'CreationType': creation_type,
        })

    async def get_by_id(self, place_id):
        """Получение площадки по ID, без учёта доступности продаж"""
        return await self._get(f'/places/{place_id}')

    async def get_schedule_by_id(self, place_id, date_from=None, date_to=None, cinema_format_date_from=None, cinema_format_date_to=None):
        """Получение расписания площадки по ID с необязательной фильтрацией по дате"""
        return await self._get(f'/places/{place_id}/schedule', {
            'DateFrom': date_from,
            'DateTo': date_to,
            'CinemaFormatDateFrom': cinema_format_date_from,
            'CinemaFormatDateTo': cinema_format_date_to,
        })
