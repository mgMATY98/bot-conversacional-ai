from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.client import Client

from app.core.auth import hash_password
from app.core.bot_config_factory import (
    create_default_bot_config,
)

from app.schemas.clients import (
    ClientCreate,
    ClientUpdate,
)


class AdminService:

    # ==========================================================
    # LISTAR CLIENTES
    # ==========================================================

    def list_clients(
        self,
        db: Session,
    ):

        return db.query(Client).order_by(Client.id).all()

    # ==========================================================
    # OBTENER CLIENTE
    # ==========================================================

    def get_client(
        self,
        db: Session,
        client_id: int,
    ):

        client = db.query(Client).filter(Client.id == client_id).first()

        if client is None:

            raise HTTPException(
                status_code=404,
                detail="Cliente no encontrado",
            )

        return client

    # ==========================================================
    # CREAR CLIENTE
    # ==========================================================

    def create_client(
        self,
        db: Session,
        data: ClientCreate,
    ):

        exists = db.query(Client).filter(Client.username == data.username).first()

        if exists:

            raise HTTPException(
                status_code=400,
                detail="Ese usuario ya existe",
            )

        client = Client(
            username=data.username,
            password_hash=hash_password(data.password),
            organization_name=data.organization_name,
            representative_name=data.representative_name,
            representative_role=data.representative_role,
            municipality=data.municipality,
            province=data.province,
            bot_phone=data.bot_phone,
            active=True,
        )

        db.add(client)

        db.commit()

        db.refresh(client)

        # ==========================================
        # Crear configuración por defecto del bot
        # ==========================================

        db.add(create_default_bot_config(client.id))

        db.commit()

        return client

    # ==========================================================
    # ACTUALIZAR CLIENTE
    # ==========================================================

    def update_client(
        self,
        db: Session,
        client_id: int,
        data: ClientUpdate,
    ):

        client = self.get_client(
            db,
            client_id,
        )

        update_data = data.model_dump(
            exclude_unset=True,
        )

        if "password" in update_data:

            client.password_hash = hash_password(update_data.pop("password"))

        for key, value in update_data.items():

            setattr(client, key, value)

        db.commit()

        db.refresh(client)

        return client

    # ==========================================================
    # CAMBIAR CANAL DE WHATSAPP
    # ==========================================================

    def change_whatsapp_channel(
        self,
        db: Session,
        client_id: int,
        channel: str,
    ):

        client = self.get_client(
            db,
            client_id,
        )

        # ======================================================
        # VALIDAR CANAL
        # ======================================================

        allowed_channels = [
            "whatsapp_web",
            "whatsapp_cloud",
        ]

        if channel not in allowed_channels:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Canal WhatsApp inválido. "
                    "Los canales permitidos son "
                    "'whatsapp_web' y 'whatsapp_cloud'."
                ),
            )

        # ======================================================
        # CLOUD
        # ======================================================

        if channel == "whatsapp_cloud":

            if not client.whatsapp_cloud_connection:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "WhatsApp Cloud API no está " "configurado para este cliente."
                    ),
                )

            if not client.whatsapp_cloud_connection.active:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "WhatsApp Cloud API está " "configurada pero no está activa."
                    ),
                )

        # ======================================================
        # CAMBIAR CANAL
        # ======================================================

        client.active_channel = channel

        db.commit()

        db.refresh(client)

        return {
            "success": True,
            "client_id": client.id,
            "active_channel": client.active_channel,
        }

    # ==========================================================
    # ELIMINAR CLIENTE
    # ==========================================================

    def delete_client(
        self,
        db: Session,
        client_id: int,
    ):

        client = self.get_client(
            db,
            client_id,
        )

        db.delete(client)

        db.commit()

        return {
            "message": "Cliente eliminado correctamente",
        }


admin_service = AdminService()
