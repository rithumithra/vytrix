from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

from sqlalchemy.engine.url import make_url

# Database engine setup
url = make_url(settings.database_url)
if url.drivername.startswith("sqlite"):
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )
else:
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=10,
        max_overflow=20,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Database dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Redis Setup
redis_client = None
if getattr(settings, "redis_url", None):
    import redis
    redis_client = redis.from_url(settings.redis_url, decode_responses=True)


# InfluxDB Setup
influx_client = None
if getattr(settings, "influxdb_url", None) and getattr(settings, "influxdb_token", None) and getattr(settings, "influxdb_org", None):
    from influxdb_client import InfluxDBClient
    influx_client = InfluxDBClient(
        url=settings.influxdb_url,
        token=settings.influxdb_token,
        org=settings.influxdb_org
    )