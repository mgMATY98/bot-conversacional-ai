from datetime import datetime

from pydantic import BaseModel, ConfigDict

# ==========================================================
# DOCUMENT RESPONSE
# ==========================================================


class DocumentResponse(BaseModel):

    id: int

    client_id: int

    title: str

    original_filename: str

    mime_type: str

    size: int

    summary: str | None = None

    status: str

    created_at: datetime

    download_url: str | None = None

    model_config = ConfigDict(from_attributes=True)
