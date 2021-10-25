from typing import Optional
from httpx import Client


class SMSru:
    def __init__(self):
        self._client: Optional[Client] = None

    @property
    def client(self):
        if not self._client:
            self._client = Client()
        return self._client
