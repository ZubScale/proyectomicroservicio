# auth_service/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    port: int = 8001
    jwt_secret: str = "default_unsafe_secret"
    jwt_algorithm: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()
