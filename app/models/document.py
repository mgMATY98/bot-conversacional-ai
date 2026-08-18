from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Document(Base):

    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    client_id = Column(
        Integer,
        ForeignKey("clients.id"),
        nullable=False,
        index=True,
    )

    title = Column(
        String,
        nullable=False,
    )

    original_filename = Column(
        String,
        nullable=False,
    )

    stored_filename = Column(
        String,
        nullable=False,
    )

    mime_type = Column(
        String,
        nullable=False,
    )

    size = Column(
        Integer,
        nullable=False,
    )

    # Texto extraído del PDF o TXT
    extracted_text = Column(
        Text,
        nullable=False,
    )

    status = Column(
        String,
        default="uploaded",
        nullable=False,
    )
    knowledge = relationship(
        "DocumentKnowledge",
        back_populates="document",
        uselist=False,
        cascade="all, delete-orphan",
    )
    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan",
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    summary = Column(Text, nullable=True)
