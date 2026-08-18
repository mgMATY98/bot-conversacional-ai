from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class WhatsAppConnection(Base):

    __tablename__ = "whatsapp_connections"

    id = Column(Integer, primary_key=True)

    client_id = Column(
        Integer,
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    session_id = Column(
        String,
        nullable=False,
        unique=True,
    )

    phone = Column(String)

    push_name = Column(String)

    status = Column(
        String,
        default="DISCONNECTED",
    )

    connected = Column(
        Boolean,
        default=False,
    )

    last_qr = Column(Text)

    last_error = Column(Text)

    last_seen = Column(DateTime)

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )

    client = relationship(
        "Client",
        back_populates="whatsapp_connection",
    )
