"""Database package for connection config and access primitives."""

from .config import get_database_url, get_test_database_url
from .repository import (
    create_doc,
    create_theme,
    enqueue_discovered_url_candidates,
    get_discovery_counts_by_source_type,
    get_doc_by_url,
    link_doc_theme,
    list_pending_discovered_urls,
)

__all__ = [
    "create_doc",
    "create_theme",
    "enqueue_discovered_url_candidates",
    "get_database_url",
    "get_discovery_counts_by_source_type",
    "get_doc_by_url",
    "get_test_database_url",
    "link_doc_theme",
    "list_pending_discovered_urls",
]
