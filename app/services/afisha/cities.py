# services/afisha/cities.py
from .base import AfishaBaseClient

class CitiesClient(AfishaBaseClient):
    async def get_list(self, date_from=None, date_to=None):
        return await self._get('/cities', {
            'DateFrom': date_from,
            'DateTo': date_to,
        })

    async def get_by_id(self, city_id: int):
        return await self._get(f'/cities/{city_id}')
