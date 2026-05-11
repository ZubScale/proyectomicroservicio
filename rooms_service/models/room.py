# rooms_service/models/room.py
from sqlalchemy import Column, Integer, String, Float
from rooms_service.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(20), unique=True, index=True)
    type = Column(String(50))
    price_per_night = Column(Float)
