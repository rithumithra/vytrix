from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database Configuration - Using SQLite for simplicity
    database_url: str = "sqlite:///./vytrix.db"
    redis_url: str = "redis://localhost:6379/0"
    influxdb_url: str = "http://localhost:8086"
    influxdb_token: str = "vytrix-super-secret-auth-token"
    influxdb_org: str = "vytrix"
    influxdb_bucket: str = "gps_tracking"
    
    # Security
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    
    # External APIs
    weather_api_key: Optional[str] = None
    weather_api_url: str = "https://api.openweathermap.org/data/2.5"
    payment_api_key: Optional[str] = None
    sms_api_key: Optional[str] = None
    
    # Application Settings
    debug: bool = True
    log_level: str = "INFO"
    max_workers: int = 4
    
    class Config:
        env_file = ".env"


settings = Settings()