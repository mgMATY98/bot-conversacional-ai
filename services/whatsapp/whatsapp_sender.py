import requests

from sqlalchemy.orm import Session

from app.models.client import Client

from services.whatsapp.whatsapp_cloud_service import (
    whatsapp_cloud_service,
)

NODE_URL = "http://localhost:3001"


def send_whatsapp_message(
    db: Session,
    client: Client,
    to: str,
    message: str,
) -> dict:

    # ==========================================================
    # WHATSAPP CLOUD API
    # ==========================================================

    if client.active_channel == "whatsapp_cloud":

        connection = client.whatsapp_cloud_connection

        if not connection:

            return {
                "success": False,
                "error": ("WhatsApp Cloud API " "no está configurado."),
            }

        if not connection.active:

            return {
                "success": False,
                "error": ("WhatsApp Cloud API " "no está activa."),
            }

        return whatsapp_cloud_service.send_message(
            access_token=connection.access_token,
            phone_number_id=connection.phone_number_id,
            to=to,
            message=message,
        )

    # ==========================================================
    # WHATSAPP WEB
    # ==========================================================

    if client.active_channel == "whatsapp_web":

        session_id = f"client_{client.id}"

        try:

            response = requests.post(
                f"{NODE_URL}/sessions/{session_id}/message",
                json={
                    "to": to,
                    "message": message,
                },
                timeout=30,
            )

            try:
                data = response.json()

            except ValueError:

                return {
                    "success": False,
                    "channel": "whatsapp_web",
                    "error": ("El Gateway Node " "devolvió una respuesta inválida."),
                    "status_code": response.status_code,
                }

            if response.ok:

                return data

            return {
                "success": False,
                "channel": "whatsapp_web",
                "error": data.get(
                    "message",
                    "Error enviando mensaje por WhatsApp Web.",
                ),
                "status_code": response.status_code,
            }

        except requests.exceptions.Timeout:

            return {
                "success": False,
                "channel": "whatsapp_web",
                "error": ("Timeout comunicando " "con el Gateway de WhatsApp."),
            }

        except requests.exceptions.RequestException as e:

            return {
                "success": False,
                "channel": "whatsapp_web",
                "error": (f"Error comunicando con " f"el Gateway: {str(e)}"),
            }

    # ==========================================================
    # CANAL DESCONOCIDO
    # ==========================================================

    return {
        "success": False,
        "error": (f"Canal WhatsApp desconocido: " f"{client.active_channel}"),
    }
