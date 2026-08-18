from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ConversationSummaryResponse(BaseModel):

    contact_id: int

    contact_name: str

    user_id: str

    last_message: str

    last_message_at: datetime

    message_count: int

    model_config = ConfigDict(from_attributes=True)


class ConversationMessageResponse(BaseModel):

    id: int

    role: str

    text: str

    sources: list[str]

    attachments: list

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
