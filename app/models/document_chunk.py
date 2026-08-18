from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Text,
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class DocumentChunk(Base):

    __tablename__ = "document_chunks"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False,
    )

    chunk_index = Column(
        Integer,
        nullable=False,
    )

    text = Column(
        Text,
        nullable=False,
    )

    word_count = Column(
        Integer,
        default=0,
    )

    keywords = Column(
        Text,
    )

    document = relationship(
        "Document",
        back_populates="chunks",
    )
