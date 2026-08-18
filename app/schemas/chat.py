from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: str
    message: str
    channel: str = "whatsapp"
    name: str | None = None


class ChatResponse(BaseModel):
    reply: str
