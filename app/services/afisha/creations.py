# services/afisha/creations.py
from app.schemas.creations import CreationScheduleRequest, CreationsRequest

from .base import AfishaBaseClient


class CreationsClient(AfishaBaseClient):
    async def get_list(self, params: CreationsRequest):
        return await self._get(endpoint='/creations/page', extra_params=params)

    async def get_by_id(self, id):
        return await self._get(endpoint=f'/creations/{id}')

    async def get_by_kinoplan_id(self, id):
        return await self._get(endpoint=f'/creations/kinoplan/{id}')

    async def get_schedule(self, id, params: CreationScheduleRequest):
        return await self._get(endpoint=f'/creations/{id}/schedule', extra_params=params)
