"""Sitemap-first URL discovery utilities for Issue 3."""

from __future__ import annotations

from collections import deque
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import datetime, timezone
from gzip import decompress
from urllib.parse import urlparse, urlunparse
from urllib.request import Request, urlopen
from xml.etree import ElementTree


@dataclass(frozen=True)
class SourceSitemapConfig:
    source: str
    sitemap_url: str


@dataclass(frozen=True)
class DiscoveredUrlCandidate:
    url: str
    source: str
    doc_type: str
    discovered_at: datetime


DEFAULT_SOURCE_SITEMAPS: tuple[SourceSitemapConfig, ...] = (
    SourceSitemapConfig("jetformbuilder", "https://jetformbuilder.com/sitemap_index.xml"),
    SourceSitemapConfig("crocoblock", "https://crocoblock.com/sitemap_index.xml"),
)

ALLOWED_SOURCES = {"jetformbuilder", "crocoblock"}
ALLOWED_DOC_TYPES = {"tutorial", "blog", "kb", "docs", "unknown"}

FetchContent = Callable[[str], bytes]


def _default_fetch_content(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "JFBDocsBot/0.1 (+sitemap-discovery)"})
    with urlopen(request, timeout=20) as response:  # noqa: S310
        return response.read()


def _xml_local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", maxsplit=1)[1]
    return tag


def _parse_sitemap_document(xml_bytes: bytes) -> tuple[str, list[str]]:
    root = ElementTree.fromstring(xml_bytes)
    root_name = _xml_local_name(root.tag)
    locations: list[str] = []

    for elem in root.iter():
        if _xml_local_name(elem.tag) != "loc":
            continue
        if elem.text:
            locations.append(elem.text.strip())

    if root_name in {"sitemapindex", "urlset"}:
        return root_name, locations
    return "unknown", locations


def normalize_url(raw_url: str) -> str | None:
    parsed = urlparse(raw_url.strip())
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        return None

    host = parsed.hostname.lower() if parsed.hostname else ""
    port = f":{parsed.port}" if parsed.port else ""
    netloc = f"{host}{port}"

    path = parsed.path or "/"
    if path != "/":
        path = path.rstrip("/")
        if not path:
            path = "/"

    return urlunparse((parsed.scheme.lower(), netloc, path, "", "", ""))


def infer_source(url: str) -> str | None:
    host = (urlparse(url).hostname or "").lower()
    if host.endswith("jetformbuilder.com"):
        return "jetformbuilder"
    if host.endswith("crocoblock.com"):
        return "crocoblock"
    return None


def infer_doc_type(url: str) -> str:
    lower = url.lower()
    if "/tutorials/" in lower or "/tutorial/" in lower:
        return "tutorial"
    if "/blog/" in lower:
        return "blog"
    if "/kb/" in lower or "/knowledge-base/" in lower:
        return "kb"
    if "/docs/" in lower or "/documentation/" in lower:
        return "docs"
    return "unknown"


def _maybe_decompress(url: str, content: bytes) -> bytes:
    if url.lower().endswith(".gz"):
        return decompress(content)
    return content


def _discover_urls_from_sitemap_tree(
    root_sitemap_url: str,
    fetch_content: FetchContent,
) -> list[str]:
    queue: deque[str] = deque([root_sitemap_url])
    visited_sitemaps: set[str] = set()
    discovered_urls: list[str] = []
    seen_urls: set[str] = set()

    while queue:
        sitemap_url = normalize_url(queue.popleft())
        if not sitemap_url or sitemap_url in visited_sitemaps:
            continue
        visited_sitemaps.add(sitemap_url)

        raw = fetch_content(sitemap_url)
        xml_bytes = _maybe_decompress(sitemap_url, raw)
        doc_type, locs = _parse_sitemap_document(xml_bytes)

        if doc_type == "sitemapindex":
            for loc in locs:
                normalized = normalize_url(loc)
                if normalized:
                    queue.append(normalized)
            continue

        for loc in locs:
            normalized = normalize_url(loc)
            if not normalized or normalized in seen_urls:
                continue
            seen_urls.add(normalized)
            discovered_urls.append(normalized)

    return discovered_urls


def discover_url_candidates(
    configs: Iterable[SourceSitemapConfig] = DEFAULT_SOURCE_SITEMAPS,
    fetch_content: FetchContent = _default_fetch_content,
    now: datetime | None = None,
) -> list[DiscoveredUrlCandidate]:
    discovered_at = now or datetime.now(timezone.utc)
    candidates: list[DiscoveredUrlCandidate] = []
    seen_urls: set[str] = set()

    for config in configs:
        if config.source not in ALLOWED_SOURCES:
            raise ValueError(f"Unsupported source '{config.source}'.")

        urls = _discover_urls_from_sitemap_tree(config.sitemap_url, fetch_content)
        for url in urls:
            if url in seen_urls:
                continue
            source = infer_source(url) or config.source
            doc_type = infer_doc_type(url)
            if source not in ALLOWED_SOURCES:
                continue
            if doc_type not in ALLOWED_DOC_TYPES:
                doc_type = "unknown"
            seen_urls.add(url)
            candidates.append(
                DiscoveredUrlCandidate(
                    url=url,
                    source=source,
                    doc_type=doc_type,
                    discovered_at=discovered_at,
                )
            )

    return candidates
