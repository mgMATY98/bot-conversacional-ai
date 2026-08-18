from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_client
from app.db.database import get_db

from services import whatsapp_connection_service
from services import whatsapp_connection_service
from services.whatsapp_dashboard.dashboard_service import (
    whatsapp_dashboard_service,
)
from app.schemas.whatsapp_connection_schema import (
    WhatsAppDisconnectedRequest,
)

router = APIRouter(prefix="/whatsapp", tags=["WhatsApp Dashboard"])


# ==========================================================
# STATUS
# ==========================================================


@router.get("/status")
def status(
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    return whatsapp_dashboard_service.get_status(
        db,
        current_client.id,
    )


# ==========================================================
# QR
# ==========================================================


@router.get("/qr")
def qr(
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    return whatsapp_dashboard_service.get_qr(
        db,
        current_client.id,
    )


# ==========================================================
# RECONNECT
# ==========================================================


@router.post("/reconnect")
def reconnect(
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    return whatsapp_dashboard_service.reconnect(
        db,
        current_client.id,
    )


# ==========================================================
# DISCONNECT
# ==========================================================


@router.post("/disconnect")
def disconnect(
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    return whatsapp_dashboard_service.disconnect(
        db,
        current_client.id,
    )


@router.post("/disconnected")
def whatsapp_disconnected(
    data: WhatsAppDisconnectedRequest,
    db: Session = Depends(get_db),
):

    whatsapp_connection_service.disconnect(
        db=db,
        client_id=data.client_id,
    )

    return {
        "success": True,
    }
