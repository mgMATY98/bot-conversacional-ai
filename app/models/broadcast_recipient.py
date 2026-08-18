from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    func,
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class BroadcastRecipient(Base):

    __tablename__ = "broadcast_recipients"

    # ==========================================================
    # ID
    # ==========================================================

    id = Column(
        Integer,
        primary_key=True,
    )

    # ==========================================================
    # BOLETÍN
    # ==========================================================

    broadcast_id = Column(
        Integer,
        ForeignKey("broadcasts.id"),
        nullable=False,
        index=True,
    )

    # ==========================================================
    # CONTACTO
    # ==========================================================

    contact_id = Column(
        Integer,
        ForeignKey("contacts.id"),
        nullable=False,
        index=True,
    )

    # ==========================================================
    # TELÉFONO
    # ==========================================================

    phone = Column(
        String,
        nullable=False,
    )

    # ==========================================================
    # ESTADO
    # ==========================================================

    status = Column(
        String,
        nullable=False,
        default="PENDING",
        index=True,
    )

    # PENDING
    # SENDING
    # SENT
    # FAILED

    # ==========================================================
    # ERROR
    # ==========================================================

    error = Column(
        String,
        nullable=True,
    )

    # ==========================================================
    # FECHAS
    # ==========================================================

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )

    sent_at = Column(
        DateTime,
        nullable=True,
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # ==========================================================
    # RELACIONES
    # ==========================================================

    broadcast = relationship(
        "Broadcast",
        back_populates="recipients",
    )

    contact = relationship(
        "Contact",
    )
