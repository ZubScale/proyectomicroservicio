# rooms_service/schemas/room.py
from pydantic import BaseModel

class RoomBase(BaseModel):
    number: str
    type: str
    price_per_night: float

class RoomCreate(RoomBase):
    pass

class RoomUpdate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int

    class Config:
        from_attributes = True
