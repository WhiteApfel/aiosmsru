from typing import Optional

from smsru.models import SMSruWithBalance


class SMSruCallcheck(SMSruWithBalance):
    status_code: None = None
    cost: Optional[float]
    code: str
    call_id: str
