from collections import Sequence
from typing import Optional, Union
from httpx import Client, Response

from smsru.models.sms import SMSruSendSmsResponse


class SMSru:
    def __init__(self, api_id: str, domain: str = "sms.ru"):
        self._api_id = api_id
        self._domain = domain
        self._client: Optional[Client] = None

    @property
    def client(self) -> Client:
        if not self._client:
            self._client = Client()
        return self._client

    def _request(self, endpoint: str, params) -> Response:
        params.update({"api_id": self._api_id, "json": 1})
        response = self.client.get(f"https://{self._domain}/{endpoint}", params=params)
        return response

    def send_sms(
        self, recipients: Union[str, Sequence[str]], messages: Union[str, Sequence[str]]
    ):
        params = {}
        if (  # More than one recipient
            isinstance(recipients, Sequence)
            and not isinstance(recipients, str)
            and len(recipients) > 1
        ):
            if (  # More than one message
                isinstance(messages, Sequence)
                and not isinstance(messages, str)
                and len(messages) > 1
            ):
                if len(recipients) == len(messages):
                    for i, recipient in enumerate(recipients):
                        params[f"to[{recipient}]"] = messages[i]
                else:
                    raise ValueError(
                        "Sequences of recipients and messages must be of the same length"
                    )
            elif (  # One message for all recipients
                isinstance(messages, str)
                or isinstance(messages, Sequence)
                and len(messages) == 1
            ):
                if isinstance(messages, Sequence):
                    messages = messages[0]
                params["to"] = ",".join(recipients)
                params["msg"] = messages
            else:
                raise ValueError(
                    "Messages must be str (message) or sequence of str (messages)"
                )
        elif (  # Only one recipient
            isinstance(recipients, str)
            or isinstance(recipients, Sequence)
            and len(recipients) == 1
        ):
            if (
                isinstance(messages, str)
                or isinstance(messages, Sequence)
                and len(messages) == 1
            ):
                if isinstance(messages, Sequence):
                    messages = messages[0]
                params["to"] = recipients
                params["msg"] = messages
            else:
                raise ValueError(
                    "If there is only one recipient, then there can be no more than one message"
                )
        else:
            raise ValueError(
                "Recipients must be str (phone number) or sequence of str (phone numbers)"
            )

        response = self._request("sms/send", params)

        return SMSruSendSmsResponse(**response.json())
