from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.db.models import DocTheme
from app.db.repository import create_doc, create_theme, get_doc_by_url, link_doc_theme


def test_insert_select_round_trip(db_session: Session) -> None:
    doc = create_doc(
        db_session,
        url="https://jetformbuilder.com/tutorials/example",
        source="jetformbuilder",
        doc_type="tutorial",
        title="Example Tutorial",
    )
    create_theme(db_session, "file upload", "Covers upload-related workflows")
    link_doc_theme(db_session, doc.id, "file upload")
    db_session.commit()

    verify_session_factory = sessionmaker(
        bind=db_session.get_bind(),
        autocommit=False,
        autoflush=False,
        class_=Session,
    )

    with verify_session_factory() as verify_session:
        loaded = get_doc_by_url(verify_session, "https://jetformbuilder.com/tutorials/example")
        assert loaded is not None
        assert loaded.url == "https://jetformbuilder.com/tutorials/example"
        assert loaded.source == "jetformbuilder"
        assert loaded.type == "tutorial"

        link_rows = verify_session.scalars(select(DocTheme)).all()
        assert len(link_rows) == 1
        assert link_rows[0].theme == "file upload"
