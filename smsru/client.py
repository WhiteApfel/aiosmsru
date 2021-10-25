from typing import Optional
from httpx import Client


class SMSru:
    def __init__(self, api_id: str, domain: str = "sms.ru"):
        self._api_id = api_id
        self._domain = domain
        self._client: Optional[Client] = None

    @property
    def client(self):
        if not self._client:
            self._client = Client()
        return self._client

    def _request(self, endpoint: str, **params):
        params.update({"api_id": self._api_id, "json": 1})
        response = self.client.get(f"https://{self._domain}/{endpoint}", params=params)
        return response
