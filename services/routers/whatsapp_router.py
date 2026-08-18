from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.whatsapp_connection_schema import (
    WhatsAppConnectedRequest,
    WhatsAppDisconnectedRequest,
    WhatsAppQRRequest,
    WhatsAppStatusRequest,
)
from app.schemas.whatsapp_message_schema import (
    WhatsAppMessageRequest,
)

from services.chat.chat_service import (
    chat_service,
)
from app.schemas.whatsapp_connection_schema import (
    WhatsAppConnectedRequest,
    WhatsAppQRRequest,
)
from services.whatsapp_connection_service import (
    whatsapp_connection_service,
)

router = APIRouter(
    prefix="/wsp",
    tags=["WhatsApp"],
)

from app.models.client import Client


@router.post("/connected")
def whatsapp_connected(
    data: WhatsAppConnectedRequest,
    db: Session = Depends(get_db),
):

    try:

        connection = whatsapp_connection_service.upsert_connection(
            db=db,
            client_id=data.client_id,
            phone=data.phone,
            push_name=data.push_name,
        )

        return {
            "success": True,
            "connection_id": connection.id,
            "status": connection.status,
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


import traceback


@router.post("/qr")
def whatsapp_qr(
    data: WhatsAppQRRequest,
    db: Session = Depends(get_db),
):

    whatsapp_connection_service.update_qr(
        db=db,
        client_id=data.client_id,
        qr=data.qr,
    )

    return {
        "success": True,
    }


@router.post("/status")
def whatsapp_status(
    data: WhatsAppStatusRequest,
    db: Session = Depends(get_db),
):

    connection = whatsapp_connection_service.update_status(
        db=db,
        client_id=data.client_id,
        status=data.status,
    )

    if connection is None:

        raise HTTPException(
            status_code=404,
            detail="Conexión no encontrada.",
        )

    return {
        "success": True,
        "status": connection.status,
    }


@router.post("/message")
def receive_message(
    data: WhatsAppMessageRequest,
    db: Session = Depends(get_db),
):

    try:

        # ======================================================
        # BUSCAR CLIENTE
        # ======================================================

        client = db.query(Client).filter(Client.id == data.client_id).first()

        if not client:

            raise HTTPException(
                status_code=404,
                detail="Cliente no encontrado.",
            )

        # ======================================================
        # VERIFICAR CANAL ACTIVO
        # ======================================================

        if client.active_channel != "whatsapp_web":

            print("ℹ️ WhatsApp Web recibió un mensaje " "pero no es el canal activo.")

            print(
                "Cliente:",
                client.id,
            )

            print(
                "Canal activo:",
                client.active_channel,
            )

            return {
                "success": True,
                "ignored": True,
                "reason": "inactive_channel",
                "reply": None,
                "attachments": [],
            }

        # ======================================================
        # PROCESAR MENSAJE
        # ======================================================

        result = chat_service.process_message(
            db=db,
            client_id=data.client_id,
            user_id=data.phone,
            channel="whatsapp",
            message=data.message,
            name=data.push_name,
        )

        # ======================================================
        # ATTACHMENTS
        # ======================================================

        attachments = result.get("attachments")

        if attachments is None:

            attachments = []

        elif isinstance(
            attachments,
            dict,
        ):

            attachments = [attachments]

        # ======================================================
        # RESPUESTA
        # ======================================================

        return {
            "success": True,
            "ignored": False,
            "reply": result["reply"],
            "attachments": attachments,
        }

    except HTTPException:

        raise

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e),
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
