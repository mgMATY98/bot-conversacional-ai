from fastapi import APIRouter, Request, HTTPException, Response, Depends
from sqlalchemy.orm import Session
import logging
import traceback

from app.db.database import get_db

from app.models.whatsapp_cloud_connection import (
    WhatsAppCloudConnection,
)

from services.chat.chat_service import chat_service

from services.whatsapp.whatsapp_cloud_service import (
    whatsapp_cloud_service,
)

from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["WhatsApp Cloud Webhook"],
)


# ==========================================================
# VERIFICACIÓN DEL WEBHOOK
# ==========================================================


@router.get("/webhook/whatsapp")
async def verify_whatsapp_webhook(
    request: Request,
    db: Session = Depends(get_db),
):

    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode != "subscribe":

        raise HTTPException(
            status_code=400,
            detail="Invalid webhook mode.",
        )

    if not token:

        raise HTTPException(
            status_code=403,
            detail="Missing verify token.",
        )

    connection = (
        db.query(WhatsAppCloudConnection)
        .filter(WhatsAppCloudConnection.verify_token == token)
        .first()
    )

    if not connection:

        logger.warning("❌ Verify token de WhatsApp Cloud no encontrado.")

        raise HTTPException(
            status_code=403,
            detail="Invalid verify token.",
        )

    logger.info("✅ WhatsApp Cloud Webhook verificado.")

    return Response(
        content=challenge,
        media_type="text/plain",
    )


# ==========================================================
# RECIBIR MENSAJES
# ==========================================================


@router.post("/webhook/whatsapp")
async def whatsapp_cloud_webhook(
    request: Request,
    db: Session = Depends(get_db),
):

    try:

        data = await request.json()

        logger.info("📩 Webhook WhatsApp Cloud recibido.")

        # ==================================================
        # VALIDAR OBJECT
        # ==================================================

        if data.get("object") != "whatsapp_business_account":

            return {"status": "ignored_invalid_object"}

        # ==================================================
        # ENTRY
        # ==================================================

        entries = data.get(
            "entry",
            [],
        )

        if not entries:

            return {"status": "ignored_no_entry"}

        for entry in entries:

            changes = entry.get(
                "changes",
                [],
            )

            for change in changes:

                value = change.get(
                    "value",
                    {},
                )

                # ==========================================
                # IGNORAR ESTADOS
                # ==========================================

                if "statuses" in value:

                    continue

                # ==========================================
                # MENSAJES
                # ==========================================

                messages = value.get(
                    "messages",
                    [],
                )

                if not messages:

                    continue

                # ==========================================
                # PHONE NUMBER ID
                # ==========================================

                metadata = value.get(
                    "metadata",
                    {},
                )

                phone_number_id = metadata.get("phone_number_id")

                if not phone_number_id:

                    logger.warning("⚠️ Webhook sin phone_number_id.")

                    continue

                # ==========================================
                # BUSCAR CLIENTE
                # ==========================================

                connection = (
                    db.query(WhatsAppCloudConnection)
                    .filter(WhatsAppCloudConnection.phone_number_id == phone_number_id)
                    .first()
                )

                if not connection:

                    logger.error(
                        "❌ No existe conexión Cloud para "
                        f"phone_number_id={phone_number_id}"
                    )

                    continue

                client = connection.client

                if not client:

                    logger.error("❌ La conexión Cloud no tiene cliente.")

                    continue

                # ==========================================
                # VERIFICAR CANAL ACTIVO
                # ==========================================

                if client.active_channel != "whatsapp_cloud":

                    logger.info(
                        "ℹ️ Cloud recibió un mensaje pero " "no es el canal activo."
                    )

                    continue

                # ==========================================
                # PROCESAR MENSAJES
                # ==========================================

                for message in messages:

                    # ======================================
                    # SOLO TEXTO
                    # ======================================

                    if message.get("type") != "text":

                        logger.info("ℹ️ Mensaje no textual ignorado.")

                        continue

                    sender = message.get("from")

                    message_text = message.get("text", {}).get("body", "").strip()

                    if not sender or not message_text:

                        continue

                    # ======================================
                    # NOMBRE
                    # ======================================

                    contacts = value.get(
                        "contacts",
                        [],
                    )

                    push_name = ""

                    if contacts:

                        push_name = contacts[0].get("profile", {}).get("name", "")

                    # ======================================
                    # LOG
                    # ======================================

                    logger.info("====================================")

                    logger.info("📱 WHATSAPP CLOUD")

                    logger.info(f"Cliente : {client.id}")

                    logger.info(f"Municipio : {client.organization_name}")

                    logger.info(f"Número bot : {client.bot_phone}")

                    logger.info(f"Usuario : {sender}")

                    logger.info(f"Mensaje : {message_text}")

                    logger.info("====================================")

                    # ======================================
                    # CHAT ENGINE
                    # ======================================

                    result = chat_service.process_message(
                        db=db,
                        client_id=client.id,
                        user_id=sender,
                        channel="whatsapp",
                        message=message_text,
                        name=push_name,
                    )

                    reply = result.get("reply")

                    if not reply:

                        logger.warning("⚠️ Chat Service no generó respuesta.")

                        continue

                    # ======================================
                    # RESPONDER POR CLOUD
                    # ======================================

                    send_result = whatsapp_cloud_service.send_message(
                        access_token=(connection.access_token),
                        phone_number_id=(connection.phone_number_id),
                        to=sender,
                        message=reply,
                    )

                    # ======================================
                    # RESULTADO
                    # ======================================

                    if not send_result.get("success"):

                        logger.error(
                            "❌ Error enviando respuesta " "por WhatsApp Cloud."
                        )

                        logger.error(send_result)

                        continue

                    logger.info("✅ Respuesta enviada por " "WhatsApp Cloud.")

        # ==================================================
        # META NECESITA 200
        # ==================================================

        return {"status": "ok"}

    except Exception as e:

        logger.error("❌ ERROR procesando WhatsApp Cloud Webhook")

        traceback.print_exc()

        return {
            "status": "error",
            "error": str(e),
        }
