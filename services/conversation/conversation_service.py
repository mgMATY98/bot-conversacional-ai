from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.contact import Contact
from app.models.conversation import Conversation

from services.conversation.message_service import message_service


class ConversationService:

    # ==========================================
    # Método interno
    # ==========================================

    def _save_message(
        self,
        db: Session,
        contact_id: int,
        role: str,
        text: str,
        sources: list[str] | None = None,
        attachments: list | None = None,
    ):
        conversation = Conversation(
            contact_id=contact_id,
            role=role,
            message=message_service.create(
                text=text,
                sources=sources,
                attachments=attachments,
            ),
        )
        db.add(conversation)

        contact = db.query(Contact).filter(Contact.id == contact_id).first()

        if contact:

            contact.updated_at = datetime.now(
                timezone.utc,
            )

        db.commit()

        db.refresh(conversation)

        return conversation

    # ==========================================
    # Guardado de mensajes
    # ==========================================
    def save_user_message(
        self,
        db: Session,
        contact_id: int,
        message: str,
    ):
        conversation = Conversation(
            contact_id=contact_id,
            role="user",
            message=message,
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation

    def save_assistant_message(
        self,
        db: Session,
        contact_id: int,
        message: str,
        sources: list[str] | None = None,
        attachments: list | None = None,
    ):

        return self._save_message(
            db=db,
            contact_id=contact_id,
            role="assistant",
            text=message,
            sources=sources,
            attachments=attachments,
        )

    # ==========================================
    # Obtener contacto del cliente
    # ==========================================

    def _get_contact(
        self,
        db: Session,
        client_id: int,
        contact_id: int,
    ):

        return (
            db.query(Contact)
            .filter(
                Contact.id == contact_id,
                Contact.client_id == client_id,
            )
            .first()
        )

    # ==========================================
    # Historial
    # ==========================================

    def get_history(
        self,
        db: Session,
        contact_id: int,
        hours: int | None = 24,
        limit: int = 12,
    ):

        query = db.query(Conversation).filter(
            Conversation.contact_id == contact_id,
        )

        if hours is not None:

            limit_date = datetime.now(timezone.utc) - timedelta(hours=hours)

            query = query.filter(
                Conversation.created_at >= limit_date,
            )

        history = (
            query.order_by(
                Conversation.created_at.desc(),
            )
            .limit(limit)
            .all()
        )

        history.reverse()

        return history

    # ==========================================
    # Información rápida
    # ==========================================

    def get_last_message(
        self,
        db: Session,
        contact_id: int,
    ):

        return (
            db.query(Conversation)
            .filter(Conversation.contact_id == contact_id)
            .order_by(Conversation.created_at.desc())
            .first()
        )
        # ==========================================
        # Último mensaje del asistente
        # ==========================================

    def count_messages(
        self,
        db: Session,
        contact_id: int,
    ):

        return (
            db.query(Conversation).filter(Conversation.contact_id == contact_id).count()
        )

    def is_first_contact(
        self,
        db: Session,
        contact_id: int,
    ):

        return (
            self.count_messages(
                db=db,
                contact_id=contact_id,
            )
            == 0
        )

    # ==========================================
    # Listado de conversaciones
    # ==========================================

    def list_conversations(
        self,
        db: Session,
        client_id: int,
    ):

        contacts = (
            db.query(Contact)
            .filter(Contact.client_id == client_id)
            .order_by(Contact.created_at.desc())
            .all()
        )

        conversations = []

        for contact in contacts:

            last_message = self.get_last_message(
                db=db,
                contact_id=contact.id,
            )

            conversations.append(
                {
                    "contact_id": contact.id,
                    "contact_name": contact.name,
                    "user_id": contact.user_id,
                    "last_message": (last_message.message if last_message else ""),
                    "last_message_at": (
                        last_message.created_at
                        if last_message
                        else datetime.now(timezone.utc)
                    ),
                    "message_count": self.count_messages(
                        db=db,
                        contact_id=contact.id,
                    ),
                }
            )

        return conversations

    # ==========================================
    # Obtener conversación completa
    # ==========================================

    def get_conversation(
        self,
        db: Session,
        client_id: int,
        contact_id: int,
    ):
        print("=========== SERVICE CONVERSATION ===========")
        print("CLIENT:", client_id)
        print("CONTACT:", contact_id)
        contact = self._get_contact(
            db=db,
            client_id=client_id,
            contact_id=contact_id,
        )

        if not contact:
            return []

        conversations = (
            db.query(Conversation)
            .filter(Conversation.contact_id == contact.id)
            .order_by(Conversation.created_at.asc())
            .all()
        )

        result = []

        for conversation in conversations:

            parsed = message_service.parse(conversation.message)

            result.append(
                {
                    "id": conversation.id,
                    "role": conversation.role,
                    "text": parsed["text"],
                    "sources": parsed["sources"],
                    "attachments": parsed["attachments"],
                    "created_at": conversation.created_at,
                }
            )

        return result

    # ==========================================
    # Últimos archivos enviados
    # ==========================================

    def get_last_attachments(
        self,
        db: Session,
        contact_id: int,
    ):

        conversations = (
            db.query(Conversation)
            .filter(
                Conversation.contact_id == contact_id,
                Conversation.role == "assistant",
            )
            .order_by(
                Conversation.created_at.desc(),
            )
            .limit(20)
            .all()
        )
        for conversation in conversations:

            parsed = message_service.parse(
                conversation.message,
            )

            if parsed["attachments"]:

                return parsed["attachments"]

        return []

    # ==========================================
    # Limpieza
    # ==========================================

    def clear_history(
        self,
        db: Session,
        client_id: int,
        contact_id: int,
    ):

        contact = self._get_contact(
            db=db,
            client_id=client_id,
            contact_id=contact_id,
        )

        if not contact:
            return

        (db.query(Conversation).filter(Conversation.contact_id == contact.id).delete())

        db.commit()

    # ==========================================
    # Historial para la IA
    # =========================================
    def get_history_for_ai(
        self,
        db: Session,
        contact_id: int,
        hours: int | None = 24,
        limit: int = 12,
    ):

        history = self.get_history(
            db=db,
            contact_id=contact_id,
            hours=hours,
            limit=limit,
        )

        messages = []

        for conversation in history:

            parsed = message_service.parse(
                conversation.message,
            )

            messages.append(
                {
                    "role": conversation.role,
                    "content": parsed["text"],
                }
            )

        return messages


conversation_service = ConversationService()
