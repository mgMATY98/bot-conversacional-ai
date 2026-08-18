import json

from app.models.conversation import Conversation


class PromptService:

    # ==================================================
    # CONSTRUIR MENSAJES
    # ==================================================

    def build_messages(
        self,
        config,
        knowledge: str,
        history: list[Conversation],
        user_message: str,
        intent: str,
        idea_context: dict | None = None,
    ) -> list[dict]:

        system_prompt = self._build_system_prompt(
            config=config,
            knowledge=knowledge,
            intent=intent,
            idea_context=idea_context,
        )

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        # ==========================================
        # Historial
        # ==========================================

        for conversation in history:

            content = conversation.message

            # Si el mensaje está guardado como JSON,
            # enviar únicamente el texto a OpenAI.
            try:

                payload = json.loads(content)

                if isinstance(payload, dict):

                    content = payload.get(
                        "text",
                        content,
                    )

            except Exception:

                pass

            messages.append(
                {
                    "role": conversation.role,
                    "content": content,
                }
            )

        # ==========================================
        # Último mensaje
        # ==========================================

        messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        return messages

    # ==================================================
    # PROMPT DEL SISTEMA
    # ==================================================

    def _build_system_prompt(
        self,
        config,
        knowledge: str,
        intent: str,
        idea_context: dict | None = None,
    ) -> str:
        sections = []
        # ==================================================
        # INTENCIÓN DETECTADA
        # ==================================================

        sections.extend(
            [
                "",
                "==============================",
                "INTENCIÓN DETECTADA",
                "==============================",
                "",
                f"Intención detectada: {intent}",
            ]
        )
        if intent == "greeting":

            sections.append(
                "El usuario está saludando. Respondé con un saludo breve, cálido y natural. "
                "Si es la primera conversación utilizá el mensaje de bienvenida configurado. "
                "Si ya hablaron anteriormente, saludalo normalmente sin volver a presentarte."
            )

        elif intent == "farewell":

            sections.append(
                "El usuario se está despidiendo. Respondé cordialmente con una despedida breve."
            )

        elif intent == "thanks":

            sections.append(
                "El usuario está agradeciendo. Respondé de forma amable y breve."
            )
        elif intent == "complaint":

            sections.append("""
        El usuario está realizando un reclamo.

        Mostrá empatía y obtené la información necesaria para poder gestionar el reclamo.

        El asistente puede registrar y gestionar reclamos directamente desde esta conversación.

        NO le indiques al ciudadano que debe realizar el reclamo por otro canal,
        por teléfono, mediante una aplicación, mediante una página web,
        presencialmente o ante otra dependencia, salvo que el usuario solicite
        explícitamente esa información o que el sistema indique que el trámite
        no puede ser gestionado desde esta conversación.

        Si todavía falta información importante para gestionar el reclamo,
        realizá preguntas concretas para obtenerla.

        Si el ciudadano ya proporcionó la información necesaria,
        no sigas haciendo preguntas innecesarias.

        No inventes números de reclamo, expedientes, tiempos de resolución,
        áreas responsables ni acciones que el sistema no haya realizado.

        Solo afirmá que un reclamo fue registrado, enviado o gestionado
        cuando el sistema realmente haya realizado esa acción.
        """)
        elif intent == "suggestion":

            sections.append(
                "El usuario está proponiendo una mejora o una idea. Agradecé la propuesta y profundizá si necesitás más información."
            )
        # ==================================================
        # IDENTIDAD
        # ==================================================

        sections.extend(
            [
                "==============================",
                "IDENTIDAD",
                "==============================",
                "",
                f"Tu nombre es {config.assistant_name}.",
                "Siempre respondé utilizando esa identidad.",
                "",
                "Si un ciudadano pregunta cómo te llamás,",
                "respondé únicamente con ese nombre.",
                "",
                "Nunca utilices otro nombre distinto.",
            ]
        )

        # ==================================================
        # PERSONALIDAD
        # ==================================================
        personality = config.personality.format(
            assistant_name=config.assistant_name,
            objective=config.objective,
            additional_instructions=config.additional_instructions,
            forbidden_topics=config.forbidden_topics or "Ninguno",
            forbidden_words=config.forbidden_words or "Ninguna",
        )
        sections.extend(
            [
                "",
                "==============================",
                "PERSONALIDAD",
                "==============================",
                "",
                personality,
            ]
        )
        objective = config.objective.format(
            assistant_name=config.assistant_name,
        )
        # ==================================================
        # OBJETIVO
        # ==================================================

        sections.extend(
            [
                "",
                "==============================",
                "OBJETIVO",
                "==============================",
                "",
                objective,
            ]
        )

        # ==================================================
        # INSTRUCCIONES ADICIONALES
        # ==================================================
        additional = config.additional_instructions.format(
            assistant_name=config.assistant_name,
            objective=config.objective,
        )
        if config.additional_instructions:

            sections.extend(
                [
                    "",
                    "==============================",
                    "INSTRUCCIONES ADICIONALES",
                    "==============================",
                    "",
                    additional,
                ]
            )

        # ==================================================
        # CONFIGURACIÓN
        # ==================================================

        sections.extend(
            [
                "",
                "==============================",
                "CONFIGURACIÓN",
                "==============================",
                "",
                f"Campañas políticas habilitadas: {'Sí' if config.political_campaigns else 'No'}",
            ]
        )

        if config.forbidden_topics:

            sections.extend(
                [
                    "",
                    "Temas prohibidos:",
                    config.forbidden_topics,
                ]
            )

        if config.forbidden_words:

            sections.extend(
                [
                    "",
                    "Palabras prohibidas:",
                    config.forbidden_words,
                ]
            )
        # ==================================================
        # CONTEXTO DEL RAG
        # ==================================================

        if knowledge:

            sections.extend(
                [
                    "",
                    "==============================",
                    "CONTEXTO",
                    "==============================",
                    "",
                    "Se encontraron documentos relevantes para responder esta consulta.",
                    "Utilizalos como fuente principal.",
                ]
            )

        else:

            sections.extend(
                [
                    "",
                    "==============================",
                    "CONTEXTO",
                    "==============================",
                    "",
                    "No se encontraron documentos relevantes para esta consulta.",
                    "Respondé utilizando tu conocimiento general.",
                ]
            )
        # ==================================================
        # DOCUMENTACIÓN
        # ==================================================

        if knowledge:

            sections.extend(
                [
                    "",
                    "==============================",
                    "DOCUMENTACIÓN DISPONIBLE",
                    "==============================",
                    "",
                    knowledge,
                ]
            )
        # ==================================================
        # GESTIÓN DE RECLAMOS E IDEAS
        # ==================================================

        sections.extend(
            [
                "",
                "==============================",
                "GESTIÓN DE RECLAMOS E IDEAS",
                "==============================",
                "",
                "Los reclamos, denuncias, sugerencias, propuestas y necesidades "
                "de los ciudadanos pueden ser registrados internamente por el sistema.",
                "",
                "El ciudadano no debe ser derivado automáticamente a un canal externo "
                "para realizar un reclamo.",
                "",
                "Cuando falte información necesaria para comprender o gestionar un reclamo, "
                "hacé preguntas concretas y relevantes.",
                "",
                "Cuando el ciudadano proporcione información adicional sobre un reclamo "
                "que ya está siendo conversado, considerala como parte del mismo problema "
                "y no como un problema completamente diferente.",
                "",
                "No afirmes que un reclamo fue registrado, enviado, derivado o resuelto "
                "si el sistema no realizó efectivamente esa acción.",
                "",
                "No inventes números de expediente, números de reclamo, plazos, "
                "áreas responsables ni estados de gestión.",
            ]
        )
        # ==================================================
        # IDEA DETECTADA / GESTIONADA
        # ==================================================
        if idea_context:

            sections.extend(
                [
                    "",
                    "==============================",
                    "RECLAMO REGISTRADO",
                    "==============================",
                    "",
                    "El sistema registró correctamente este reclamo en su base de datos.",
                    "",
                    f"ID del reclamo: {idea_context.get('id')}",
                    f"Tipo: {idea_context.get('type')}",
                    f"Categoría: {idea_context.get('category')}",
                    f"Prioridad: {idea_context.get('priority')}",
                    f"Estado: {idea_context.get('status')}",
                    f"Resumen: {idea_context.get('summary')}",
                    "",
                    "Podés informar al ciudadano que el reclamo fue registrado correctamente.",
                    "No le indiques al ciudadano que debe realizar nuevamente el reclamo.",
                    "No le indiques que debe acudir personalmente al municipio.",
                    "No le indiques que debe utilizar otro canal para registrar el reclamo.",
                    "No inventes acciones, funcionarios, áreas municipales ni tiempos de resolución.",
                    "Podés informar al ciudadano que su reclamo fue registrado.",
                ]
            )
        # ==================================================
        # REGLAS
        # ==================================================

        sections.extend(
            [
                "",
                "==============================",
                "REGLAS OBLIGATORIAS",
                "==============================",
                "",
                "1. Si existe documentación relevante para la consulta, utilizala como fuente principal.",
                "2. Nunca contradigas la documentación proporcionada.",
                "3. Si la documentación responde parcial o totalmente la consulta, basá tu respuesta en ella y complementala con tu conocimiento general únicamente si aporta valor y no genera contradicciones.",
                "4. Si no existe documentación relevante, respondé utilizando tu conocimiento general de forma natural y útil.",
                "5. Nunca inventes información oficial, normativas, trámites o datos específicos del cliente que no estén respaldados por la documentación.",
                "6. Cuando utilices documentación, mencioná naturalmente el nombre del documento utilizado.",
                "7. Si varios documentos aportan información, combiná el contenido de forma coherente.",
                "8. No copies grandes fragmentos de los documentos; resumí con tus propias palabras.",
                "9. Si la consulta es ambigua, pedí una aclaración antes de responder.",
                "10. Respondé siempre en español.",
                "11. Respondé de manera cordial, clara y profesional.",
                "12. Respondé SIEMPRE en texto plano.",
                "13. Nunca respondas utilizando formato JSON.",
                "14. Nunca incluyas campos como text, sources, attachments o similares.",
                "15. Tu respuesta debe ser únicamente el mensaje que leerá el usuario.",
            ]
        )

        return "\n".join(sections)

    def format_text(
        self,
        text: str,
        config,
    ):

        return text.format(
            assistant_name=config.assistant_name,
            objective=config.objective,
            additional_instructions=config.additional_instructions,
            forbidden_topics=config.forbidden_topics or "",
            forbidden_words=config.forbidden_words or "",
        )


prompt_service = PromptService()
