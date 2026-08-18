import json

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.contact import Contact


class ConversationStateService:

    # ==========================================
    # Estado
    # ==========================================

    def get_state(
        self,
        contact: Contact,
    ) -> str:

        return contact.conversation_state

    # ==========================================
    # Contexto
    # ==========================================

    def get_context(
        self,
        contact: Contact,
    ) -> dict:

        if not contact.conversation_context:
            return {}

        try:
            return json.loads(contact.conversation_context)

        except Exception:
            return {}

    # ==========================================
    # Guardar estado
    # ==========================================

    def set_state(
        self,
        db: Session,
        contact: Contact,
        state: str,
        context: dict | None = None,
    ):

        contact.conversation_state = state

        contact.conversation_context = json.dumps(
            context or {},
            ensure_ascii=False,
        )

        contact.conversation_updated_at = datetime.utcnow()

        db.commit()

        db.refresh(contact)

    # ==========================================
    # Limpiar
    # ==========================================

    def clear(
        self,
        db: Session,
        contact: Contact,
    ):

        contact.conversation_state = "NORMAL"

        contact.conversation_context = None

        contact.conversation_updated_at = datetime.utcnow()

        db.commit()

        db.refresh(contact)

    # ==========================================
    # Actualizar actividad
    # ==========================================

    def touch(
        self,
        db: Session,
        contact: Contact,
    ):

        contact.conversation_updated_at = datetime.utcnow()

        db.commit()

    # ==========================================
    # ¿Expiró?
    # ==========================================

    def is_expired(
        self,
        contact: Contact,
        hours: int = 24,
    ) -> bool:

        if contact.conversation_updated_at is None:
            return True

        return (datetime.utcnow() - contact.conversation_updated_at) > timedelta(
            hours=hours
        )


conversation_state_service = ConversationStateService()
