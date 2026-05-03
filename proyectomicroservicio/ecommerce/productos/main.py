# productos/main.py  —  Puerto 8002
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session

from .database import engine, get_db
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Servicio de Productos", version="1.0.0")


# ── Schemas ──────────────────────────────────────────────────────────────────

class ProductoCreate(BaseModel):
    nombre:      str   = Field(..., min_length=3)
    precio:      float = Field(..., gt=0)
    stock:       int   = Field(default=0, ge=0)
    descripcion: Optional[str] = None


class ProductoPublico(ProductoCreate):
    id: int

    class Config:
        from_attributes = True


class StockUpdate(BaseModel):
    cantidad: int = Field(..., description="Negativo para reducir stock")


# ── Datos iniciales ───────────────────────────────────────────────────────────

def seed(db: Session):
    if db.query(models.Producto).count() == 0:
        db.add_all([
            models.Producto(nombre="Laptop Pro",   precio=1299.99, stock=10, descripcion="16GB RAM"),
            models.Producto(nombre="Teclado Mec.", precio=149.99,  stock=35, descripcion="Cherry MX"),
            models.Producto(nombre="Monitor 4K",   precio=699.99,  stock=8,  descripcion="27 pulgadas"),
        ])
        db.commit()


@app.on_event("startup")
def startup():
    db = next(get_db())
    seed(db)


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/productos/", response_model=list[ProductoPublico])
def listar(db: Session = Depends(get_db)):
    return db.query(models.Producto).all()


@app.get("/productos/{pid}", response_model=ProductoPublico)
def obtener(pid: int, db: Session = Depends(get_db)):
    p = db.query(models.Producto).filter(models.Producto.id == pid).first()
    if not p:
        raise HTTPException(404, "Producto no encontrado")
    return p


@app.post("/productos/", response_model=ProductoPublico, status_code=201)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    nuevo = models.Producto(**producto.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@app.delete("/productos/reset", status_code=200)
def reset_productos(db: Session = Depends(get_db)):
    db.query(models.Producto).delete()
    db.commit()
    seed(db)
    return {"mensaje": "Productos restablecidos a datos iniciales"}


@app.patch("/productos/{pid}/stock")
def actualizar_stock(pid: int, update: StockUpdate, db: Session = Depends(get_db)):
    p = db.query(models.Producto).filter(models.Producto.id == pid).first()
    if not p:
        raise HTTPException(404, "Producto no encontrado")
    nuevo_stock = p.stock + update.cantidad
    if nuevo_stock < 0:
        raise HTTPException(409, "Stock insuficiente")
    p.stock = nuevo_stock
    db.commit()
    return {"producto_id": pid, "stock_actual": nuevo_stock}
