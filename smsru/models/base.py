from pydantic import BaseModel


class SMSruResponse(BaseModel):
    status: str
    status_code: int


class SMSruWithBalance(SMSruResponse):
    balance: float
