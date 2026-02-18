"""Sitemap-first discovery package."""

from .sitemap import (
    DEFAULT_SOURCE_SITEMAPS,
    DiscoveredUrlCandidate,
    SourceSitemapConfig,
    discover_url_candidates,
    infer_doc_type,
    infer_source,
    normalize_url,
)

__all__ = [
    "DEFAULT_SOURCE_SITEMAPS",
    "DiscoveredUrlCandidate",
    "SourceSitemapConfig",
    "discover_url_candidates",
    "infer_doc_type",
    "infer_source",
    "normalize_url",
]
