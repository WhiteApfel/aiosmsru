from typing import Optional, Dict

from . import SMSruWithBalance, SMSruBase


class SMSruSendSms(SMSruBase):
    sms_id: Optional[str]


class SMSruSendSmsResponse(SMSruWithBalance):
    sms: Dict[str, SMSruSendSms]
