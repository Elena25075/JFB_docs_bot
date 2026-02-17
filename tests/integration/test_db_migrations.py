from __future__ import annotations

from sqlalchemy import create_engine, inspect


def test_migrate_up_creates_required_schema(migrated_database: str) -> None:
    engine = create_engine(migrated_database, pool_pre_ping=True)
    inspector = inspect(engine)

    table_names = set(inspector.get_table_names())
    assert {"docs", "themes", "doc_themes"} <= table_names

    unique_constraints = inspector.get_unique_constraints("docs")
    assert any(
        constraint["name"] == "uq_docs_url" and "url" in constraint["column_names"]
        for constraint in unique_constraints
    )

    check_constraints = {
        constraint["name"]
        for constraint in inspector.get_check_constraints("docs")
    }
    assert "ck_docs_source_values" in check_constraints
    assert "ck_docs_type_values" in check_constraints

    index_names = {index["name"] for index in inspector.get_indexes("docs")}
    assert "idx_docs_source" in index_names
    assert "idx_docs_type" in index_names
    assert "idx_docs_published_at" in index_names

    doc_themes_index_names = {index["name"] for index in inspector.get_indexes("doc_themes")}
    assert "idx_doc_themes_theme" in doc_themes_index_names

    engine.dispose()
