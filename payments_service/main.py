# payments_service/main.py
from fastapi import FastAPI
from payments_service.routers import payments
from payments_service.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Payments Service")

app.include_router(payments.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Payments Service"}
