import re


class QueryAnalyzerService:

    STOPWORDS = {
        "el",
        "la",
        "los",
        "las",
        "un",
        "una",
        "unos",
        "unas",
        "de",
        "del",
        "al",
        "y",
        "o",
        "u",
        "que",
        "como",
        "con",
        "para",
        "por",
        "en",
        "me",
        "te",
        "se",
        "mi",
        "tu",
        "su",
        "quiero",
        "quisiera",
        "necesito",
        "podria",
        "podrías",
        "puedo",
        "hacer",
        "sacar",
        "tener",
        "dar",
        "obtener",
    }

    def analyze(
        self,
        question: str,
    ) -> dict:

        if not question:

            return {
                "intent": "",
                "category": "",
                "keywords": [],
                "synonyms": [],
            }

        text = question.lower()

        words = re.findall(
            r"[a-záéíóúñ0-9]+",
            text,
        )

        keywords = []

        for word in words:

            if len(word) < 3:
                continue

            if word in self.STOPWORDS:
                continue

            if word not in keywords:
                keywords.append(word)

        return {
            "intent": question,
            "category": "",
            "keywords": keywords,
            "synonyms": [],
        }


query_analyzer_service = QueryAnalyzerService()
