"""Run sitemap URL discovery and persist queue candidates."""

from __future__ import annotations

import json
import os
import sys

from app.db.repository import (
    enqueue_discovered_url_candidates,
    get_discovery_counts_by_source_type,
)
from app.db.session import get_session
from app.discovery.sitemap import SourceSitemapConfig, discover_url_candidates


def _source_configs_from_env() -> list[SourceSitemapConfig]:
    return [
        SourceSitemapConfig(
            source="jetformbuilder",
            sitemap_url=os.getenv(
                "JETFORMBUILDER_SITEMAP_URL",
                "https://jetformbuilder.com/sitemap_index.xml",
            ),
        ),
        SourceSitemapConfig(
            source="crocoblock",
            sitemap_url=os.getenv(
                "CROCOBLOCK_SITEMAP_URL",
                "https://crocoblock.com/sitemap_index.xml",
            ),
        ),
    ]


def main() -> int:
    try:
        candidates = discover_url_candidates(configs=_source_configs_from_env())
        with get_session() as session:
            processed_count = enqueue_discovered_url_candidates(session, candidates)
            session.commit()
            counts = get_discovery_counts_by_source_type(session)

        summary = {
            "event": "url_discovery_summary",
            "candidate_count": len(candidates),
            "processed_count": processed_count,
            "counts_by_source_type": [
                {
                    "source": source,
                    "type": doc_type,
                    "count": count,
                }
                for source, doc_type, count in counts
            ],
        }
        print(json.dumps(summary, sort_keys=True))
        return 0
    except Exception as exc:
        print(
            json.dumps(
                {
                    "event": "url_discovery_failed",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                },
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
