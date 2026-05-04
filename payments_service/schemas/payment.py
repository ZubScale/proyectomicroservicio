# payments_service/schemas/payment.py
from pydantic import BaseModel
from typing import Optional

class PaymentBase(BaseModel):
    reservation_id: int
    amount: float
    currency: str = "USD"

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    status: str
    transaction_id: Optional[str] = None

class PaymentResponse(PaymentBase):
    id: int
    status: str
    transaction_id: Optional[str] = None

    class Config:
        from_attributes = True
