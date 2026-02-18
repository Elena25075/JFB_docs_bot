"""Add discovered_urls queue table for sitemap-first discovery.

Revision ID: 20260218_0002
Revises: 20260217_0001
Create Date: 2026-02-18
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260218_0002"
down_revision = "20260217_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "discovered_urls",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column("type", sa.Text(), nullable=False, server_default=sa.text("'unknown'")),
        sa.Column("status", sa.Text(), nullable=False, server_default=sa.text("'pending'")),
        sa.Column(
            "discovered_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "last_seen_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("crawl_attempts", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("last_error", sa.Text(), nullable=True),
    )
    op.create_unique_constraint("uq_discovered_urls_url", "discovered_urls", ["url"])
    op.create_check_constraint(
        "ck_discovered_urls_source_values",
        "discovered_urls",
        "source IN ('jetformbuilder', 'crocoblock')",
    )
    op.create_check_constraint(
        "ck_discovered_urls_type_values",
        "discovered_urls",
        "type IN ('tutorial', 'blog', 'kb', 'docs', 'unknown')",
    )
    op.create_check_constraint(
        "ck_discovered_urls_status_values",
        "discovered_urls",
        "status IN ('pending', 'processing', 'crawled', 'failed')",
    )
    op.create_index(
        "idx_discovered_urls_status_discovered_at",
        "discovered_urls",
        ["status", "discovered_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("idx_discovered_urls_status_discovered_at", table_name="discovered_urls")
    op.drop_constraint("ck_discovered_urls_status_values", "discovered_urls", type_="check")
    op.drop_constraint("ck_discovered_urls_type_values", "discovered_urls", type_="check")
    op.drop_constraint("ck_discovered_urls_source_values", "discovered_urls", type_="check")
    op.drop_constraint("uq_discovered_urls_url", "discovered_urls", type_="unique")
    op.drop_table("discovered_urls")
