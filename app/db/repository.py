"""Minimal repository helpers for Issue 2 integration tests."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Doc, DocTheme, Theme


def create_doc(
    session: Session,
    *,
    url: str,
    source: str,
    doc_type: str,
    title: str,
) -> Doc:
    doc = Doc(
        url=url,
        source=source,
        type=doc_type,
        title=title,
    )
    session.add(doc)
    session.flush()
    return doc


def get_doc_by_url(session: Session, url: str) -> Doc | None:
    stmt = select(Doc).where(Doc.url == url)
    return session.scalar(stmt)


def create_theme(session: Session, theme: str, description: str | None = None) -> Theme:
    theme_row = Theme(theme=theme, description=description)
    session.add(theme_row)
    session.flush()
    return theme_row


def link_doc_theme(session: Session, doc_id: uuid.UUID, theme: str) -> DocTheme:
    link = DocTheme(doc_id=doc_id, theme=theme)
    session.add(link)
    session.flush()
    return link
