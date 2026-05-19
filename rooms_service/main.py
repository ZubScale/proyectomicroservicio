# rooms_service/main.py
from fastapi import FastAPI
from rooms_service.routers import rooms
from rooms_service.database import engine, Base, wait_for_db

wait_for_db()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rooms Service")

app.include_router(rooms.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Rooms Service"}
