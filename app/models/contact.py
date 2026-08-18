from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class Contact(Base):

    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)

    # ==========================
    # RELACIÓN CON EL CLIENTE
    # ==========================

    client_id = Column(
        Integer,
        ForeignKey("clients.id"),
        nullable=False,
    )

    # ==========================
    # DATOS DEL CONTACTO
    # ==========================

    user_id = Column(
        String,
        nullable=False,
        index=True,
    )

    channel = Column(
        String,
        nullable=False,
    )

    name = Column(String)

    # ==========================
    # FECHAS
    # ==========================

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )
    # ==========================================================
    # BOLETINES
    # ==========================================================

    broadcast_enabled = Column(
        Boolean,
        nullable=False,
        default=True,
    )
    # ==========================
    # RELACIONES
    # ==========================

    client = relationship(
        "Client",
        back_populates="contacts",
    )

    conversations = relationship(
        "Conversation",
        back_populates="contact",
        cascade="all, delete-orphan",
    )

    ideas = relationship(
        "Idea",
        back_populates="contact",
        cascade="all, delete-orphan",
    )

    pending_document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=True,
    )

    pending_document = relationship(
        "Document",
        foreign_keys=[pending_document_id],
    )

    conversation_state = Column(
        String,
        nullable=False,
        default="NORMAL",
    )

    conversation_context = Column(
        Text,
        nullable=True,
    )

    conversation_updated_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    broadcast_recipients = relationship(
        "BroadcastRecipient",
        back_populates="contact",
    )
