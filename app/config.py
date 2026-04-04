from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database Configuration - Using SQLite for simplicity
    database_url: str = "sqlite:///./vytrix.db"
    
    # Security
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    
    # Application Settings
    debug: bool = True
    log_level: str = "INFO"
    
    # Optional external services
    redis_url: Optional[str] = None
    influxdb_url: Optional[str] = None
    influxdb_token: Optional[str] = None
    influxdb_org: Optional[str] = None

settings = Settings()