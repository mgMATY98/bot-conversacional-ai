import json


class MessageService:

    # =====================================================
    # CREAR MENSAJE
    # =====================================================

    def create(
        self,
        text: str,
        sources: list[str] | None = None,
        attachments: list | dict | None = None,
    ) -> str:

        # Compatibilidad:
        # si viene un único documento como dict,
        # convertirlo automáticamente en lista.
        if attachments is None:
            attachments = []

        elif isinstance(attachments, dict):
            attachments = [attachments]

        return json.dumps(
            {
                "text": text,
                "sources": sources or [],
                "attachments": attachments,
            },
            ensure_ascii=False,
        )

    # =====================================================
    # LEER MENSAJE
    # =====================================================

    def parse(
        self,
        message: str,
    ) -> dict:

        try:

            data = json.loads(message)

            if isinstance(data, dict):

                sources = data.get("sources", [])

                if sources is None:
                    sources = []

                attachments = data.get("attachments", [])

                if attachments is None:
                    attachments = []

                elif isinstance(attachments, dict):
                    attachments = [attachments]

                elif not isinstance(attachments, list):
                    attachments = []

                return {
                    "text": data.get("text", ""),
                    "sources": sources,
                    "attachments": attachments,
                }

        except Exception:
            pass

        return {
            "text": message,
            "sources": [],
            "attachments": [],
        }


message_service = MessageService()
