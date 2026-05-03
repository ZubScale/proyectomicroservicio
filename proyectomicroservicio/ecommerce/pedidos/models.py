# pedidos/models.py
from sqlalchemy import Column, Integer, Float, String, JSON
from .database import Base


class Pedido(Base):
    __tablename__ = "pedidos"

    id         = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False)
    items      = Column(JSON,    nullable=False)
    total      = Column(Float,   nullable=False)
    estado     = Column(String,  default="confirmado")
    creado_en  = Column(String,  nullable=False)
