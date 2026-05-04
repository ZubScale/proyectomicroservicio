# payments_service/models/payment.py
from sqlalchemy import Column, Integer, String, Float
from payments_service.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, index=True)
    amount = Column(Float)
    currency = Column(String, default="USD")
    status = Column(String, default="pending")
    transaction_id = Column(String, unique=True, index=True, nullable=True)
