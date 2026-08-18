from pydantic import BaseModel
from typing import Optional


class WhatsAppConnectedRequest(BaseModel):

    client_id: int

    phone: str

    push_name: Optional[str] = None


class WhatsAppConnectionResponse(BaseModel):

    id: int

    client_id: int

    session_id: str

    phone: Optional[str]

    push_name: Optional[str]

    status: str

    connected: bool

    class Config:
        from_attributes = True


class WhatsAppQRRequest(BaseModel):

    client_id: int

    qr: str


class WhatsAppDisconnectedRequest(BaseModel):

    client_id: int


from pydantic import BaseModel


class WhatsAppStatusRequest(BaseModel):

    client_id: int

    status: str
