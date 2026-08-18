import requests


class WhatsAppCloudService:

    GRAPH_URL = "https://graph.facebook.com/v23.0"

    # ==========================================================
    # ENVIAR MENSAJE
    # ==========================================================

    def send_message(
        self,
        access_token: str,
        phone_number_id: str,
        to: str,
        message: str,
    ) -> dict:

        url = f"{self.GRAPH_URL}/" f"{phone_number_id}/messages"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {
                "body": message,
            },
        }

        try:

            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=10,
            )

            try:
                data = response.json()
            except ValueError:

                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": response.text,
                }

            if response.ok:

                return {
                    "success": True,
                    "status_code": response.status_code,
                    "data": data,
                }

            return {
                "success": False,
                "status_code": response.status_code,
                "error": data,
            }

        except requests.exceptions.Timeout:

            return {
                "success": False,
                "status_code": 408,
                "error": "Timeout conectando con WhatsApp Cloud API.",
            }

        except requests.exceptions.RequestException as e:

            return {
                "success": False,
                "status_code": 500,
                "error": str(e),
            }

    # ==========================================================
    # OBTENER INFORMACIÓN DEL NÚMERO DESDE META
    # ==========================================================

    def get_phone_number_info(
        self,
        access_token: str,
        phone_number_id: str,
    ) -> dict:

        url = f"{self.GRAPH_URL}/" f"{phone_number_id}"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        params = {
            "fields": "id,display_phone_number,verified_name",
        }

        try:

            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=10,
            )

            try:
                data = response.json()

            except ValueError:

                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": response.text,
                }

            if response.ok:

                return {
                    "success": True,
                    "status_code": response.status_code,
                    "data": data,
                }

            return {
                "success": False,
                "status_code": response.status_code,
                "error": data,
            }

        except requests.exceptions.Timeout:

            return {
                "success": False,
                "status_code": 408,
                "error": ("Timeout consultando " "WhatsApp Cloud API."),
            }

        except requests.exceptions.RequestException as e:

            return {
                "success": False,
                "status_code": 500,
                "error": str(e),
            }


whatsapp_cloud_service = WhatsAppCloudService()
