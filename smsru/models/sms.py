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


class SMSruSmsCost(SMSruBase):
    cost: Optional[float]
    sms: Optional[int]


class SMSruSmsCostResponse(SMSruBase):
    sms: Dict[str, SMSruSmsCost]
    total_cost: float
    total_sms: int
