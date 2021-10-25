from typing import Optional
from httpx import AsyncClient


class AioSMSru:
    def __init__(self):
        self._client: Optional[AsyncClient] = None

    @property
    def client(self):
        if not self._client:
            self._client = AsyncClient()
        return self._client
