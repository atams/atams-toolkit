from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# Global variables untuk engine dan session
engine = None
SessionLocal = None


def init_database(database_url: str, debug: bool = False):
    """
    Initialize database engine dan session

    Args:
        database_url: Database connection URL
        debug: Enable SQL echo for debugging
    """
    global engine, SessionLocal

    # Normalisasi URL database (postgres:// -> postgresql+psycopg2://)
    db_url = database_url
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)

    engine = create_engine(
        db_url,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=debug,
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    if SessionLocal is None:
        raise RuntimeError(
            "Database not initialized. Call init_database() first."
        )

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
