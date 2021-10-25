from typing import Optional

from . import SMSruWithBalance, SMSruBase


class SMSruSendSms(SMSruBase):
    sms_id: str


class SMSruSendSmsResponse(SMSruWithBalance):
    sms: dict[str, SMSruSendSms]
