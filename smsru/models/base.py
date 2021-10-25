from typing import Optional

from pydantic import BaseModel


class SMSruBase(BaseModel):
    status: str
    status_code: int
    status_text: Optional[str]


class SMSruWithBalance(SMSruBase):
    balance: float
