from .base import AfishaBaseClient


class PromotionsClient(AfishaBaseClient):
    async def get_list(self, availability=None):
        """
        Получение списка действующих промоакций.
        """
        return await self._get('/promotions', {
            'PromotionAvailability': availability
        })

    async def get_sessions(self, promotion_id, city_id):
        """
        Получение списка сеансов по промоакции.
        Возвращает не более 150000 сеансов.
        """
        return await self._get(f'/promotions/{promotion_id}/sessions', {
            'CityId': city_id
        })
