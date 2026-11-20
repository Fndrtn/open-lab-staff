from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .user_models import Base

DATABASE_URL = 'sqlite:///./auth.db'
engine = create_engine(
    DATABASE_URL,
)


session_factory = sessionmaker(
    bind=engine,
)


def get_db() -> Generator[Session]:
    db = session_factory()

    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    Base.metadata.create_all(engine)
