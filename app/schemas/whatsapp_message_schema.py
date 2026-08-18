from pydantic import BaseModel


class WhatsAppMessageRequest(BaseModel):
    client_id: int
    phone: str
    push_name: str | None = None
    message: str
