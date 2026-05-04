# guests_service/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    port: int = 8003

    class Config:
        env_file = ".env"

settings = Settings()
