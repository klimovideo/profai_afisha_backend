from httpx import AsyncClient, Response
from app.core.config import settings

class AfishaBaseClient:
    BASE_URL = 'https://api.afisha.ru/v3'

    def __init__(self):
        self._headers = {'X-ApiAuth-PartnerKey': settings.afisha_api_key}
        self._params = {'WidgetKey': settings.afisha_widget_key}
        self.client = AsyncClient(base_url=self.BASE_URL)

    def _build_params(self, extra: dict = None) -> dict:
        params = {**self._params, **(extra or {})}
        return {k: v for k, v in params.items() if v is not None}

    async def _get(self, endpoint: str, extra_params: dict = None) -> dict:
        response: Response = await self.client.get(
            endpoint,
            headers=self._headers,
            params=self._build_params(extra_params),
        )
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()
