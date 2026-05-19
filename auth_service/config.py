# auth_service/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    port: int = 8001
    jwt_secret: str = "default_unsafe_secret"
    jwt_algorithm: str = "HS256"

settings = Settings()
