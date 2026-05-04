# reservations_service/main.py
from fastapi import FastAPI
from reservations_service.routers import reservations
from reservations_service.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Reservations Service")

app.include_router(reservations.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Reservations Service"}
