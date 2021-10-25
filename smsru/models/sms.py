from typing import Optional, Dict

from . import SMSruWithBalance, SMSruBase


class SMSruSendSms(SMSruBase):
    sms_id: Optional[str]


class SMSruSendSmsResponse(SMSruWithBalance):
    sms: Dict[str, SMSruSendSms]


class SMSruCheckSms(SMSruBase):
    cost: Optional[float]


class SMSruCheckSmsResponse(SMSruWithBalance):
    sms: Dict[str, SMSruCheckSms]
