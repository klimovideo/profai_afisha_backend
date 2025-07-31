# app/services/afisha/__init__.py

from .cities import CitiesClient
from .creations import CreationsClient
from .places import PlacesClient
from .promotions import PromotionsClient


class AfishaClient:
    def __init__(self):
        self.cities = CitiesClient()
        self.creations = CreationsClient()
        self.places = PlacesClient()
        self.promotions = PromotionsClient()

    async def close(self):
        await self.cities.close()
        await self.creations.close()
        await self.places.close()
        await self.promotions.close()
