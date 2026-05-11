# payments_service/models/payment.py
from sqlalchemy import Column, Integer, String, Float
from payments_service.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, index=True)
    amount = Column(Float)
    currency = Column(String(10), default="USD")
    status = Column(String(50), default="pending")
    transaction_id = Column(String(255), unique=True, index=True, nullable=True)
