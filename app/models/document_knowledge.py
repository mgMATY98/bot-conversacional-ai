from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Text,
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class DocumentKnowledge(Base):

    __tablename__ = "document_knowledge"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False,
        unique=True,
    )

    # ==========================================
    # ANÁLISIS IA
    # ==========================================

    summary = Column(Text)

    category = Column(Text)

    topics = Column(Text)

    keywords = Column(Text)

    synonyms = Column(Text)

    questions = Column(Text)

    language = Column(Text)

    pages = Column(Integer)

    words = Column(Integer)

    chunks = Column(Integer)

    # ==========================================
    # RELACIÓN
    # ==========================================

    document = relationship(
        "Document",
        back_populates="knowledge",
    )
