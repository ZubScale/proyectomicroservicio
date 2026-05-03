# usuarios/main.py  —  Puerto 8001
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from datetime import datetime
from sqlalchemy.orm import Session

from .database import engine, get_db
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Servicio de Usuarios", version="1.0.0")


# ── Schemas ──────────────────────────────────────────────────────────────────

class UsuarioCreate(BaseModel):
    nombre:   str
    email:    EmailStr
    password: str


class UsuarioPublico(BaseModel):
    id:        int
    nombre:    str
    email:     str
    creado_en: datetime

    class Config:
        from_attributes = True


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.post("/usuarios/", response_model=UsuarioPublico, status_code=201)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existe = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if existe:
        raise HTTPException(409, "Email ya registrado")
    nuevo = models.Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password=usuario.password,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@app.get("/usuarios/{usuario_id}", response_model=UsuarioPublico)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(404, f"Usuario {usuario_id} no encontrado")
    return usuario


@app.get("/usuarios/", response_model=list[UsuarioPublico])
def listar_usuarios(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(models.Usuario).offset(skip).limit(limit).all()


@app.delete("/usuarios/reset", status_code=200)
def reset_usuarios(db: Session = Depends(get_db)):
    eliminados = db.query(models.Usuario).delete()
    db.commit()
    return {"mensaje": f"{eliminados} usuarios eliminados"}
