# pedidos/main.py  —  Puerto 8003
from fastapi import FastAPI, HTTPException, Depends
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
import httpx

from .schemas import PedidoCreate, PedidoPublico, EstadoPedido, ItemDetalle
from .database import engine, get_db
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Servicio de Pedidos", version="1.0.0")

# URLs de los otros servicios (en producción vendrían de variables de entorno)
USUARIOS_URL  = "http://localhost:8001"
PRODUCTOS_URL = "http://localhost:8002"


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.post("/pedidos/", response_model=PedidoPublico, status_code=201)
async def crear_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):

    async with httpx.AsyncClient() as client:

        # 1. Verificar que el usuario existe
        resp = await client.get(f"{USUARIOS_URL}/usuarios/{pedido.usuario_id}")
        if resp.status_code == 404:
            raise HTTPException(404, "Usuario no encontrado")

        items_detalle = []
        total = 0.0

        # 2. Verificar stock y calcular total
        for item in pedido.items:
            resp = await client.get(f"{PRODUCTOS_URL}/productos/{item.producto_id}")
            if resp.status_code == 404:
                raise HTTPException(404, f"Producto {item.producto_id} no existe")
            producto = resp.json()
            if producto["stock"] < item.cantidad:
                raise HTTPException(
                    409, f"Stock insuficiente para '{producto['nombre']}'"
                )
            subtotal = producto["precio"] * item.cantidad
            items_detalle.append(ItemDetalle(
                producto_id=item.producto_id,
                nombre=producto["nombre"],
                precio=producto["precio"],
                cantidad=item.cantidad,
                subtotal=subtotal,
            ))
            total += subtotal

        # 3. Descontar stock en el servicio de Productos
        for item in pedido.items:
            await client.patch(
                f"{PRODUCTOS_URL}/productos/{item.producto_id}/stock",
                json={"cantidad": -item.cantidad},
            )

    # 4. Guardar el pedido en la base de datos
    nuevo = models.Pedido(
        usuario_id=pedido.usuario_id,
        items=[i.dict() for i in items_detalle],
        total=round(total, 2),
        estado=EstadoPedido.confirmado,
        creado_en=datetime.utcnow().isoformat(),
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return PedidoPublico(
        id=nuevo.id,
        usuario_id=nuevo.usuario_id,
        items=nuevo.items,
        total=nuevo.total,
        estado=nuevo.estado,
        creado_en=nuevo.creado_en,
    )


@app.get("/pedidos/{pedido_id}", response_model=PedidoPublico)
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db)):
    p = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if not p:
        raise HTTPException(404, "Pedido no encontrado")
    return PedidoPublico(
        id=p.id,
        usuario_id=p.usuario_id,
        items=p.items,
        total=p.total,
        estado=p.estado,
        creado_en=p.creado_en,
    )


@app.delete("/pedidos/reset", status_code=200)
def reset_pedidos(db: Session = Depends(get_db)):
    eliminados = db.query(models.Pedido).delete()
    db.commit()
    return {"mensaje": f"{eliminados} pedidos eliminados"}


@app.get("/pedidos/", response_model=list[PedidoPublico])
def listar_pedidos(usuario_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(models.Pedido)
    if usuario_id:
        query = query.filter(models.Pedido.usuario_id == usuario_id)
    return [
        PedidoPublico(
            id=p.id,
            usuario_id=p.usuario_id,
            items=p.items,
            total=p.total,
            estado=p.estado,
            creado_en=p.creado_en,
        )
        for p in query.all()
    ]
