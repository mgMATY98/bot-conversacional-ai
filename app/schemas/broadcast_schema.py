from pydantic import BaseModel, Field


class BroadcastCreateRequest(BaseModel):

    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
    )


class BroadcastRecipientResultRequest(BaseModel):

    recipient_id: int

    success: bool

    error: str | None = None
