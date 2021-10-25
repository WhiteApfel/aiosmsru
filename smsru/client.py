from typing import Optional, Union
import sys

from smsru.models import SMSruWithBalance
from smsru.models.limits import SMSruLimit, SMSruFreeLimit

if sys.version_info >= (3, 9):
    from collections.abc import Sequence
else:
    from typing import Sequence
from httpx import Client, Response

from smsru.models.sms import (
    SMSruSendSmsResponse,
    SMSruCheckSmsResponse,
    SMSruSmsCostResponse,
)


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

    def _request(self, endpoint: str, params: dict = None) -> Response:
        if not params:
            params = {}
        params.update({"api_id": self._api_id, "json": 1})
        response = self.client.get(f"https://{self._domain}/{endpoint}", params=params)
        return response

    def send_sms(
        self, recipients: Union[str, Sequence[str]], messages: Union[str, Sequence[str]]
    ) -> SMSruSendSmsResponse:
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
                if isinstance(messages, Sequence) and not isinstance(messages, str):
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
                if isinstance(messages, Sequence) and not isinstance(messages, str):
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

    def check_sms(self, ids: Union[str, Sequence[str]]) -> SMSruCheckSmsResponse:
        if isinstance(ids, str):
            ids = [ids]
        if not isinstance(ids, Sequence):
            raise ValueError("ids must be str or sequence of str")

        params = {"sms_id": ",".join(ids)}

        response = self._request("sms/status", params)

        return SMSruCheckSmsResponse(**response.json())

    def sms_cost(
        self, recipients: Union[str, Sequence[str]], messages: Union[str, Sequence[str]]
    ) -> SMSruSmsCostResponse:
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
                if isinstance(messages, Sequence) and not isinstance(messages, str):
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
                if isinstance(messages, Sequence) and not isinstance(messages, str):
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

        response = self._request("sms/cost", params)

        return SMSruSmsCostResponse(**response.json())

    def balance(self):
        response = self._request("my/balance")

        return SMSruWithBalance(**response.json())

    def limit(self):
        response = self._request("my/limit")

        return SMSruLimit(**response.json())

    def free_limit(self):
        response = self._request("my/free")

        return SMSruFreeLimit(**response.json())
