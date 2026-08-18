from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class BotLog(Base):

    __tablename__ = "bot_logs"

    id = Column(Integer, primary_key=True)

    # ==========================
    # RELACIONES
    # ==========================

    client_id = Column(
        Integer,
        ForeignKey("clients.id"),
        nullable=False,
        index=True,
    )

    contact_id = Column(
        Integer,
        ForeignKey("contacts.id"),
        nullable=True,
        index=True,
    )

    # ==========================
    # EVENTO
    # ==========================

    event = Column(
        String,
        nullable=False,
    )

    details = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # ==========================
    # RELACIONES SQLALCHEMY
    # ==========================

    client = relationship(
        "Client",
        back_populates="bot_logs",
    )

    contact = relationship("Contact")
