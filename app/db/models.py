"""SQLAlchemy models for Issue 2 baseline schema."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    PrimaryKeyConstraint,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Doc(Base):
    __tablename__ = "docs"
    __table_args__ = (
        UniqueConstraint("url", name="uq_docs_url"),
        Index("idx_docs_source", "source"),
        Index("idx_docs_type", "type"),
        Index("idx_docs_published_at", text("published_at DESC")),
        CheckConstraint(
            "source IN ('jetformbuilder', 'crocoblock')",
            name="ck_docs_source_values",
        ),
        CheckConstraint(
            "type IN ('tutorial', 'blog', 'kb', 'docs', 'unknown')",
            name="ck_docs_type_values",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    url: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    tags: Mapped[list[str]] = mapped_column(
        ARRAY(Text),
        nullable=False,
        server_default=text("'{}'::text[]"),
    )
    categories: Mapped[list[str]] = mapped_column(
        ARRAY(Text),
        nullable=False,
        server_default=text("'{}'::text[]"),
    )
    short_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    headings: Mapped[list[str]] = mapped_column(
        ARRAY(Text),
        nullable=False,
        server_default=text("'{}'::text[]"),
    )
    content_hash: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_crawled_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    http_status: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    language: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'en'"))

    doc_themes: Mapped[list["DocTheme"]] = relationship(
        back_populates="doc",
        cascade="all, delete-orphan",
    )


class Theme(Base):
    __tablename__ = "themes"

    theme: Mapped[str] = mapped_column(Text, primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    doc_themes: Mapped[list["DocTheme"]] = relationship(
        back_populates="theme_rel",
        cascade="all, delete-orphan",
    )


class DocTheme(Base):
    __tablename__ = "doc_themes"
    __table_args__ = (
        Index("idx_doc_themes_theme", "theme"),
        PrimaryKeyConstraint("doc_id", "theme", name="pk_doc_themes"),
    )

    doc_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("docs.id", ondelete="CASCADE"),
        nullable=False,
    )
    theme: Mapped[str] = mapped_column(
        Text,
        ForeignKey("themes.theme", ondelete="CASCADE"),
        nullable=False,
    )

    doc: Mapped[Doc] = relationship(back_populates="doc_themes")
    theme_rel: Mapped[Theme] = relationship(back_populates="doc_themes")
