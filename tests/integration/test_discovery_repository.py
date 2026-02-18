from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import DiscoveredUrl
from app.db.repository import (
    enqueue_discovered_url_candidates,
    get_discovery_counts_by_source_type,
    list_pending_discovered_urls,
)
from app.discovery.sitemap import DiscoveredUrlCandidate


def test_discovery_enqueue_is_idempotent_and_counts_are_reported(db_session: Session) -> None:
    now = datetime.now(timezone.utc)
    batch_1 = [
        DiscoveredUrlCandidate(
            url="https://jetformbuilder.com/tutorials/start",
            source="jetformbuilder",
            doc_type="tutorial",
            discovered_at=now,
        ),
        DiscoveredUrlCandidate(
            url="https://crocoblock.com/blog/entry",
            source="crocoblock",
            doc_type="blog",
            discovered_at=now + timedelta(seconds=1),
        ),
    ]
    processed_1 = enqueue_discovered_url_candidates(db_session, batch_1)
    db_session.commit()

    batch_2 = [
        DiscoveredUrlCandidate(
            url="https://jetformbuilder.com/tutorials/start",
            source="jetformbuilder",
            doc_type="docs",
            discovered_at=now + timedelta(seconds=2),
        )
    ]
    processed_2 = enqueue_discovered_url_candidates(db_session, batch_2)
    db_session.commit()

    rows = db_session.scalars(select(DiscoveredUrl).order_by(DiscoveredUrl.url.asc())).all()
    assert processed_1 == 2
    assert processed_2 == 1
    assert len(rows) == 2

    updated = next(row for row in rows if row.url == "https://jetformbuilder.com/tutorials/start")
    assert updated.type == "docs"
    assert updated.status == "pending"
    assert updated.crawl_attempts == 0

    pending_rows = list_pending_discovered_urls(db_session, limit=10)
    assert len(pending_rows) == 2
    assert all(row.status == "pending" for row in pending_rows)

    counts = get_discovery_counts_by_source_type(db_session)
    assert counts == [
        ("crocoblock", "blog", 1),
        ("jetformbuilder", "docs", 1),
    ]
