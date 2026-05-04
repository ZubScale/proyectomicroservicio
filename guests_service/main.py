# guests_service/main.py
from fastapi import FastAPI
from guests_service.routers import guests
from guests_service.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Guests Service")

app.include_router(guests.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Guests Service"}
