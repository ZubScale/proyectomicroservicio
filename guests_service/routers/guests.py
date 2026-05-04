# guests_service/routers/guests.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from guests_service.database import get_db
from guests_service.models.guest import Guest
from guests_service.schemas.guest import GuestCreate, GuestUpdate, GuestResponse

router = APIRouter(prefix="/guests", tags=["guests"])

@router.post("/", response_model=GuestResponse, status_code=status.HTTP_201_CREATED)
def create_guest(guest: GuestCreate, db: Session = Depends(get_db)):
    db_guest = db.query(Guest).filter(Guest.email == guest.email).first()
    if db_guest:
        raise HTTPException(status_code=409, detail="Email already registered")

    new_guest = Guest(**guest.model_dump())
    db.add(new_guest)
    db.commit()
    db.refresh(new_guest)
    return new_guest

@router.get("/", response_model=List[GuestResponse])
def get_guests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Guest).offset(skip).limit(limit).all()

@router.get("/{guest_id}", response_model=GuestResponse)
def get_guest(guest_id: int, db: Session = Depends(get_db)):
    db_guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not db_guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return db_guest

@router.put("/{guest_id}", response_model=GuestResponse)
def update_guest(guest_id: int, guest: GuestUpdate, db: Session = Depends(get_db)):
    db_guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not db_guest:
        raise HTTPException(status_code=404, detail="Guest not found")

    for key, value in guest.model_dump().items():
        setattr(db_guest, key, value)

    db.commit()
    db.refresh(db_guest)
    return db_guest

@router.delete("/{guest_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_guest(guest_id: int, db: Session = Depends(get_db)):
    db_guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not db_guest:
        raise HTTPException(status_code=404, detail="Guest not found")

    db.delete(db_guest)
    db.commit()
    return None
