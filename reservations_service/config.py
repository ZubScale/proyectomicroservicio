# reservations_service/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    port: int = 8004
    redis_url: str = "redis://localhost:6379"
    availability_service_url: str = "http://availability_service:8007"

    class Config:
        env_file = ".env"

settings = Settings()
