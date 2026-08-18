from typing import Optional

from pydantic import BaseModel


class BotConfigUpdate(BaseModel):

    assistant_name: Optional[str] = None

    personality: Optional[str] = None

    objective: Optional[str] = None

    additional_instructions: Optional[str] = None

    welcome_message: Optional[str] = None

    farewell_message: Optional[str] = None

    forbidden_topics: Optional[str] = None

    forbidden_words: Optional[str] = None

    political_campaigns: Optional[bool] = None


class BotConfigResponse(BaseModel):

    assistant_name: str

    personality: str

    objective: str

    additional_instructions: str

    welcome_message: str

    farewell_message: str

    forbidden_topics: str

    forbidden_words: str

    political_campaigns: bool

    class Config:
        from_attributes = True
