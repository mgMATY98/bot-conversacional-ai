from app.core.openai_client import client


def detect_idea_llm(message: str) -> str:

    try:

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            response_format={"type": "json_object"},
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": """
Sos un clasificador de mensajes ciudadanos.

Determiná si el mensaje contiene una propuesta, idea o sugerencia.

Respondé únicamente:

{
    "intent":"idea" o "chat",
    "confidence":0.0
}
""",
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
        )

        return response.choices[0].message.content.strip()

    except Exception:

        return '{"intent":"chat","confidence":0.0}'
