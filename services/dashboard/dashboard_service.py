from openai import conversations
from sqlalchemy.orm import Session

from app.models.contact import Contact
from app.models.conversation import Conversation
from app.models.document import Document
from app.models.idea import Idea
from app.models.whatsapp_connection import WhatsAppConnection

from services.summary.summary_service import summary_service


class DashboardService:

    # ==========================================================
    # DASHBOARD
    # ==========================================================

    def get_dashboard(self, db: Session, client):

        stats = self.get_stats(db, client)

        conversations = self.get_recent_conversations(db, client)

        ideas = self.get_recent_ideas(db, client)

        documents = self.get_recent_documents(db, client)

        whatsapp = self.get_whatsapp_status(db, client)

        summary = summary_service.generate_dashboard_summary(
            stats=stats,
            conversations=conversations,
            ideas=ideas,
            documents=documents,
            whatsapp=whatsapp,
        )

        return {
            "summary": summary,
            "stats": stats,
            "recentConversations": conversations,
            "recentIdeas": ideas,
            "recentDocuments": documents,
            "whatsapp": whatsapp,
        }

    # ==========================================================
    # STATS
    # ==========================================================

    def get_stats(self, db: Session, client):

        conversation_count = (
            db.query(Conversation)
            .join(Contact)
            .filter(Contact.client_id == client.id)
            .count()
        )

        idea_count = (
            db.query(Idea).join(Contact).filter(Contact.client_id == client.id).count()
        )

        document_count = (
            db.query(Document).filter(Document.client_id == client.id).count()
        )

        whatsapp = (
            db.query(WhatsAppConnection)
            .filter(WhatsAppConnection.client_id == client.id)
            .first()
        )

        return {
            "conversations": conversation_count,
            "ideas": idea_count,
            "documents": document_count,
            "whatsappConnected": bool(whatsapp and whatsapp.connected),
        }

    # ==========================================================
    # RECENT CONVERSATIONS
    # ==========================================================

    def get_recent_conversations(self, db: Session, client):

        contacts = (
            db.query(Contact)
            .filter(Contact.client_id == client.id)
            .order_by(Contact.updated_at.desc())
            .limit(5)
            .all()
        )

        conversations = []

        for contact in contacts:

            last_message = (
                db.query(Conversation)
                .filter(Conversation.contact_id == contact.id)
                .order_by(Conversation.created_at.desc())
                .first()
            )

            if not last_message:

                continue

            conversations.append(
                {
                    "id": contact.id,
                    "contact_id": contact.id,
                    # Nombre visible
                    "contact_name": contact.name or contact.user_id,
                    # WhatsApp / Telegram ID
                    "user_id": contact.user_id,
                    # Canal
                    "channel": contact.channel,
                    # Último mensaje
                    "lastMessage": last_message.message,
                    # Quién envió el último mensaje
                    "lastRole": last_message.role,
                    # Cantidad de mensajes
                    "messagesCount": (
                        db.query(Conversation)
                        .filter(Conversation.contact_id == contact.id)
                        .count()
                    ),
                    # Fecha
                    "date": last_message.created_at.strftime("%d/%m/%Y %H:%M"),
                }
            )

        return conversations

    # ==========================================================
    # RECENT IDEAS
    # ==========================================================

    def get_recent_ideas(self, db: Session, client):

        ideas = (
            db.query(Idea)
            .join(Contact)
            .filter(Contact.client_id == client.id)
            .order_by(Idea.created_at.desc())
            .limit(5)
            .all()
        )

        return [
            {
                "id": idea.id,
                "title": idea.summary,
                "priority": idea.priority,
                "created_at": idea.created_at.strftime("%d/%m/%Y"),
            }
            for idea in ideas
        ]

    # ==========================================================
    # RECENT DOCUMENTS
    # ==========================================================

    def get_recent_documents(self, db: Session, client):

        documents = (
            db.query(Document)
            .filter(Document.client_id == client.id)
            .order_by(Document.created_at.desc())
            .limit(5)
            .all()
        )

        return [
            {
                "id": document.id,
                "name": document.title,
                "uploaded_at": document.created_at.strftime("%d/%m/%Y"),
            }
            for document in documents
        ]

    # ==========================================================
    # WHATSAPP
    # ==========================================================

    def get_whatsapp_status(self, db: Session, client):

        whatsapp = (
            db.query(WhatsAppConnection)
            .filter(WhatsAppConnection.client_id == client.id)
            .first()
        )

        if whatsapp is None:

            return {"connected": False, "phone": "", "lastSync": ""}

        return {
            "connected": whatsapp.connected,
            "phone": whatsapp.phone or "",
            "lastSync": (
                whatsapp.updated_at.strftime("%d/%m/%Y %H:%M")
                if whatsapp.updated_at
                else ""
            ),
        }


dashboard_service = DashboardService()
