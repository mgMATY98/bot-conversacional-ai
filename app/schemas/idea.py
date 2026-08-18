from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

# ==================================================
# MENSAJE DE CONVERSACIÓN
# ==================================================


class IdeaConversationMessage(BaseModel):

    id: int

    role: str

    message: str

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================================================
# CREAR IDEA
# ==================================================


class IdeaCreate(BaseModel):

    contact_id: int
    conversation_id: int

    original_message: str
    summary: str
    category: str

    priority: str = "MEDIA"

    ai_confidence: Optional[float] = None


# ==================================================
# ACTUALIZAR IDEA
# ==================================================


class IdeaUpdate(BaseModel):

    summary: str

    type: str

    category: str
    priority: str
    status: str


# ==================================================
# RESPUESTA
# ==================================================


class IdeaResponse(BaseModel):

    id: int

    summary: str

    original_message: str

    type: str

    category: str
    priority: str
    status: str

    ai_confidence: float | None

    created_at: datetime

    contact_name: str | None

    contact_phone: str

    # ==============================================
    # CONVERSACIÓN ASOCIADA
    # ==============================================

    conversation: list[IdeaConversationMessage] = []

    model_config = ConfigDict(from_attributes=True)
