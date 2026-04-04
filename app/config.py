import json
import os
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings


def load_json_config():
    config_path = Path(__file__).resolve().parents[1] / "config.json"
    if not config_path.exists():
        return {}
    try:
        return json.loads(config_path.read_text())
    except json.JSONDecodeError:
        return {}


def build_database_url(cfg: dict) -> str:
    if not cfg:
        return "sqlite:///./vytrix.db"
    if cfg.get("url"):
        return cfg["url"]

    driver = cfg.get("driver", "sqlite")
    if driver == "sqlite":
        db_path = cfg.get("db", "./vytrix.db")
        return f"sqlite:///{db_path}"
    else:
        # For PostgreSQL or others
        user = cfg.get("user", "vytrix_user")
        password = cfg.get("password", "vytrix_password")
        host = cfg.get("host", "localhost")
        port = cfg.get("port", 5432)
        db = cfg.get("db", "vytrix_db")
        return f"{driver}://{user}:{password}@{host}:{port}/{db}"


json_config = load_json_config()
local_database_config = json_config.get("database", {})
local_database_url = build_database_url(local_database_config)
local_redis_url = json_config.get("redis", {}).get("url")
local_influx_config = json_config.get("influxdb", {})
local_influx_url = local_influx_config.get("url")
local_influx_token = local_influx_config.get("token")
local_influx_org = local_influx_config.get("org")


class Settings(BaseSettings):
    # Database configuration
    # Use DATABASE_URL to connect to PostgreSQL in development or production.
    # If DATABASE_URL is not provided, the app will build a local Postgres URL
    # from config.json or use a default local Postgres config.
    database_url: str = os.getenv("DATABASE_URL", local_database_url)

    # Security
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    # Application Settings
    debug: bool = True
    log_level: str = "INFO"

    # Optional external services
    redis_url: Optional[str] = os.getenv("REDIS_URL", local_redis_url)
    influxdb_url: Optional[str] = os.getenv("INFLUXDB_URL", local_influx_url)
    influxdb_token: Optional[str] = os.getenv("INFLUXDB_TOKEN", local_influx_token)
    influxdb_org: Optional[str] = os.getenv("INFLUXDB_ORG", local_influx_org)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()