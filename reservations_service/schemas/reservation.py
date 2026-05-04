# reservations_service/schemas/reservation.py
from pydantic import BaseModel
from datetime import date, datetime

class ReservationBase(BaseModel):
    guest_id: int
    room_id: int
    check_in: date
    check_out: date
    total_price: float

class ReservationCreate(ReservationBase):
    pass

class ReservationResponse(ReservationBase):
    id: int
    status: str

    class Config:
        from_attributes = True

class ReservationEvent(BaseModel):
    event: str = "reserva.confirmada"
    reservation_id: str
    guest_id: str
    room_id: str
    check_in: str
    check_out: str
    timestamp: str
