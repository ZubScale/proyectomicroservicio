# availability_service/routers/availability.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from availability_service.database import get_db
from availability_service.models.availability import AvailabilityRecord
from availability_service.schemas.availability import AvailabilityCheckRequest, AvailabilityCheckResponse, AvailabilityRecordCreate, AvailabilityRecordResponse

router = APIRouter(prefix="/availability", tags=["availability"])

@router.post("/check", response_model=AvailabilityCheckResponse)
def check_availability(request: AvailabilityCheckRequest, db: Session = Depends(get_db)):
    # Check if there is any overlapping record for the room
    # Overlap condition: existing_check_in < new_check_out AND existing_check_out > new_check_in
    overlap = db.query(AvailabilityRecord).filter(
        AvailabilityRecord.room_id == request.room_id,
        AvailabilityRecord.check_in < request.check_out,
        AvailabilityRecord.check_out > request.check_in
    ).first()

    return AvailabilityCheckResponse(available=overlap is None)

@router.post("/record", response_model=AvailabilityRecordResponse, status_code=status.HTTP_201_CREATED)
def record_booking(record: AvailabilityRecordCreate, db: Session = Depends(get_db)):
    # First check availability to prevent race conditions
    overlap = db.query(AvailabilityRecord).filter(
        AvailabilityRecord.room_id == record.room_id,
        AvailabilityRecord.check_in < record.check_out,
        AvailabilityRecord.check_out > record.check_in
    ).first()

    if overlap:
        raise HTTPException(status_code=409, detail="Room is not available for these dates")

    new_record = AvailabilityRecord(**record.model_dump())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record
