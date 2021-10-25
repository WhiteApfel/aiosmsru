from typing import Dict

from . import SMSruBase


class SMSruStoplist(SMSruBase):
    stoplist: Dict[str, str]
