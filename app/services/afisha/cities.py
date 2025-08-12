# services/afisha/cities.py
from app.schemas.cities import CitiesRequest

from .base import AfishaBaseClient


class CitiesClient(AfishaBaseClient):
    async def get_list(self, params: CitiesRequest):
        return await self._get(endpoint='/cities', extra_params=params)

    async def get_by_id(self, city_id: int):
        return await self._get(endpoint=f'/cities/{city_id}')
