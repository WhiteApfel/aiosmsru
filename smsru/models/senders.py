from typing import List

from . import SMSruBase


class SMSruSenders(SMSruBase):
    senders: List[str]
