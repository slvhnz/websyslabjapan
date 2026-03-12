from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env.local if it exists
env_path = Path(__file__).resolve().parent.parent / ".env.local"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
Base = declarative_base()

# Only create engine when actually needed
_engine = None
_session_factory = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args={"sslmode": "prefer"}
        )
    return _engine

def get_session_factory():
    global _session_factory
    if _session_factory is None:
        _session_factory = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _session_factory

def SessionLocal():
    """Factory function - creates a new session when called"""
    factory = get_session_factory()
    return factory()

# Export for backwards compatibility
engine = None  # Placeholder, actual engine created lazily on first use
