# rooms_service/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    port: int = 8002

    class Config:
        env_file = ".env"

settings = Settings()
