from typing import Optional
from httpx import Client


class SMSru:
    def __init__(self, api_id: str):
        self._api_id = api_id
        self._client: Optional[Client] = None

    @property
    def client(self):
        if not self._client:
            self._client = Client()
        return self._client
