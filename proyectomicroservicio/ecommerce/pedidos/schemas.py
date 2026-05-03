# pedidos/schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class EstadoPedido(str, Enum):
    pendiente  = "pendiente"
    confirmado = "confirmado"
    cancelado  = "cancelado"


class ItemPedido(BaseModel):
    producto_id: int
    cantidad:    int = Field(..., gt=0)


class PedidoCreate(BaseModel):
    usuario_id: int
    items:      list[ItemPedido]


class ItemDetalle(BaseModel):
    producto_id: int
    nombre:      str
    precio:      float
    cantidad:    int
    subtotal:    float


class PedidoPublico(BaseModel):
    id:         int
    usuario_id: int
    items:      list[ItemDetalle]
    total:      float
    estado:     EstadoPedido
    creado_en:  str
