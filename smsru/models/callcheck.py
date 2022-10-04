from typing import Optional

from smsru.models import SMSruWithBalance


class SMSruCallcheck(SMSruWithBalance):
    cost: Optional[float]
    code: str
    call_id: str
