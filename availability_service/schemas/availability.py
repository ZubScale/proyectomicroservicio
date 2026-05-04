# availability_service/schemas/availability.py
from pydantic import BaseModel
from datetime import date

class AvailabilityCheckRequest(BaseModel):
    room_id: int
    check_in: date
    check_out: date

class AvailabilityCheckResponse(BaseModel):
    available: bool

class AvailabilityRecordCreate(BaseModel):
    room_id: int
    check_in: date
    check_out: date

class AvailabilityRecordResponse(BaseModel):
    id: int
    room_id: int
    check_in: date
    check_out: date

    class Config:
        from_attributes = True
