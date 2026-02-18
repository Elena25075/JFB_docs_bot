from __future__ import annotations

from datetime import datetime, timezone

from app.discovery.sitemap import (
    SourceSitemapConfig,
    discover_url_candidates,
    infer_doc_type,
    infer_source,
    normalize_url,
)


def test_discover_url_candidates_parses_nested_sitemaps_and_deduplicates() -> None:
    index_xml = (
        b'<?xml version="1.0"?>'
        b'<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        b"<sitemap><loc>https://jetformbuilder.com/post-sitemap.xml</loc></sitemap>"
        b"</sitemapindex>"
    )
    urlset_xml = (
        b'<?xml version="1.0"?>'
        b'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        b"<url><loc>https://jetformbuilder.com/tutorials/example/?utm_source=test</loc></url>"
        b"<url><loc>https://jetformbuilder.com/tutorials/example/</loc></url>"
        b"<url><loc>https://jetformbuilder.com/blog/example/#heading</loc></url>"
        b"</urlset>"
    )
    payloads = {
        "https://jetformbuilder.com/sitemap_index.xml": index_xml,
        "https://jetformbuilder.com/post-sitemap.xml": urlset_xml,
    }

    def fetch(url: str) -> bytes:
        return payloads[url]

    now = datetime(2026, 2, 18, 0, 0, tzinfo=timezone.utc)
    candidates = discover_url_candidates(
        configs=[
            SourceSitemapConfig(
                source="jetformbuilder",
                sitemap_url="https://jetformbuilder.com/sitemap_index.xml",
            )
        ],
        fetch_content=fetch,
        now=now,
    )

    assert [candidate.url for candidate in candidates] == [
        "https://jetformbuilder.com/tutorials/example",
        "https://jetformbuilder.com/blog/example",
    ]
    assert [candidate.doc_type for candidate in candidates] == ["tutorial", "blog"]
    assert all(candidate.source == "jetformbuilder" for candidate in candidates)
    assert all(candidate.discovered_at == now for candidate in candidates)


def test_discover_url_candidates_collects_rows_per_configured_source() -> None:
    jet_xml = (
        b'<?xml version="1.0"?>'
        b'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        b"<url><loc>https://jetformbuilder.com/tutorials/one</loc></url>"
        b"</urlset>"
    )
    croco_xml = (
        b'<?xml version="1.0"?>'
        b'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        b"<url><loc>https://crocoblock.com/blog/two</loc></url>"
        b"</urlset>"
    )
    payloads = {
        "https://jetformbuilder.com/sitemap_index.xml": jet_xml,
        "https://crocoblock.com/sitemap_index.xml": croco_xml,
    }

    def fetch(url: str) -> bytes:
        return payloads[url]

    candidates = discover_url_candidates(
        configs=[
            SourceSitemapConfig("jetformbuilder", "https://jetformbuilder.com/sitemap_index.xml"),
            SourceSitemapConfig("crocoblock", "https://crocoblock.com/sitemap_index.xml"),
        ],
        fetch_content=fetch,
        now=datetime(2026, 2, 18, 0, 0, tzinfo=timezone.utc),
    )

    assert {(candidate.source, candidate.doc_type) for candidate in candidates} == {
        ("jetformbuilder", "tutorial"),
        ("crocoblock", "blog"),
    }


def test_normalize_url_handles_common_discovery_cases() -> None:
    assert normalize_url("https://example.com/tutorials/demo/?x=1#top") == "https://example.com/tutorials/demo"
    assert normalize_url("https://example.com/") == "https://example.com/"
    assert normalize_url("mailto:ops@example.com") is None
    assert normalize_url("not-a-url") is None


def test_infer_doc_type_patterns_and_unknown_fallback() -> None:
    assert infer_doc_type("https://jetformbuilder.com/tutorials/form-example") == "tutorial"
    assert infer_doc_type("https://crocoblock.com/blog/post-example") == "blog"
    assert infer_doc_type("https://site.test/knowledge-base/item") == "kb"
    assert infer_doc_type("https://site.test/docs/setup") == "docs"
    assert infer_doc_type("https://site.test/features/new-item") == "unknown"


def test_infer_source_from_domain() -> None:
    assert infer_source("https://jetformbuilder.com/tutorials/example") == "jetformbuilder"
    assert infer_source("https://crocoblock.com/blog/example") == "crocoblock"
    assert infer_source("https://example.com/article") is None
