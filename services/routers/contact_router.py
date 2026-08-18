from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.auth import get_current_client

from services.contact.contact_service import contact_service

router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"],
)


@router.get("/")
def list_contacts(
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    return contact_service.list_contacts(
        db,
        current_client.id,
    )


@router.get("/{contact_id}")
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    return contact_service.get_contact(
        db,
        current_client.id,
        contact_id,
    )
