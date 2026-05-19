# reservations_service/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    port: int = 8004
    redis_url: str = "redis://localhost:6379"
    availability_service_url: str = "http://availability_service:8007"

settings = Settings()
