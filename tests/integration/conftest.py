from __future__ import annotations

import time
from collections.abc import Iterator

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from app.db.config import get_test_database_url


def _build_alembic_config(database_url: str) -> Config:
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", database_url)
    return config


def _reset_public_schema(engine: Engine) -> None:
    with engine.connect() as connection:
        connection = connection.execution_options(isolation_level="AUTOCOMMIT")
        connection.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))
        connection.execute(text("GRANT ALL ON SCHEMA public TO CURRENT_USER"))


@pytest.fixture(scope="session")
def database_url() -> str:
    return get_test_database_url()


@pytest.fixture(scope="session")
def migrated_database(database_url: str) -> Iterator[str]:
    engine = create_engine(database_url, pool_pre_ping=True)
    ready = False
    for _ in range(15):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            ready = True
            break
        except SQLAlchemyError:
            time.sleep(1)

    if not ready:
        engine.dispose()
        pytest.skip("Postgres is not reachable; skipping DB integration tests.")

    _reset_public_schema(engine)
    command.upgrade(_build_alembic_config(database_url), "head")
    engine.dispose()
    yield database_url


@pytest.fixture()
def db_session(migrated_database: str) -> Iterator[Session]:
    engine = create_engine(migrated_database, pool_pre_ping=True)
    session_factory = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        class_=Session,
    )

    with session_factory() as session:
        yield session
        session.rollback()

    engine.dispose()
