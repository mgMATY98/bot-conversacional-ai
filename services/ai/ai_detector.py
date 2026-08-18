import json

from app.core.openai_client import client


def detect_idea(message: str):
    """
    Analiza un mensaje y determina si contiene una idea, sugerencia,
    reclamo o propuesta útil para el municipio.
    """

    system_prompt = """
Sos un clasificador de mensajes para un municipio.

Debés responder ÚNICAMENTE un JSON válido.

Si el mensaje contiene:

- una sugerencia
- un reclamo
- una propuesta
- una mejora
- una solicitud de obra
- una denuncia
- una necesidad de los vecinos

respondé:

{
    "is_idea": true,
    "summary": "...",
    "category": "...",
    "priority": "LOW|MEDIUM|HIGH"
}

Si NO contiene una idea útil:

{
    "is_idea": false
}

No agregues texto.
No expliques nada.
Sólo JSON.
"""

    try:

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
        )

        content = response.choices[0].message.content

        return json.loads(content)

    except Exception:

        return {
            "is_idea": False,
        }
