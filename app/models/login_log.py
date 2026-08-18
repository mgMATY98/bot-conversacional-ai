from sqlalchemy import Column, Integer, String, DateTime, func

from app.db.database import Base


class LoginLog(Base):

    __tablename__ = "login_logs"

    id = Column(Integer, primary_key=True)

    # ==========================
    # DATOS DEL LOGIN
    # ==========================

    username = Column(
        String,
        nullable=False,
        index=True,
    )

    ip = Column(
        String,
        nullable=False,
        index=True,
    )

    user_agent = Column(String)

    login_type = Column(
        String,
        nullable=False,
    )
    # ADMIN | CLIENT

    status = Column(
        String,
        nullable=False,
    )
    # SUCCESS | FAILED

    reason = Column(String)

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )
