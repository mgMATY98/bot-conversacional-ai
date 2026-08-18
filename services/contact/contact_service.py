from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.contact import Contact
from app.models.conversation import Conversation
from datetime import datetime


class ContactService:

    def list_contacts(
        self,
        db: Session,
        client_id: int,
    ):

        contacts = (
            db.query(Contact)
            .filter(Contact.client_id == client_id)
            .order_by(Contact.updated_at.desc())
            .all()
        )

        result = []

        for contact in contacts:

            last_message = (
                db.query(Conversation)
                .filter(
                    Conversation.contact_id == contact.id,
                )
                .order_by(Conversation.created_at.desc())
                .first()
            )

            messages_count = (
                db.query(Conversation)
                .filter(
                    Conversation.contact_id == contact.id,
                )
                .count()
            )

            result.append(
                {
                    "id": contact.id,
                    "user_id": contact.user_id,
                    "channel": contact.channel,
                    "name": contact.name,
                    "last_message": (last_message.message if last_message else None),
                    "last_role": (last_message.role if last_message else None),
                    "last_message_at": (
                        last_message.created_at if last_message else None
                    ),
                    "messages_count": messages_count,
                }
            )

        return result

    def get_contact(
        self,
        db: Session,
        client_id: int,
        contact_id: int,
    ):

        contact = (
            db.query(Contact)
            .filter(
                Contact.client_id == client_id,
                Contact.id == contact_id,
            )
            .first()
        )

        if contact is None:
            raise HTTPException(
                status_code=404,
                detail="Contacto no encontrado",
            )

        return contact

    def get_contact_by_user_id(
        self,
        db: Session,
        client_id: int,
        user_id: str,
    ):

        return (
            db.query(Contact)
            .filter(
                Contact.client_id == client_id,
                Contact.user_id == user_id,
            )
            .first()
        )

    def create_contact(
        self,
        db: Session,
        client_id: int,
        user_id: str,
        channel: str,
        name: str | None = None,
    ):

        contact = Contact(
            client_id=client_id,
            user_id=user_id,
            channel=channel,
            name=name,
        )

        db.add(contact)
        db.commit()
        db.refresh(contact)

        return contact

    def get_or_create_contact(
        self,
        db: Session,
        client_id: int,
        user_id: str,
        channel: str,
        name: str | None = None,
    ):

        contact = self.get_contact_by_user_id(
            db,
            client_id,
            user_id,
        )

        if contact:

            # Actualizar nombre si cambió
            if name and contact.name != name:
                contact.name = name

            # Actualizar última actividad
            contact.updated_at = datetime.utcnow()

            db.commit()

            db.refresh(contact)

            return contact

        return self.create_contact(
            db,
            client_id,
            user_id,
            channel,
            name,
        )

    def set_pending_document(
        self,
        db: Session,
        contact_id: int,
        document_id: int | None,
    ):

        contact = db.query(Contact).filter(Contact.id == contact_id).first()

        if not contact:
            return

        contact.pending_document_id = document_id

        db.commit()

        db.refresh(contact)

        return contact

    def clear_pending_document(
        self,
        db: Session,
        contact_id: int,
    ):

        return self.set_pending_document(
            db=db,
            contact_id=contact_id,
            document_id=None,
        )


contact_service = ContactService()
