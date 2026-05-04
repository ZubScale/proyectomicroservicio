# reservations_service/routers/reservations.py
import httpx
import json
import redis
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from reservations_service.database import get_db
from reservations_service.models.reservation import Reservation
from reservations_service.schemas.reservation import ReservationCreate, ReservationResponse, ReservationEvent
from reservations_service.config import settings

router = APIRouter(prefix="/reservations", tags=["reservations"])

redis_client = redis.from_url(settings.redis_url)

@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(res: ReservationCreate, db: Session = Depends(get_db)):
    # 1. Call Availability Service
    availability_payload = {
        "room_id": res.room_id,
        "check_in": res.check_in.isoformat(),
        "check_out": res.check_out.isoformat()
    }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(f"{settings.availability_service_url}/availability/record", json=availability_payload)
            if resp.status_code == 409:
                raise HTTPException(status_code=409, detail="Room is not available for these dates")
            resp.raise_for_status()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Availability service unavailable")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 409:
             raise HTTPException(status_code=409, detail="Room is not available for these dates")
        raise HTTPException(status_code=500, detail="Error communicating with availability service")

    # 2. Save reservation
    # We use run_in_threadpool since db.commit() is a synchronous blocking operation
    from fastapi.concurrency import run_in_threadpool

    def save_reservation():
        new_res = Reservation(**res.model_dump())
        db.add(new_res)
        db.commit()
        db.refresh(new_res)
        return new_res

    new_res = await run_in_threadpool(save_reservation)

    # 3. Publish event
    event = ReservationEvent(
        reservation_id=str(new_res.id),
        guest_id=str(new_res.guest_id),
        room_id=str(new_res.room_id),
        check_in=new_res.check_in.isoformat(),
        check_out=new_res.check_out.isoformat(),
        timestamp=datetime.utcnow().isoformat()
    )

    # Publish event synchronously, but wrap in an executor to avoid blocking the event loop
    import asyncio
    try:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None,
            lambda: redis_client.publish("reserva.confirmada", json.dumps(event.model_dump()))
        )
    except Exception as e:
        # We don't fail the reservation if event publishing fails, but we could log it
        print(f"Failed to publish event: {e}")

    return new_res

@router.get("/", response_model=List[ReservationResponse])
def get_reservations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Reservation).offset(skip).limit(limit).all()

@router.get("/{reservation_id}", response_model=ReservationResponse)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    db_res = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not db_res:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_res
