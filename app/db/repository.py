"""Repository helpers for DB-backed application workflows."""

from __future__ import annotations

import uuid
from collections.abc import Iterable

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.db.models import DiscoveredUrl, Doc, DocTheme, Theme
from app.discovery.sitemap import DiscoveredUrlCandidate


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


def enqueue_discovered_url_candidates(
    session: Session,
    candidates: Iterable[DiscoveredUrlCandidate],
) -> int:
    rows = [
        {
            "url": candidate.url,
            "source": candidate.source,
            "type": candidate.doc_type,
            "discovered_at": candidate.discovered_at,
            "last_seen_at": candidate.discovered_at,
        }
        for candidate in candidates
    ]
    if not rows:
        return 0

    stmt = insert(DiscoveredUrl).values(rows)
    stmt = stmt.on_conflict_do_update(
        index_elements=[DiscoveredUrl.url],
        set_={
            "source": stmt.excluded.source,
            "type": stmt.excluded.type,
            "last_seen_at": stmt.excluded.last_seen_at,
        },
    )
    session.execute(stmt)
    session.flush()
    return len(rows)


def list_pending_discovered_urls(session: Session, limit: int = 100) -> list[DiscoveredUrl]:
    stmt = (
        select(DiscoveredUrl)
        .where(DiscoveredUrl.status == "pending")
        .order_by(DiscoveredUrl.discovered_at.asc())
        .limit(limit)
    )
    return list(session.scalars(stmt).all())


def get_discovery_counts_by_source_type(session: Session) -> list[tuple[str, str, int]]:
    stmt = (
        select(
            DiscoveredUrl.source,
            DiscoveredUrl.type,
            func.count(DiscoveredUrl.id),
        )
        .group_by(DiscoveredUrl.source, DiscoveredUrl.type)
        .order_by(DiscoveredUrl.source.asc(), DiscoveredUrl.type.asc())
    )
    return [(source, doc_type, count) for source, doc_type, count in session.execute(stmt).all()]
