from openai import OpenAI, OpenAIError

from app.core.config import settings


class AIService:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
        )

        self.model = "gpt-4.1-mini"

    def generate(
        self,
        messages: list[dict],
    ) -> str:

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )

            content = response.choices[0].message.content or ""

            # Si la IA respondió un JSON por error,
            # devolver únicamente el texto.
            try:

                import json

                data = json.loads(content)

                if isinstance(data, dict):

                    if "text" in data:

                        return data["text"]

            except Exception:

                pass

            return content

        except OpenAIError as e:

            print(f"OpenAI Error: {e}")

            return (
                "Lo siento, en este momento no puedo responder. "
                "Intentá nuevamente en unos minutos."
            )


ai_service = AIService()
