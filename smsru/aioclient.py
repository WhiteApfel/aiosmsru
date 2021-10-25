from typing import Optional
from httpx import AsyncClient


class AioSMSru:
    def __init__(self, api_id: str, domain: str = "sms.ru"):
        self._api_id = api_id
        self._domain = domain
        self._client: Optional[AsyncClient] = None

    @property
    def client(self):
        if not self._client:
            self._client = AsyncClient()
        return self._client

    async def _request(self, endpoint: str, **params):
        params.update({"api_id": self._api_id, "json": 1})
        response = await self.client.get(f"https://{self._domain}/{endpoint}", params=params)
        return response
