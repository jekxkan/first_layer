from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

DATABASE_URL = "sqlite:///D:/code/first_layer/data/database.sqlite"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Зависимость FastAPI, которая предоставляет сессию БД.
    Используйте её в эндпоинтах через Depends(get_db).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()