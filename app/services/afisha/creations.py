# services/afisha/creations.py
from .base import AfishaBaseClient

class CreationsClient(AfishaBaseClient):
    async def get_list(self, city_id, date_from=None, date_to=None, creation_type=None, limit=None, cursor=None):
        return await self._get('/creations/page', {
            'CityId': city_id,
            'DateFrom': date_from,
            'DateTo': date_to,
            'CreationType': creation_type,
            'Limit': limit,
            'Cursor': cursor,
        })

    async def get_by_id(self, id):
        return await self._get(f'/creations/{id}')

    async def get_by_kinoplan_id(self, id):
        return await self._get(f'/creations/kinoplan/{id}')

    async def get_schedule(self, id, city_id=None, date_from=None, date_to=None, cinema_format_date_from=None, cinema_format_date_to=None):
        return await self._get(f'/creations/{id}/schedule', {
            'CityId': city_id,
            'DateFrom': date_from,
            'DateTo': date_to,
            'CinemaFormatDateFrom': cinema_format_date_from,
            'CinemaFormatDateTo': cinema_format_date_to,
        })
