from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from app.db.database import Base


class Idea(Base):

    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True)

    # ==========================
    # RELACIONES
    # ==========================

    contact_id = Column(
        Integer,
        ForeignKey("contacts.id"),
        nullable=False,
    )

    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id"),
        nullable=False,
    )

    # ==========================
    # CONTENIDO
    # ==========================

    original_message = Column(
        Text,
        nullable=False,
    )

    summary = Column(
        Text,
        nullable=False,
    )

    category = Column(
        String,
        nullable=False,
    )

    type = Column(
        String,
        nullable=False,
    )

    priority = Column(
        String,
        nullable=False,
        default="MEDIA",
    )
    # BAJA | MEDIA | ALTA

    status = Column(
        String,
        nullable=False,
        default="PENDIENTE",
    )

    # PENDIENTE | EN_REVISION | RESUELTA | DESCARTADA

    ai_confidence = Column(
        Float,
        nullable=True,
    )

    # ==========================
    # FECHAS
    # ==========================

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    # ==========================
    # RELACIONES
    # ==========================

    contact = relationship(
        "Contact",
        back_populates="ideas",
    )

    conversation = relationship(
        "Conversation",
        back_populates="ideas",
    )
