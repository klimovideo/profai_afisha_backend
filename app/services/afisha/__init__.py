from .cities import CitiesClient
from .creations import CreationsClient


class AfishaClient:
    def __init__(self):
        self.cities = CitiesClient()
        self.creations = CreationsClient()

    async def close(self):
        await self.cities.close()
        await self.creations.close()
