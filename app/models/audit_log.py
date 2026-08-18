from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.database import Base


class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)

    # ==========================
    # RELACIÓN
    # ==========================

    client_id = Column(
        Integer,
        ForeignKey("clients.id"),
        nullable=True,
        index=True,
    )

    # ==========================
    # DATOS
    # ==========================

    username = Column(String, index=True)

    ip = Column(String)

    action = Column(String, nullable=False)

    status = Column(String)

    details = Column(String)

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )

    # ==========================
    # RELACIONES
    # ==========================

    client = relationship(
        "Client",
        back_populates="audit_logs",
    )
