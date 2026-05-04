# availability_service/models/availability.py
from sqlalchemy import Column, Integer, String, Date
from availability_service.database import Base

class AvailabilityRecord(Base):
    """
    Keeps track of confirmed reservations to prevent double booking.
    """
    __tablename__ = "availability_records"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, index=True)
    check_in = Column(Date)
    check_out = Column(Date)
