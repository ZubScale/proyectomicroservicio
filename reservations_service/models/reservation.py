# reservations_service/models/reservation.py
from sqlalchemy import Column, Integer, String, Date, Float
from reservations_service.database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    guest_id = Column(Integer, index=True)
    room_id = Column(Integer, index=True)
    check_in = Column(Date)
    check_out = Column(Date)
    total_price = Column(Float)
    status = Column(String(50), default="confirmed")
