# notifications_service/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from notifications_service.services.redis_consumer import start_consumer

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the Redis consumer in a background thread when the app starts
    start_consumer()
    yield
    # Shutdown logic if needed

app = FastAPI(title="Notifications Service", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Welcome to Notifications Service. Listening for events..."}
