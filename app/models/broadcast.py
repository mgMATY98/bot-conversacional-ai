from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    func,
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class Broadcast(Base):

    __tablename__ = "broadcasts"

    # ==========================================================
    # ID
    # ==========================================================

    id = Column(
        Integer,
        primary_key=True,
    )

    # ==========================================================
    # CLIENTE
    # ==========================================================

    client_id = Column(
        Integer,
        ForeignKey("clients.id"),
        nullable=False,
        index=True,
    )

    # ==========================================================
    # MENSAJE
    # ==========================================================

    message = Column(
        Text,
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
    # PAUSED
    # COMPLETED
    # CANCELLED
    # FAILED

    # ==========================================================
    # ESTADÍSTICAS
    # ==========================================================

    total_recipients = Column(
        Integer,
        nullable=False,
        default=0,
    )

    sent_count = Column(
        Integer,
        nullable=False,
        default=0,
    )

    failed_count = Column(
        Integer,
        nullable=False,
        default=0,
    )

    # ==========================================================
    # FECHAS
    # ==========================================================

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )

    started_at = Column(
        DateTime,
        nullable=True,
    )

    finished_at = Column(
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

    client = relationship(
        "Client",
        back_populates="broadcasts",
    )

    recipients = relationship(
        "BroadcastRecipient",
        back_populates="broadcast",
        cascade="all, delete-orphan",
    )
