from sqlalchemy.orm import Session
from src.db.base import SessionLocal


def get_db() -> Session:
    """
    Dependency function to provide a database session.
    Ensures that the session is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()