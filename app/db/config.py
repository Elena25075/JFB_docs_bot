"""Database configuration helpers sourced from environment variables."""

from __future__ import annotations

import os
from urllib.parse import quote_plus


def _env(name: str, default: str) -> str:
    return os.getenv(name, default)


def build_database_url() -> str:
    """Build Postgres URL from individual env vars."""
    user = quote_plus(_env("POSTGRES_USER", "jfb_user"))
    password = quote_plus(_env("POSTGRES_PASSWORD", "jfb_password"))
    host = _env("POSTGRES_HOST", "localhost")
    port = _env("POSTGRES_PORT", "5432")
    database = _env("POSTGRES_DB", "jfb_docs")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"


def get_database_url() -> str:
    """Primary application database URL."""
    return os.getenv("DATABASE_URL", build_database_url())


def get_test_database_url() -> str:
    """Database URL used by DB integration tests."""
    test_url = os.getenv("TEST_DATABASE_URL")
    if not test_url:
        raise RuntimeError(
            "TEST_DATABASE_URL must be set for integration tests. "
            "Refusing to fall back to DATABASE_URL."
        )
    return test_url
