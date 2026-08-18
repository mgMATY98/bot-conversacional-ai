from services.ai.ai_service import ai_service

from services.document.text_chunk_service import text_chunk_service


class SummaryService:

    MAX_TEXT_LENGTH = 12000
    MAX_CHUNKS_DIRECT = 2
    # =====================================================
    # RESUMEN DE UN FRAGMENTO
    # =====================================================

    def _summarize_chunk(
        self,
        chunk: str,
    ) -> str:

        prompt = f"""
        Sos un asistente especializado en analizar documentos.

        Resumí el siguiente fragmento.

        No inventes información.

        El resumen debe tener entre 60 y 100 palabras.

        Fragmento:

        {chunk}
        """

        return ai_service.generate(
            [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )

    # =====================================================
    # DOCUMENTOS
    # =====================================================

    def generate_document_summary(
        self,
        text: str,
    ) -> str:

        if not text:
            return ""

        chunks = text_chunk_service.split(text)

        if not chunks:
            return ""

        # ==========================================
        # Documento pequeño
        # ==========================================

        if len(chunks) <= self.MAX_CHUNKS_DIRECT:

            prompt = f"""
            Sos un asistente especializado en analizar documentos.

            Generá un resumen profesional del siguiente documento.

            El resumen debe incluir:

            - De qué trata el documento.
            - Qué tipo de información contiene.
            - Cuáles son los temas principales.

            No inventes información.

            Debe tener entre 150 y 250 palabras.

            Documento:

            {text}
            """

            return ai_service.generate(
                [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ]
            )

        # ==========================================
        # Documento grande
        # ==========================================

        partial_summaries = []

        for chunk in chunks:

            try:

                summary = self._summarize_chunk(chunk)

                if summary:

                    partial_summaries.append(summary)

            except Exception:

                continue

        if not partial_summaries:
            return ""

        # ==========================================
        # Resumen final
        # ==========================================

        prompt = f"""
        Sos un asistente especializado en analizar documentos.

        A partir de los siguientes resúmenes parciales, generá un único resumen.

        Debe incluir:

        - De qué trata el documento.
        - Qué información contiene.
        - Cuáles son los temas principales.

        No inventes información.

        El resumen final debe tener entre 150 y 250 palabras.

        Resúmenes:

        {chr(10).join(partial_summaries)}
        """

        try:

            return ai_service.generate(
                [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ]
            )

        except Exception:

            # Si falla el resumen final,
            # devolver los resúmenes parciales unidos.
            return "\n\n".join(partial_summaries)

    # =====================================================
    # DASHBOARD
    # =====================================================

    def generate_dashboard_summary(
        self,
        stats,
        conversations,
        ideas,
        documents,
        whatsapp,
    ):

        prompt = f"""
        Sos un analista de datos especializado en municipios.

        Generá un resumen ejecutivo profesional.

        No inventes datos.

        Usá solamente la información proporcionada.

        El resumen debe tener entre 120 y 180 palabras.

        Finalizá siempre con una recomendación para el municipio.

        Si algun documento no tiene datos, no lo incluyas en el resumen.

        ESTADÍSTICAS

        - Conversaciones: {stats["conversations"]}

        - Ideas detectadas: {stats["ideas"]}

        - Documentos: {stats["documents"]}

        - WhatsApp conectado: {"Sí" if whatsapp["connected"] else "No"}

        ÚLTIMAS CONVERSACIONES

        {conversations}

        ÚLTIMAS IDEAS

        {ideas}

        ÚLTIMOS DOCUMENTOS

        {documents}
"""

        return ai_service.generate([{"role": "user", "content": prompt}])


summary_service = SummaryService()
