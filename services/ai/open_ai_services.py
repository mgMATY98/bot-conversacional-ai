from openai import OpenAI

from app.core.config import settings


class OpenAIService:

    def __init__(self):

        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

        self.model = settings.OPENAI_MODEL

    def generate_response(
        self,
        system_prompt: str,
        history: list,
    ):

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        messages.extend(history)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        return response.choices[0].message.content


openai_service = OpenAIService()
