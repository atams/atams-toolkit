"""
Database Layer
==============
Provides database session management and base repository pattern.

Usage:
    from atams.db import Base, get_db, BaseRepository, init_database
"""
from atams.db.base import Base
from atams.db.session import SessionLocal, engine, get_db, init_database
from atams.db.repository import BaseRepository

__all__ = [
    "Base",
    "SessionLocal",
    "engine",
    "get_db",
    "init_database",
    "BaseRepository",
]
