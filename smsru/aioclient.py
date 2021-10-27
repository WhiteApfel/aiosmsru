from typing import Optional, Union
import sys

from smsru.models import SMSruWithBalance, SMSruBase
from smsru.models.limits import SMSruLimit, SMSruFreeLimit
from smsru.models.senders import SMSruSenders
from smsru.models.stoplist import SMSruStoplist

if sys.version_info >= (3, 9):
    from collections.abc import Sequence
else:
    from typing import Sequence
from httpx import AsyncClient, Response

from smsru.models.sms import (
    SMSruSendSmsResponse,
    SMSruCheckSmsResponse,
    SMSruSmsCostResponse,
)


class AioSMSru:
    def __init__(self, api_id: str, domain: str = "sms.ru"):
        self._api_id = api_id
        self._domain = domain
        self._client: Optional[AsyncClient] = None

    @property
    def client(self) -> AsyncClient:
        if not self._client:
            self._client = AsyncClient()
        return self._client

    async def _request(self, endpoint: str, params: dict = None) -> Response:
        if not params:
            params = {}
        params.update({"api_id": self._api_id, "json": 1, "partner_id": 331687})
        response = await self.client.get(
            f"https://{self._domain}/{endpoint}", params=params
        )
        return response

    async def send_sms(
        self,
        recipients: Union[str, Sequence[str]],
        messages: Union[str, Sequence[str]],
        **kwargs,
    ) -> SMSruSendSmsResponse:
        """
        Method for sending SMS.
        Method can send one or more messages
        with the same or different text.

        For example, you can

        :param recipients: Phone number or their sequence
        :type recipients: ``str`` or sequence of ``str``
        :param messages: Message or their sequence according
        to the sequence of recipients
        :param kwargs: ``str`` or sequence of ``str``
        :return: sms.ru response
        :rtype: SMSruSendSmsResponse
        """
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
                        "Sequences of recipients and messages "
                        "must be of the same length"
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
                    "Messages must be str (message) " "or sequence of str (messages)"
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
                    "If there is only one recipient, "
                    "then there can be no more than one message"
                )
        else:
            raise ValueError(
                "Recipients must be str (phone number) "
                "or sequence of str (phone numbers)"
            )

        params.update(kwargs)

        response = await self._request("sms/send", params)

        return SMSruSendSmsResponse(**response.json())

    async def check_sms(self, ids: Union[str, Sequence[str]]) -> SMSruCheckSmsResponse:
        """
        Check the status of one or more messages

        :param ids: message identifier or sequence
        :return: sms.ru response
        :rtype: SMSruCheckSmsResponse
        """
        if isinstance(ids, str):
            ids = [ids]
        if not isinstance(ids, Sequence):
            raise ValueError("ids must be str or sequence of str")

        params = {"sms_id": ",".join(ids)}

        response = await self._request("sms/status", params)

        return SMSruCheckSmsResponse(**response.json())

    async def sms_cost(
        self,
        recipients: Union[str, Sequence[str]],
        messages: Union[str, Sequence[str]],
        **kwargs,
    ) -> SMSruSmsCostResponse:
        """
        Get the cost of sending a specific message to a specific number

        :param recipients: Phone number or their sequence
        :type recipients: ``str`` or sequence of ``str``
        :param messages: Message or their sequence according
        to the sequence of recipients
        :type messages: ``str`` or sequence of ``str``
        :param kwargs: Other parameters according to the documentation sms.ru
        :return: sms.ru response
        :rtype: SMSruSmsCostResponse
        """
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
                        "Sequences of recipients and messages "
                        "must be of the same length"
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
                    "Messages must be str (message) " "or sequence of str (messages)"
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
                    "If there is only one recipient, "
                    "then there can be no more than one message"
                )
        else:
            raise ValueError(
                "Recipients must be str (phone number) "
                "or sequence of str (phone numbers)"
            )

        params.update(kwargs)

        response = await self._request("sms/cost", params)

        return SMSruSmsCostResponse(**response.json())

    async def balance(self) -> SMSruWithBalance:
        """
        Get account balance

        :return: sms.ru response
        :rtype: SMSruWithBalance
        """
        response = await self._request("my/balance")

        return SMSruWithBalance(**response.json())

    async def limit(self) -> SMSruLimit:
        """
        Get account sms limits

        :return: sms.ru response
        :rtype: SMSruLimit
        """
        response = await self._request("my/limit")

        return SMSruLimit(**response.json())

    async def free_limit(self) -> SMSruFreeLimit:
        """
        Get account free sms limit

        :return: sms.ru response
        :rtype: SMSruFreeLimit
        """
        response = await self._request("my/free")

        return SMSruFreeLimit(**response.json())

    async def senders(self) -> SMSruSenders:
        """
        Get approved senders

        :return: sms.ru response
        :rtype: SMSruSenders
        """
        response = await self._request("my/senders")

        return SMSruSenders(**response.json())

    async def check_auth(
        self, api_id: str = None, login: str = None, password: str = None
    ) -> SMSruBase:
        """
        Check username/password or app_id for validity.
        Be sure to specify api_id or login and password

        :param api_id: api_id
        :type api_id: ``str``
        :param login: login (phone number in 79996662244 format)
        :type login: ``str``
        :param password: password
        :type password: ``str``
        :return: sms.ru response
        :rtype: SMSruBase
        """
        if api_id:
            params = {"api_id": api_id}
        elif login and password:
            params = {"login": login, "password": password}
        else:
            raise ValueError("You must provide api_id or login and password")

        response = await self.client.get(
            f"https://{self._domain}/auth/check", params=params
        )

        return SMSruBase(**response.json())

    async def stoplist(self) -> SMSruStoplist:
        response = await self._request("stoplist/get")

        return SMSruStoplist(**response.json())
