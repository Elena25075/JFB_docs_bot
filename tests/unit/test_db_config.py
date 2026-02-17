from __future__ import annotations

from sqlalchemy.engine import make_url

from app.db.config import build_database_url


def test_build_database_url_wraps_bare_ipv6_host(monkeypatch) -> None:
    monkeypatch.setenv("POSTGRES_USER", "jfb_user")
    monkeypatch.setenv("POSTGRES_PASSWORD", "jfb_password")
    monkeypatch.setenv("POSTGRES_HOST", "::1")
    monkeypatch.setenv("POSTGRES_PORT", "5432")
    monkeypatch.setenv("POSTGRES_DB", "jfb_docs")

    url = build_database_url()
    parsed = make_url(url)

    assert "@[::1]:5432/" in url
    assert parsed.host == "::1"


def test_build_database_url_keeps_bracketed_ipv6_host(monkeypatch) -> None:
    monkeypatch.setenv("POSTGRES_HOST", "[::1]")

    url = build_database_url()
    parsed = make_url(url)

    assert "@[::1]:5432/" in url
    assert parsed.host == "::1"


def test_build_database_url_keeps_ipv4_host(monkeypatch) -> None:
    monkeypatch.setenv("POSTGRES_HOST", "127.0.0.1")

    url = build_database_url()
    parsed = make_url(url)

    assert "@127.0.0.1:5432/" in url
    assert parsed.host == "127.0.0.1"
