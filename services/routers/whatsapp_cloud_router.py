from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_client
from app.db.database import get_db

from app.models.whatsapp_cloud_connection import (
    WhatsAppCloudConnection,
)

from app.schemas.whatsapp_cloud_schema import (
    WhatsAppCloudConfigRequest,
)
from services.whatsapp import whatsapp_cloud_service

router = APIRouter(
    prefix="/whatsapp-cloud",
    tags=["WhatsApp Cloud"],
)

from services.channel.channel_service import (
    channel_service,
)

# ==========================================================
# CONFIGURAR WHATSAPP CLOUD
# ==========================================================


@router.post("/config")
def configure_whatsapp_cloud(
    data: WhatsAppCloudConfigRequest,
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    try:

        # ======================================================
        # 1. VALIDAR QUE EL CLIENTE TENGA BOT_PHONE
        # ======================================================

        if not current_client.bot_phone:

            raise HTTPException(
                status_code=400,
                detail=("El cliente no tiene configurado " "un número de WhatsApp."),
            )

        # ======================================================
        # 2. CONSULTAR EL NÚMERO EN META
        # ======================================================

        phone_info = whatsapp_cloud_service.get_phone_number_info(
            access_token=data.access_token,
            phone_number_id=data.phone_number_id,
        )

        if not phone_info.get("success"):

            raise HTTPException(
                status_code=400,
                detail={
                    "message": (
                        "No se pudo validar el número " "contra WhatsApp Cloud API."
                    ),
                    "meta": phone_info.get("error"),
                },
            )

        meta_data = phone_info.get(
            "data",
            {},
        )

        meta_phone = meta_data.get("display_phone_number")

        # ======================================================
        # 3. NORMALIZAR NÚMEROS
        # ======================================================

        def normalize_phone(phone):

            if not phone:
                return ""

            return "".join(character for character in str(phone) if character.isdigit())

        client_phone = normalize_phone(current_client.bot_phone)

        meta_phone_normalized = normalize_phone(meta_phone)

        # ======================================================
        # 4. COMPARAR
        # ======================================================

        if client_phone != meta_phone_normalized:

            raise HTTPException(
                status_code=400,
                detail={
                    "message": (
                        "El número de WhatsApp de Meta "
                        "no coincide con el número "
                        "configurado para este cliente."
                    ),
                    "client_phone": current_client.bot_phone,
                    "meta_phone": meta_phone,
                },
            )

        # ======================================================
        # 5. BUSCAR CONFIGURACIÓN EXISTENTE
        # ======================================================

        connection = (
            db.query(WhatsAppCloudConnection)
            .filter(WhatsAppCloudConnection.client_id == current_client.id)
            .first()
        )

        # ======================================================
        # 6. CREAR CONFIGURACIÓN
        # ======================================================

        if not connection:

            connection = WhatsAppCloudConnection(
                client_id=current_client.id,
                phone_number_id=data.phone_number_id,
                access_token=data.access_token,
                waba_id=data.waba_id,
                verify_token=data.verify_token,
                active=False,
            )

            db.add(connection)

        # ======================================================
        # 7. ACTUALIZAR CONFIGURACIÓN
        # ======================================================

        else:

            connection.phone_number_id = data.phone_number_id

            connection.access_token = data.access_token

            connection.waba_id = data.waba_id

            connection.verify_token = data.verify_token

            # Nunca activar automáticamente.

            connection.active = False

        # ======================================================
        # 8. GUARDAR
        # ======================================================

        db.commit()

        db.refresh(connection)

        return {
            "success": True,
            "message": ("WhatsApp Cloud configurado " "correctamente como respaldo."),
            "cloud": {
                "id": connection.id,
                "client_id": connection.client_id,
                "phone_number_id": (connection.phone_number_id),
                "phone": meta_phone,
                "waba_id": connection.waba_id,
                "active": connection.active,
            },
        }

    except HTTPException:

        db.rollback()

        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ==========================================================
# OBTENER CONFIGURACIÓN
# ==========================================================


@router.get("/config")
def get_whatsapp_cloud_config(
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    connection = (
        db.query(WhatsAppCloudConnection)
        .filter(WhatsAppCloudConnection.client_id == current_client.id)
        .first()
    )

    # ======================================================
    # TODAVÍA NO CONFIGURADO
    # ======================================================

    if not connection:

        return {
            "configured": False,
            "cloud": None,
        }

    # ======================================================
    # CONFIGURADO
    # ======================================================

    return {
        "configured": True,
        "cloud": {
            "id": connection.id,
            "client_id": connection.client_id,
            "phone_number_id": (connection.phone_number_id),
            "waba_id": (connection.waba_id),
            "active": (connection.active),
        },
    }


@router.post("/activate")
def activate_whatsapp_cloud(
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    try:

        result = channel_service.activate_cloud(
            db=db,
            client=current_client,
        )

        return {
            "success": True,
            "message": ("WhatsApp Cloud API activado " "como canal principal."),
            "active_channel": (result["active_channel"]),
        }

    except ValueError as e:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ==========================================================
# ESTADO DEL CANAL
# ==========================================================


@router.get("/channel")
def get_active_channel(
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    connection = (
        db.query(WhatsAppCloudConnection)
        .filter(WhatsAppCloudConnection.client_id == current_client.id)
        .first()
    )

    return {
        "success": True,
        "active_channel": (current_client.active_channel),
        "cloud_configured": (connection is not None),
        "cloud_active": (connection.active if connection else False),
    }


# ==========================================================
# VOLVER A WHATSAPP WEB
# ==========================================================


@router.post("/activate-web")
def activate_whatsapp_web(
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    try:

        result = channel_service.activate_web(
            db=db,
            client=current_client,
        )

        return {
            "success": True,
            "message": ("WhatsApp Web restaurado " "como canal principal."),
            "active_channel": (result["active_channel"]),
        }

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
