# guests_service/schemas/guest.py
from pydantic import BaseModel, EmailStr

class GuestBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str

class GuestCreate(GuestBase):
    pass

class GuestUpdate(GuestBase):
    pass

class GuestResponse(GuestBase):
    id: int

    class Config:
        from_attributes = True
