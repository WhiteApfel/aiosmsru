from typing import Optional

from . import SMSruBase


class SMSruLimit(SMSruBase):
    total_limit: Optional[int]
    used_today: Optional[int]


class SMSruFreeLimit(SMSruBase):
    total_free: Optional[int]
    used_today: Optional[int]
