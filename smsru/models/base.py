from pydantic import BaseModel


class SMSruBase(BaseModel):
    status: str
    status_code: int


class SMSruWithBalance(SMSruBase):
    balance: float
