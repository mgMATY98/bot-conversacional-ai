from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.clients import ClientCreate, ClientUpdate
from app.db.database import get_db
from app.core.auth import (
    get_current_admin,
)
from services.admin.admin_service import admin_service
from pydantic import BaseModel

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/clients")
def list_clients(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return admin_service.list_clients(db)


@router.get("/clients/{client_id}")
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return admin_service.get_client(db, client_id)


@router.post("/clients", status_code=status.HTTP_201_CREATED)
def create_client(
    data: ClientCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return admin_service.create_client(db, data)


@router.put("/clients/{client_id}")
def update_client(
    client_id: int,
    data: ClientUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return admin_service.update_client(db, client_id, data)


@router.delete("/clients/{client_id}")
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return admin_service.delete_client(db, client_id)


# ==========================================================
# CAMBIAR CANAL WHATSAPP
# ==========================================================


class WhatsAppChannelRequest(BaseModel):

    channel: str


@router.post("/clients/{client_id}/whatsapp-channel")
def change_whatsapp_channel(
    client_id: int,
    data: WhatsAppChannelRequest,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):

    return admin_service.change_whatsapp_channel(
        db=db,
        client_id=client_id,
        channel=data.channel,
    )
