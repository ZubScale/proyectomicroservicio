# notifications_service/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    port: int = 8006
    redis_url: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"

settings = Settings()
