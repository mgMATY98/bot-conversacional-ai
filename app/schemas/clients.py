from typing import Optional

from pydantic import BaseModel


class ClientCreate(BaseModel):
    username: str
    password: str

    organization_name: str
    representative_name: str
    representative_role: str

    municipality: str
    province: str

    bot_phone: str


class ClientUpdate(BaseModel):
    organization_name: Optional[str] = None
    representative_name: Optional[str] = None
    representative_role: Optional[str] = None

    municipality: Optional[str] = None
    province: Optional[str] = None

    bot_phone: Optional[str] = None

    active: Optional[bool] = None


class ClientResponse(BaseModel):
    id: int

    username: str
    active: bool

    organization_name: str
    representative_name: str
    representative_role: str

    municipality: str
    province: str

    bot_phone: str

    class Config:
        from_attributes = True
