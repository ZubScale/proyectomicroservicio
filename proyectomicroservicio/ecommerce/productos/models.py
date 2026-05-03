# productos/models.py
from sqlalchemy import Column, Integer, String, Float
from .database import Base


class Producto(Base):
    __tablename__ = "productos"

    id          = Column(Integer, primary_key=True, index=True)
    nombre      = Column(String,  nullable=False)
    precio      = Column(Float,   nullable=False)
    stock       = Column(Integer, default=0)
    descripcion = Column(String,  nullable=True)
