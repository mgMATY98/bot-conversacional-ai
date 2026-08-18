from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy import JSON
from app.db.database import Base


class Conversation(Base):

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    # ==========================
    # RELACIÓN
    # ==========================

    contact_id = Column(
        Integer,
        ForeignKey("contacts.id"),
        nullable=False,
    )

    # ==========================
    # MENSAJES
    # ==========================

    role = Column(
        String,
        nullable=False,
    )
    # user | assistant | system

    message = Column(
        Text,
        nullable=False,
    )

    sources = Column(JSON, nullable=True)

    attachments = Column(JSON, nullable=True)

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )

    # ==========================
    # RELACIONES
    # ==========================

    contact = relationship(
        "Contact",
        back_populates="conversations",
    )

    ideas = relationship(
        "Idea",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )
