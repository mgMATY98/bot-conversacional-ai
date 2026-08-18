from pydantic import BaseModel


class WhatsAppCloudConfigRequest(BaseModel):

    phone_number_id: str
    access_token: str
    waba_id: str | None = None
    verify_token: str | None = None
