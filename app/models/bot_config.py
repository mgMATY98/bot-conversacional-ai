from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class BotConfig(Base):

    __tablename__ = "bot_configs"

    id = Column(Integer, primary_key=True)

    # ==========================
    # RELACIÓN
    # ==========================

    client_id = Column(
        Integer,
        ForeignKey("clients.id"),
        unique=True,
        nullable=False,
    )

    # ==========================
    # IDENTIDAD DEL BOT
    # ==========================

    assistant_name = Column(String, nullable=False)

    # ==========================
    # PERSONALIDAD
    # ==========================

    personality = Column(Text)

    objective = Column(Text)

    additional_instructions = Column(Text)

    # ==========================
    # MENSAJES
    # ==========================

    welcome_message = Column(Text)

    farewell_message = Column(Text)

    # ==========================
    # MODERACIÓN
    # ==========================

    forbidden_topics = Column(Text)

    forbidden_words = Column(Text)

    # ==========================
    # CONFIGURACIÓN
    # ==========================

    political_campaigns = Column(Text)

    # ==========================
    # RELACIONES
    # ==========================

    client = relationship(
        "Client",
        back_populates="bot_config",
    )
