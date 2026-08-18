from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Text,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class WhatsAppCloudConnection(Base):

    __tablename__ = "whatsapp_cloud_connections"

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
        unique=True,
    )

    # ==========================================================
    # META / WHATSAPP CLOUD API
    # ==========================================================

    phone_number_id = Column(
        String,
        nullable=False,
    )

    access_token = Column(
        Text,
        nullable=False,
    )

    waba_id = Column(
        String,
        nullable=True,
    )

    verify_token = Column(
        String,
        nullable=True,
    )

    # ==========================================================
    # ESTADO
    # ==========================================================

    active = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ==========================================================
    # FECHAS
    # ==========================================================

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
    # RELACIÓN
    # ==========================================================

    client = relationship(
        "Client",
        back_populates="whatsapp_cloud_connection",
    )
