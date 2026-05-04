# payments_service/routers/payments.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from payments_service.database import get_db
from payments_service.models.payment import Payment
from payments_service.schemas.payment import PaymentCreate, PaymentUpdate, PaymentResponse

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    new_payment = Payment(**payment.model_dump())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@router.get("/", response_model=List[PaymentResponse])
def get_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Payment).offset(skip).limit(limit).all()

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: int, payment: PaymentUpdate, db: Session = Depends(get_db)):
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    db_payment.status = payment.status
    if payment.transaction_id:
        db_payment.transaction_id = payment.transaction_id
    elif payment.status == "completed" and not db_payment.transaction_id:
        db_payment.transaction_id = str(uuid.uuid4())

    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    db.delete(db_payment)
    db.commit()
    return None
