from sqlalchemy import Column, Integer, String, DateTime

from app.db.database import Base


class IPBlock(Base):

    __tablename__ = "ip_blocks"

    id = Column(Integer, primary_key=True)

    ip = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    failed_attempts = Column(
        Integer,
        default=0,
        nullable=False,
    )

    blocked_until = Column(DateTime)

    last_attempt = Column(DateTime)
