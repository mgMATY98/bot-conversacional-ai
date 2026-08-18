from datetime import datetime

from pydantic import BaseModel


class ContactResponse(BaseModel):

    id: int

    user_id: str

    channel: str

    name: str | None = None

    class Config:
        from_attributes = True

    last_message: str | None = None

    last_message_at: datetime | None = None

    messages_count: int = 0

    last_role: str | None = None
