# billing_service/main.py
from fastapi import FastAPI
from billing_service.routers import billing
from billing_service.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Billing Service")

app.include_router(billing.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Billing Service"}
