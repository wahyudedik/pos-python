"""
Database Configuration & Setup
SQLAlchemy connection dan session management
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool
from typing import Optional
import logging

from src.config.settings import DATABASE_URL, DATABASE_ECHO

logger = logging.getLogger(__name__)

# Base class untuk semua ORM models
Base = declarative_base()

# Create engine
if "sqlite" in DATABASE_URL:
    # SQLite settings
    engine = create_engine(
        DATABASE_URL,
        echo=DATABASE_ECHO,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    # PostgreSQL atau MySQL settings
    engine = create_engine(
        DATABASE_URL,
        echo=DATABASE_ECHO,
        pool_size=10,
        pool_recycle=3600,
        pool_pre_ping=True,
    )

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """
    Dependency untuk get database session
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session():
    """Get a new database session"""
    return SessionLocal()


def init_db() -> None:
    """Initialize database - create all tables."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


def drop_db() -> None:
    """Drop all tables - WARNING: This deletes all data!"""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.warning("All database tables dropped!")
    except Exception as e:
        logger.error(f"Error dropping database: {e}")
        raise
