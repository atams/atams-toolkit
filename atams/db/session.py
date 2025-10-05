"""
Database Session Management
===========================
Provides database engine, session factory, and get_db dependency.

Usage in user project:
    # In app/db/session.py (user project)
    from atams.db.session import create_session_factory, get_db_factory
    from app.core.config import settings

    SessionLocal = create_session_factory(settings)
    get_db = get_db_factory(SessionLocal)

Or simpler with init_database:
    # In app/main.py
    from atams.db import init_database
    from app.core.config import settings

    init_database(settings.DATABASE_URL, settings.DEBUG)
"""
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator, TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from atams.config.base import AtamsBaseSettings


def normalize_database_url(db_url: str) -> str:
    """
    Normalize database URL (postgres:// -> postgresql+psycopg2://)

    Args:
        db_url: Original database URL

    Returns:
        Normalized database URL
    """
    if db_url.startswith("postgres://"):
        return db_url.replace("postgres://", "postgresql+psycopg2://", 1)
    return db_url


def create_engine_from_settings(settings: 'AtamsBaseSettings') -> Engine:
    """
    Create SQLAlchemy engine from settings

    Args:
        settings: Application settings

    Returns:
        SQLAlchemy engine
    """
    db_url = normalize_database_url(settings.DATABASE_URL)

    return create_engine(
        db_url,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=settings.DEBUG,
    )


def create_session_factory(settings: 'AtamsBaseSettings'):
    """
    Create session factory from settings

    Args:
        settings: Application settings

    Returns:
        SessionLocal factory
    """
    engine = create_engine_from_settings(settings)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_factory(session_factory) -> Callable:
    """
    Create get_db dependency function

    Args:
        session_factory: SessionLocal factory

    Returns:
        get_db function
    """
    def get_db() -> Generator[Session, None, None]:
        """Dependency to get database session"""
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    return get_db


# Global variables (will be initialized by init_database)
engine: Engine = None
SessionLocal = None


def init_database(database_url: str, debug: bool = False) -> None:
    """
    Initialize database engine and session factory

    This is the main function to call in user projects.

    Args:
        database_url: Database connection URL
        debug: Enable SQL echo

    Example:
        from atams.db import init_database
        from app.core.config import settings

        init_database(settings.DATABASE_URL, settings.DEBUG)
    """
    global engine, SessionLocal

    db_url = normalize_database_url(database_url)

    engine = create_engine(
        db_url,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=debug,
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session

    Must call init_database() first!

    Example:
        from fastapi import Depends
        from atams.db import get_db

        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    if SessionLocal is None:
        raise RuntimeError(
            "Database not initialized! Call init_database() first in your main.py"
        )

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
