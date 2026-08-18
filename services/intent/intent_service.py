import json

from app.core.openai_client import client


class IntentService:

    # ==================================================
    # DETECCIÓN LOCAL
    # ==================================================

    def detect(
        self,
        message: str,
    ):

        text = message.lower().strip()

        # -------------------------
        # Saludos
        # -------------------------

        greetings = {
            "hola",
            "hola!",
            "buenas",
            "buen día",
            "buen dia",
            "buenas tardes",
            "buenas noches",
            "hey",
            "hi",
        }

        if text in greetings:

            return {
                "intent": "greeting",
                "confidence": 1.0,
            }

        # -------------------------
        # Despedidas
        # -------------------------

        farewells = {
            "chau",
            "adios",
            "adiós",
            "hasta luego",
            "nos vemos",
            "bye",
        }

        if text in farewells:

            return {
                "intent": "farewell",
                "confidence": 1.0,
            }

        # -------------------------
        # Agradecimientos
        # -------------------------

        thanks = {
            "gracias",
            "muchas gracias",
            "mil gracias",
            "gracias!",
            "genial gracias",
            "perfecto gracias",
            "ok gracias",
            "listo gracias",
        }

        if text in thanks:

            return {
                "intent": "thanks",
                "confidence": 1.0,
            }

        # -------------------------
        # Catálogo de conocimiento
        # -------------------------

        catalog_patterns = [
            "qué documentos",
            "que documentos",
            "qué archivo",
            "que archivo",
            "qué archivos",
            "que archivos",
            "qué pdf",
            "que pdf",
            "qué información",
            "que información",
            "qué temas",
            "que temas",
            "qué sabés",
            "que sabes",
            "qué conocés",
            "que conoces",
            "qué podés responder",
            "que podes responder",
            "qué sabes hacer",
            "que sabes hacer",
            "qué conoces",
            "que conoces",
            "qué tenés",
            "que tenes",
            "qué información manejás",
            "que informacion manejas",
            "qué documentación",
            "que documentacion",
            "qué información disponible",
            "que informacion disponible",
        ]

        if any(pattern in text for pattern in catalog_patterns):

            return {
                "intent": "knowledge_catalog",
                "confidence": 1.0,
            }

        # ==================================================
        # IA (solo cuando realmente hace falta)
        # ==================================================

        try:

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                temperature=0,
                response_format={
                    "type": "json_object",
                },
                messages=[
                    {
                        "role": "system",
                        "content": """
Sos un clasificador de intenciones.

Las únicas intenciones posibles son:

- question
- complaint
- idea
- human
- chat

NO utilices greeting, farewell, thanks ni knowledge_catalog porque ya fueron detectadas previamente.

Respondé únicamente un JSON.

Ejemplo:

{
    "intent":"question",
    "confidence":0.97
}
""",
                    },
                    {
                        "role": "user",
                        "content": message,
                    },
                ],
            )

            return json.loads(response.choices[0].message.content)

        except Exception:

            return {
                "intent": "chat",
                "confidence": 0.0,
            }


intent_service = IntentService()
