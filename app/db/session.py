"""Synchronous SQLAlchemy engine/session helpers."""

from __future__ import annotations

from contextlib import contextmanager
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.config import get_database_url


@lru_cache(maxsize=1)
def create_db_engine() -> Engine:
    return create_engine(get_database_url(), pool_pre_ping=True)


@lru_cache(maxsize=1)
def get_session_factory() -> sessionmaker[Session]:
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        class_=Session,
        bind=create_db_engine(),
    )


@contextmanager
def get_session() -> Session:
    session = get_session_factory()()
    try:
        yield session
    finally:
        session.close()
