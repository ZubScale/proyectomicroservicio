# api_gateway/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    port: int = 8000

    # Service URLs
    auth_service_url: str = "http://auth_service:8001"
    rooms_service_url: str = "http://rooms_service:8002"
    guests_service_url: str = "http://guests_service:8003"
    reservations_service_url: str = "http://reservations_service:8004"
    payments_service_url: str = "http://payments_service:8005"
    notifications_service_url: str = "http://notifications_service:8006"
    availability_service_url: str = "http://availability_service:8007"
    billing_service_url: str = "http://billing_service:8008"

    jwt_secret: str = "default_unsafe_secret"
    jwt_algorithm: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()
