# billing_service/models/invoice.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from billing_service.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, unique=True, index=True)
    amount = Column(Float)
    status = Column(String, default="generated")
    created_at = Column(DateTime, default=datetime.utcnow)
