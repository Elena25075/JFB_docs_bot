from __future__ import annotations

import os
import time
from collections.abc import Iterator

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

ALLOWED_TEST_DB_HOSTS = {"localhost", "127.0.0.1", "::1"}


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
    raw = os.getenv("TEST_DATABASE_URL")
    if not raw:
        pytest.fail(
            "TEST_DATABASE_URL is required for DB integration tests. "
            "Refusing to use DATABASE_URL for destructive test setup."
        )

    parsed = make_url(raw)
    db_name = parsed.database or ""
    if not db_name.endswith("_test"):
        pytest.fail(
            "Unsafe TEST_DATABASE_URL database name detected. "
            "Database name must end with '_test'."
        )
    if parsed.host not in ALLOWED_TEST_DB_HOSTS:
        pytest.fail(
            "Unsafe TEST_DATABASE_URL host detected. "
            "Allowed hosts for destructive reset: localhost, 127.0.0.1, ::1."
        )
    if os.getenv("ALLOW_DESTRUCTIVE_TEST_DB_RESET") != "1":
        pytest.skip(
            "Destructive DB reset is disabled. "
            "Set ALLOW_DESTRUCTIVE_TEST_DB_RESET=1 to run DB integration tests."
        )

    return raw


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

    with engine.connect() as connection:
        connection = connection.execution_options(isolation_level="AUTOCOMMIT")
        connection.execute(text("TRUNCATE TABLE doc_themes, docs, themes RESTART IDENTITY CASCADE"))

    engine.dispose()
