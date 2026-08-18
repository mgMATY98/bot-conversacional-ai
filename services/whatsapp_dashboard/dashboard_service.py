import requests

from sqlalchemy.orm import Session

from app.models.whatsapp_connection import WhatsAppConnection

NODE_URL = "http://localhost:3001"


class WhatsAppDashboardService:

    # ==========================================================
    # STATUS
    # ==========================================================

    def get_status(
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

            return {
                "connected": False,
                "status": "DISCONNECTED",
                "phone": "",
                "push_name": "",
                "session_id": f"client_{client_id}",
                "last_seen": None,
            }

        return {
            "connected": connection.connected,
            "status": connection.status,
            "phone": connection.phone or "",
            "push_name": connection.push_name or "",
            "session_id": connection.session_id,
            "last_seen": connection.last_seen,
        }

    # ==========================================================
    # QR
    # ==========================================================

    def get_qr(
        self,
        db: Session,
        client_id: int,
    ):

        try:

            response = requests.get(
                f"{NODE_URL}/sessions/client_{client_id}/qr",
                timeout=5,
            )

            if response.status_code == 200:

                return response.json()

            return {
                "qr": "",
            }

        except Exception as e:

            print("Error obteniendo QR:", e)

            return {
                "qr": "",
            }

    # ==========================================================
    # CONECTAR
    # ==========================================================

    def reconnect(
        self,
        db: Session,
        client_id: int,
    ):

        try:

            response = requests.post(
                f"{NODE_URL}/sessions",
                json={
                    "client_id": client_id,
                },
                timeout=10,
            )

            return response.json()

        except Exception as e:

            return {
                "success": False,
                "error": str(e),
            }

    # ==========================================================
    # DESCONECTAR
    # ==========================================================

    def disconnect(
        self,
        db: Session,
        client_id: int,
    ):

        try:

            print("")
            print("====================================")
            print("🔴 DASHBOARD: solicitando desconexión")
            print("Cliente:", client_id)
            print("====================================")

            response = requests.post(
                f"{NODE_URL}/sessions/client_{client_id}/disconnect",
                timeout=10,
            )

            print("STATUS NODE:", response.status_code)
            print("RESPUESTA NODE:", response.text)

            result = response.json()

            # ======================================================
            # ACTUALIZAR SIEMPRE LA BD
            # ======================================================

            from services.whatsapp_connection_service import (
                whatsapp_connection_service,
            )

            connection = whatsapp_connection_service.disconnect(
                db=db,
                client_id=client_id,
            )

            print("")
            print("====================================")
            print("🗄️ BD ACTUALIZADA")
            print("connected:", connection.connected if connection else None)
            print("status:", connection.status if connection else None)
            print("====================================")

            return {
                "success": True,
                "status": "DISCONNECTED",
            }

        except requests.exceptions.RequestException as e:

            print(
                "❌ Error comunicando con WhatsApp:",
                e,
            )

            # Aunque Node no responda,
            # el dashboard debe reflejar que está desconectado.

            from services.whatsapp_connection_service import (
                whatsapp_connection_service,
            )

            connection = whatsapp_connection_service.disconnect(
                db=db,
                client_id=client_id,
            )

            return {
                "success": True,
                "status": "DISCONNECTED",
                "warning": "WhatsApp Gateway no respondió.",
            }

        except Exception as e:

            print(
                "❌ Error desconectando WhatsApp:",
                e,
            )

            return {
                "success": False,
                "error": str(e),
            }


whatsapp_dashboard_service = WhatsAppDashboardService()
