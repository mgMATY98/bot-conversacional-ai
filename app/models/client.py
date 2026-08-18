from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.database import Base


class Client(Base):

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)

    # ==========================
    # ACCESO
    # ==========================

    username = Column(String, unique=True, nullable=False)

    password_hash = Column(String, nullable=False)

    active = Column(Boolean, default=True)

    # ==========================
    # DATOS DEL CLIENTE
    # ==========================

    organization_name = Column(String, nullable=False)

    representative_name = Column(String, nullable=False)

    representative_role = Column(String, nullable=False)

    municipality = Column(String)

    province = Column(String)

    bot_phone = Column(String, nullable=False)
    # ==========================
    # CANAL WHATSAPP ACTIVO
    # ==========================

    active_channel = Column(
        String,
        nullable=False,
        default="whatsapp_web",
        server_default="whatsapp_web",
    )

    # ==========================
    # RELACIONES
    # ==========================

    bot_config = relationship(
        "BotConfig",
        back_populates="client",
        uselist=False,
        cascade="all, delete-orphan",
    )

    contacts = relationship(
        "Contact",
        back_populates="client",
        cascade="all, delete-orphan",
    )

    audit_logs = relationship(
        "AuditLog",
        back_populates="client",
        cascade="all, delete-orphan",
    )

    bot_logs = relationship(
        "BotLog",
        back_populates="client",
        cascade="all, delete-orphan",
    )
    whatsapp_connection = relationship(
        "WhatsAppConnection",
        back_populates="client",
        uselist=False,
        cascade="all, delete-orphan",
    )
    whatsapp_cloud_connection = relationship(
        "WhatsAppCloudConnection",
        back_populates="client",
        uselist=False,
        cascade="all, delete-orphan",
    )
    broadcasts = relationship(
        "Broadcast",
        back_populates="client",
        cascade="all, delete-orphan",
    )
