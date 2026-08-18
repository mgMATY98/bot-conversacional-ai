from datetime import datetime

from sqlalchemy.orm import Session

from app.models.client import Client
from app.models.whatsapp_connection import WhatsAppConnection


class WhatsAppConnectionService:

    def upsert_connection(
        self,
        db: Session,
        client_id: int,
        phone: str,
        push_name: str | None,
    ) -> WhatsAppConnection:

        # Verificamos que el cliente exista
        client = db.query(Client).filter(Client.id == client_id).first()

        if client is None:
            raise ValueError(f"El cliente {client_id} no existe.")

        # Buscamos una conexión existente
        connection = (
            db.query(WhatsAppConnection)
            .filter(WhatsAppConnection.client_id == client_id)
            .first()
        )

        # Si no existe la creamos
        if connection is None:

            connection = WhatsAppConnection(
                client_id=client_id,
                session_id=f"client_{client_id}",
            )

            db.add(connection)

        # Actualizamos la información
        connection.phone = phone
        connection.push_name = push_name
        connection.connected = True
        connection.status = "CONNECTED"
        connection.last_seen = datetime.utcnow()
        connection.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(connection)

        return connection

    def disconnect(
        self,
        db: Session,
        client_id: int,
    ):

        connection = (
            db.query(WhatsAppConnection)
            .filter(WhatsAppConnection.client_id == client_id)
            .first()
        )

        if connection is None:
            return None

        connection.connected = False
        connection.status = "DISCONNECTED"

        connection.phone = ""
        connection.push_name = ""
        connection.last_qr = None

        connection.last_seen = datetime.utcnow()
        connection.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(connection)

        return connection

    def update_status(
        self,
        db: Session,
        client_id: int,
        status: str,
    ):

        connection = (
            db.query(WhatsAppConnection)
            .filter(WhatsAppConnection.client_id == client_id)
            .first()
        )

        if connection is None:
            return None

        connection.status = status

        if status == "AUTHENTICATED":
            connection.connected = False

        elif status == "CONNECTED":
            connection.connected = True

        elif status == "DISCONNECTED":
            connection.connected = False

        connection.last_seen = datetime.utcnow()

        db.commit()
        db.refresh(connection)

        return connection

    def update_qr(
        self,
        db: Session,
        client_id: int,
        qr: str,
    ):

        connection = (
            db.query(WhatsAppConnection)
            .filter(WhatsAppConnection.client_id == client_id)
            .first()
        )

        if connection is None:
            return None

        connection.last_qr = qr
        connection.last_seen = datetime.utcnow()

        db.commit()

        return connection


whatsapp_connection_service = WhatsAppConnectionService()
