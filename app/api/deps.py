from typing import Generator
from sqlalchemy.orm import Session
from app.core.database import SessionLocal


def get_db() -> Generator:
    """Database dependency."""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
