from sqlalchemy.orm import Session

from app.models.whatsapp_cloud_connection import (
    WhatsAppCloudConnection,
)


class ChannelService:

    # ==========================================================
    # ACTIVAR WHATSAPP CLOUD
    # ==========================================================

    def activate_cloud(
        self,
        db: Session,
        client,
    ):

        connection = (
            db.query(WhatsAppCloudConnection)
            .filter(WhatsAppCloudConnection.client_id == client.id)
            .first()
        )

        # ======================================================
        # CLOUD NO CONFIGURADO
        # ======================================================

        if not connection:

            raise ValueError("WhatsApp Cloud API no está configurado.")

        # ======================================================
        # VALIDAR CONFIGURACIÓN
        # ======================================================

        if not connection.phone_number_id:

            raise ValueError("WhatsApp Cloud no tiene phone_number_id.")

        if not connection.access_token:

            raise ValueError("WhatsApp Cloud no tiene access_token.")

        # ======================================================
        # ACTIVAR
        # ======================================================

        client.active_channel = "whatsapp_cloud"

        connection.active = True

        db.commit()

        db.refresh(client)
        db.refresh(connection)

        return {
            "success": True,
            "active_channel": client.active_channel,
            "connection": connection,
        }

    # ==========================================================
    # ACTIVAR WHATSAPP WEB
    # ==========================================================

    def activate_web(
        self,
        db: Session,
        client,
    ):

        # ======================================================
        # DESACTIVAR CLOUD
        # ======================================================

        connection = (
            db.query(WhatsAppCloudConnection)
            .filter(WhatsAppCloudConnection.client_id == client.id)
            .first()
        )

        if connection:

            connection.active = False

        # ======================================================
        # ACTIVAR WEB
        # ======================================================

        client.active_channel = "whatsapp_web"

        db.commit()

        db.refresh(client)

        return {
            "success": True,
            "active_channel": client.active_channel,
        }

    # ==========================================================
    # OBTENER CANAL ACTIVO
    # ==========================================================

    def get_active_channel(
        self,
        client,
    ):

        return client.active_channel


# ==========================================================
# INSTANCIA GLOBAL
# ==========================================================

channel_service = ChannelService()
