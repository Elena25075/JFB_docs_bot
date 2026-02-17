"""Initial schema for docs, themes, and doc_themes.

Revision ID: 20260217_0001
Revises:
Create Date: 2026-02-17
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260217_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    op.create_table(
        "docs",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column("type", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "tags",
            postgresql.ARRAY(sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::text[]"),
        ),
        sa.Column(
            "categories",
            postgresql.ARRAY(sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::text[]"),
        ),
        sa.Column("short_description", sa.Text(), nullable=True),
        sa.Column("content_text", sa.Text(), nullable=True),
        sa.Column(
            "headings",
            postgresql.ARRAY(sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::text[]"),
        ),
        sa.Column("content_hash", sa.Text(), nullable=True),
        sa.Column("last_crawled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("http_status", sa.Integer(), nullable=True),
        sa.Column("language", sa.Text(), nullable=False, server_default=sa.text("'en'")),
    )

    op.create_unique_constraint("uq_docs_url", "docs", ["url"])
    op.create_check_constraint(
        "ck_docs_source_values",
        "docs",
        "source IN ('jetformbuilder', 'crocoblock')",
    )
    op.create_check_constraint(
        "ck_docs_type_values",
        "docs",
        "type IN ('tutorial', 'blog', 'kb', 'docs', 'unknown')",
    )
    op.create_index("idx_docs_source", "docs", ["source"], unique=False)
    op.create_index("idx_docs_type", "docs", ["type"], unique=False)
    op.create_index(
        "idx_docs_published_at",
        "docs",
        [sa.text("published_at DESC")],
        unique=False,
    )

    op.create_table(
        "themes",
        sa.Column("theme", sa.Text(), nullable=False, primary_key=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    op.create_table(
        "doc_themes",
        sa.Column("doc_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("theme", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["doc_id"], ["docs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["theme"], ["themes.theme"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("doc_id", "theme", name="pk_doc_themes"),
    )
    op.create_index("idx_doc_themes_theme", "doc_themes", ["theme"], unique=False)


def downgrade() -> None:
    op.drop_index("idx_doc_themes_theme", table_name="doc_themes")
    op.drop_table("doc_themes")

    op.drop_table("themes")

    op.drop_index("idx_docs_published_at", table_name="docs")
    op.drop_index("idx_docs_type", table_name="docs")
    op.drop_index("idx_docs_source", table_name="docs")
    op.drop_constraint("ck_docs_type_values", "docs", type_="check")
    op.drop_constraint("ck_docs_source_values", "docs", type_="check")
    op.drop_constraint("uq_docs_url", "docs", type_="unique")
    op.drop_table("docs")
