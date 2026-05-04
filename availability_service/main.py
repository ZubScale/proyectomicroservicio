# availability_service/main.py
from fastapi import FastAPI
from availability_service.routers import availability
from availability_service.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Availability Service")

app.include_router(availability.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Availability Service"}
