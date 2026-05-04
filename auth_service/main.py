# auth_service/main.py
from fastapi import FastAPI
from auth_service.routers import auth
from auth_service.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service")

app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Auth Service"}
