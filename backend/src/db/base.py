
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.core.config import settings

Base = declarative_base()
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Helps prevent stale connections
    echo=True  # Enables SQL query logging for debugging (optional)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)