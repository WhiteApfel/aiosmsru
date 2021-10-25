from typing import Optional
from httpx import AsyncClient


class AioSMSru:
    def __init__(self, api_id: str):
        self._api_id = api_id
        self._client: Optional[AsyncClient] = None

    @property
    def client(self):
        if not self._client:
            self._client = AsyncClient()
        return self._client
