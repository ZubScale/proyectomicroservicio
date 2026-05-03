# usuarios/models.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

""" 
Modelo de Usuario para la base de datos de usuarios.
Contiene campos para id, nombre, email, password y fecha de creación.
Representa la tabla en la base de datos. Define columnas, tipos SQL, índices y restricciones. 
SQLAlchemy la usa para crear la tabla y para leer/escribir registros. 
Tiene los 5 campos reales que se guardan en disco, incluyendo password
"""
class Usuario(Base):
    __tablename__ = "usuarios"

    id        = Column(Integer, primary_key=True, index=True)
    nombre    = Column(String,  nullable=False)
    email     = Column(String,  unique=True, index=True, nullable=False)
    password  = Column(String,  nullable=False)
    creado_en = Column(DateTime, default=datetime.utcnow)
