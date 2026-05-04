# billing_service/schemas/invoice.py
from pydantic import BaseModel
from datetime import datetime

class InvoiceBase(BaseModel):
    reservation_id: int
    amount: float

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceResponse(InvoiceBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
